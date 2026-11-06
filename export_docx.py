import os
import re
import shutil
import sys
from pathlib import Path

import docx
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Inches, Pt, RGBColor

# Thử nạp bộ chuyển đổi công thức toán sang Native Word Equation (OMML)
HAS_MATH_TRANSFORM = False
_transform = None
try:
    import latex2mathml.converter
    import lxml.etree as ET

    env_xsl = os.environ.get("MML2OMML_PATH")
    candidates = [
        env_xsl,
        str(Path(__file__).resolve().parent / "MML2OMML.XSL"),
        r"C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL",
        r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL",
    ]
    for p in candidates:
        if p and os.path.exists(p):
            xslt_dom = ET.parse(p)
            _transform = ET.XSLT(xslt_dom)
            HAS_MATH_TRANSFORM = True
            break
except Exception:
    HAS_MATH_TRANSFORM = False


def _add_math_run(paragraph, latex_code: str):
    """Chuyển đổi chuỗi LaTeX thành Office Math (OMML) hoặc fallback dạng nghiêng."""
    clean_ltx = (
        latex_code.strip()
        .replace(r"\displaystyle", "")
        .replace(r"\mathrm", "")
        .replace(r"\text", "")
        .replace(r"\quad", " ")
        .replace(r"\qquad", "  ")
    )
    if HAS_MATH_TRANSFORM and _transform:
        try:
            mml_str = latex2mathml.converter.convert(clean_ltx)
            mml_dom = ET.fromstring(mml_str)
            omml_dom = _transform(mml_dom)
            paragraph._element.append(omml_dom.getroot())
            return
        except Exception:
            pass

    # Fallback chữ nghiêng nếu không chuyển đổi được OMML
    run = paragraph.add_run(f" {latex_code.strip()} ")
    run.font.name = "Cambria Math"
    run.italic = True


def _add_inline_formatted(paragraph, text: str, default_italic: bool = False, font_size: float = 12.0):
    """Thêm chuỗi văn bản có chứa $...$ hoặc $$...$$ và **in đậm** vào paragraph."""
    tokens = re.split(r"(\$\$[\s\S]+?\$\$|\$[^\$]+?\$)", text)
    for token in tokens:
        if not token:
            continue
        if token.startswith("$$") and token.endswith("$$"):
            _add_math_run(paragraph, token[2:-2])
        elif token.startswith("$") and token.endswith("$"):
            _add_math_run(paragraph, token[1:-1])
        else:
            sub_tokens = re.split(r"(\*\*[^\*]+?\*\*)", token)
            for st in sub_tokens:
                if not st:
                    continue
                if st.startswith("**") and st.endswith("**"):
                    run = paragraph.add_run(st[2:-2])
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(font_size)
                    run.bold = True
                    if default_italic:
                        run.italic = True
                else:
                    run = paragraph.add_run(st)
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(font_size)
                    if default_italic:
                        run.italic = True


def _set_cell_background(cell, fill_hex: str):
    """Đặt màu nền cho một ô trong bảng (hex, vd: 'F1F5F9')."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))


def _set_table_borders(table, color="94A3B8", sz="4", val="single"):
    """Đặt viền cho bảng Word."""
    tblPr = table._tbl.tblPr
    borders_xml = f"""
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
    </w:tblBorders>
    """
    tblPr.append(parse_xml(borders_xml))


def _set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt khoảng cách đệm (padding) trong ô bảng."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f"""
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    """)
    tcPr.append(tcMar)


def _render_markdown_table(doc, table_lines: list[str]):
    """Chuyển đổi một khối bảng Markdown (| ... | ... |) thành Bảng Microsoft Word hoàn chỉnh."""
    if not table_lines:
        return

    rows_data = []
    alignments = []

    for line in table_lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # Kiểm tra xem có phải dòng định dạng căn lề (| :--- | :---: |)
        if all(re.match(r"^:?-+:?$", c) for c in cells):
            alignments = []
            for c in cells:
                if c.startswith(":") and c.endswith(":"):
                    alignments.append(WD_ALIGN_PARAGRAPH.CENTER)
                elif c.endswith(":"):
                    alignments.append(WD_ALIGN_PARAGRAPH.RIGHT)
                else:
                    alignments.append(WD_ALIGN_PARAGRAPH.LEFT)
        else:
            rows_data.append(cells)

    if not rows_data or not rows_data[0]:
        return

    num_cols = max(len(r) for r in rows_data)
    # Chuẩn hóa số cột của các hàng
    for r in rows_data:
        while len(r) < num_cols:
            r.append("")

    table = doc.add_table(rows=len(rows_data), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True
    _set_table_borders(table, color="94A3B8", sz="4", val="single")

    for r_idx, r_vals in enumerate(rows_data):
        row = table.rows[r_idx]
        is_header = (r_idx == 0)

        for c_idx, cell_text in enumerate(r_vals):
            cell = row.cells[c_idx]
            _set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

            if is_header:
                _set_cell_background(cell, "F1F5F9")  # Nền xám nhạt tiêu chuẩn

            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)

            if c_idx < len(alignments):
                p.alignment = alignments[c_idx]
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (not is_header or c_idx > 0) else WD_ALIGN_PARAGRAPH.LEFT

            _add_inline_formatted(p, cell_text, default_italic=False, font_size=11.5)
            if is_header:
                for run in p.runs:
                    run.bold = True

    # Thêm khoảng cách nhỏ sau bảng
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(2)
    p_spacer.paragraph_format.space_after = Pt(2)


def _render_image(doc, img_src: str, img_alt: str = ""):
    """Chèn hình ảnh hình học / đồ thị vào Word, căn giữa và chuẩn kích thước in ấn."""
    img_clean = img_src.strip().strip("'\"")
    img_path = Path(img_clean)

    # Tìm kiếm file ảnh ở các vị trí phổ biến trong dự án
    candidates = [
        img_path,
        Path("output") / img_clean,
        Path("output/images") / img_path.name,
        Path("input/blueprint_images") / img_path.name,
        Path(os.getcwd()) / img_clean,
    ]
    resolved = None
    for c in candidates:
        if c.exists() and c.is_file():
            resolved = c
            break

    if resolved:
        try:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(4)
            p_img.paragraph_format.space_after = Pt(2)
            run = p_img.add_run()
            run.add_picture(str(resolved), width=Inches(3.3))

            # Chú thích hình ảnh bên dưới (nếu có alt text và không phải link rác)
            clean_alt = img_alt.strip()
            if clean_alt and not clean_alt.startswith("http") and not clean_alt.endswith((".png", ".jpg")):
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_before = Pt(0)
                p_cap.paragraph_format.space_after = Pt(4)
                r_cap = p_cap.add_run(f"({clean_alt})")
                r_cap.font.name = "Times New Roman"
                r_cap.font.size = Pt(10)
                r_cap.italic = True
        except Exception:
            pass


def _render_question_stem(doc, q_title: str, stem_text: str):
    """
    Hiển thị nội dung câu hỏi trong Word:
    - Giữ đúng thứ tự các đoạn văn bản, hình vẽ minh họa và bảng số liệu.
    - Hỗ trợ hình vẽ đồ thị & hình học không gian (![...](...)).
    - Phương án trắc nghiệm A, B, C, D: BỎ dấu gạch đầu dòng '-', tự động chia 2 cột đối với phương án ngắn (<= 75 ký tự).
    - Các mệnh đề Đúng/Sai a, b, c, d: BỎ dấu gạch đầu dòng '-', in đậm ký hiệu a), b), c), d).
    """
    lines = [l.strip() for l in stem_text.strip().splitlines() if l.strip()]
    if not lines:
        return

    # Regex nhận dạng hình ảnh Markdown ![alt](src)
    img_re = re.compile(r"!\[(.*?)\]\((.*?)\)")
    # Regex nhận dạng phương án trắc nghiệm A, B, C, D
    opt_re = re.compile(r"^(?:-\s+|\*\s+)?(?:\*\*)?([A-D])(?:\.|\:)\*{0,2}\s*(.*)$")
    # Regex nhận dạng mệnh đề Đúng/Sai a), b), c), d)
    sub_re = re.compile(r"^(?:-\s+|\*\s+)?(?:\*\*)?([a-d])\)\*{0,2}\s*(.*)$")

    blocks = []  # Danh sách ('text', str), ('table', list[str]), hoặc ('image', (alt, src))
    options_list = []  # Danh sách (A/B/C/D, content)
    subitems_list = []  # Danh sách (a/b/c/d, content)
    table_lines = []
    in_table = False

    def flush_table():
        nonlocal table_lines, in_table
        if table_lines:
            blocks.append(("table", list(table_lines)))
            table_lines = []
        in_table = False

    for line in lines:
        # Kiểm tra dòng bảng Markdown
        if line.startswith("|") and line.endswith("|") and line.count("|") >= 2:
            in_table = True
            table_lines.append(line)
            continue
        elif in_table:
            flush_table()

        # Kiểm tra hình ảnh Markdown
        m_img = img_re.search(line)
        if m_img:
            blocks.append(("image", (m_img.group(1), m_img.group(2))))
            continue

        # Kiểm tra phương án A, B, C, D
        m_opt = opt_re.match(line)
        if m_opt:
            options_list.append((m_opt.group(1).upper(), m_opt.group(2).strip()))
            continue

        # Kiểm tra mệnh đề a), b), c), d)
        m_sub = sub_re.match(line)
        if m_sub:
            subitems_list.append((m_sub.group(1).lower(), m_sub.group(2).strip()))
            continue

        # Dòng văn bản bình thường của câu hỏi
        blocks.append(("text", line))

    if in_table:
        flush_table()

    # 1. Render các khối văn bản, hình vẽ và bảng theo đúng thứ tự xuất hiện
    first_text_rendered = False
    for b_type, b_data in blocks:
        if b_type == "text":
            p = doc.add_paragraph()
            if not first_text_rendered:
                p.paragraph_format.space_before = Pt(6)
                p.paragraph_format.space_after = Pt(2)
                r_title = p.add_run(f"{q_title}. ")
                r_title.font.name = "Times New Roman"
                r_title.font.size = Pt(12)
                r_title.bold = True
                first_text_rendered = True
            else:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
            _add_inline_formatted(p, b_data, font_size=12.0)
        elif b_type == "table":
            _render_markdown_table(doc, b_data)
        elif b_type == "image":
            img_alt, img_src = b_data
            _render_image(doc, img_src, img_alt)

    # Nếu chưa có đoạn văn nào được render (vd câu hỏi bắt đầu ngay bằng bảng)
    if not first_text_rendered:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        r_title = p_q.add_run(f"{q_title}. ")
        r_title.font.name = "Times New Roman"
        r_title.font.size = Pt(12)
        r_title.bold = True

    # 2. Render các phương án A, B, C, D (Chia 2 cột nếu ngắn, không gạch đầu dòng)
    if options_list:
        max_opt_len = max(len(content) for _, content in options_list)
        # Nếu có đúng 4 phương án A, B, C, D và độ dài mỗi phương án <= 75 ký tự -> Chia 2 cột
        if len(options_list) == 4 and max_opt_len <= 75:
            opt_table = doc.add_table(rows=2, cols=2)
            opt_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            opt_table.autofit = False

            # Sắp xếp theo thứ tự: Hàng 1 (A, B) - Hàng 2 (C, D)
            grid_order = [
                (options_list[0], opt_table.cell(0, 0)),
                (options_list[1], opt_table.cell(0, 1)),
                (options_list[2], opt_table.cell(1, 0)),
                (options_list[3], opt_table.cell(1, 1)),
            ]
            for (opt_char, opt_content), cell in grid_order:
                cell.width = Inches(3.45)
                p_c = cell.paragraphs[0]
                p_c.paragraph_format.space_before = Pt(2)
                p_c.paragraph_format.space_after = Pt(2)
                r_c = p_c.add_run(f"{opt_char}. ")
                r_c.font.name = "Times New Roman"
                r_c.font.size = Pt(12)
                r_c.bold = True
                _add_inline_formatted(p_c, opt_content, font_size=12.0)

            p_sp = doc.add_paragraph()
            p_sp.paragraph_format.space_before = Pt(1)
            p_sp.paragraph_format.space_after = Pt(1)
        else:
            # Đáp án dài: Mỗi phương án 1 dòng, KHÔNG có gạch đầu dòng '-'
            for opt_char, opt_content in options_list:
                p_opt = doc.add_paragraph()
                p_opt.paragraph_format.left_indent = Inches(0.25)
                p_opt.paragraph_format.space_before = Pt(1.5)
                p_opt.paragraph_format.space_after = Pt(1.5)
                r_char = p_opt.add_run(f"{opt_char}. ")
                r_char.font.name = "Times New Roman"
                r_char.font.size = Pt(12)
                r_char.bold = True
                _add_inline_formatted(p_opt, opt_content, font_size=12.0)

    # 3. Hiển thị các mệnh đề Đúng/Sai a), b), c), d) (Không gạch đầu dòng)
    if subitems_list:
        for sub_char, sub_content in subitems_list:
            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.left_indent = Inches(0.25)
            p_sub.paragraph_format.space_before = Pt(2)
            p_sub.paragraph_format.space_after = Pt(2)
            r_sc = p_sub.add_run(f"{sub_char}) ")
            r_sc.font.name = "Times New Roman"
            r_sc.font.size = Pt(12)
            r_sc.bold = True
            _add_inline_formatted(p_sub, sub_content, font_size=12.0)


def export_exam_word(
    header_md: str,
    questions: list[dict],
    mode: str = "exam_only",  # 'exam_only' | 'exam_and_solution' | 'solution_only'
    school_name: str = "SỞ GIÁO DỤC VÀ ĐÀO TẠO",
    exam_title: str = "ĐỀ THI TỐT NGHIỆP TRUNG HỌC PHỔ THÔNG NĂM 2026",
    exam_code: str = "101",
    output_path: Path = None,
) -> Path:
    """
    Tạo file Word (.docx) chuyên nghiệp chuẩn Bộ GD&ĐT theo 3 chế độ:
    - 'exam_only': Chỉ xuất đề thi (để in cho học sinh).
    - 'exam_and_solution': Xuất toàn bộ đề thi kèm lời giải chi tiết.
    - 'solution_only': Bảng đáp án nhanh + Hướng dẫn giải chi tiết.
    """
    doc = Document()

    # Thiết lập lề trang tiêu chuẩn 2.0 cm (chuẩn văn bản Bộ GD&ĐT)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.79)
        section.bottom_margin = Inches(0.79)
        section.left_margin = Inches(0.79)
        section.right_margin = Inches(0.79)

    # -------------------------------------------------------------
    # 1. TIÊU ĐỀ ĐẦU TRANG (HEADER CHUẨN THPT)
    # -------------------------------------------------------------
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False

    cell_left, cell_right = header_table.rows[0].cells
    cell_left.width = Inches(3.2)
    cell_right.width = Inches(3.8)

    # Cột trái: Đơn vị / Cơ sở giáo dục
    p_l1 = cell_left.paragraphs[0]
    p_l1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_l1 = p_l1.add_run(school_name.upper())
    r_l1.font.name = "Times New Roman"
    r_l1.font.size = Pt(11)
    r_l1.bold = True

    p_l2 = cell_left.add_paragraph()
    p_l2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    mode_sub = (
        "ĐỀ CHÍNH THỨC"
        if mode == "exam_only"
        else ("ĐỀ THI & HƯỚNG DẪN GIẢI" if mode == "exam_and_solution" else "HƯỚNG DẪN CHẤM & ĐÁP ÁN")
    )
    r_l2 = p_l2.add_run(f"({mode_sub})")
    r_l2.font.name = "Times New Roman"
    r_l2.font.size = Pt(10.5)
    r_l2.italic = True

    # Cột phải: Tên kỳ thi + Môn thi + Thời gian
    p_r1 = cell_right.paragraphs[0]
    p_r1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_r1 = p_r1.add_run(exam_title.upper())
    r_r1.font.name = "Times New Roman"
    r_r1.font.size = Pt(11)
    r_r1.bold = True

    p_r2 = cell_right.add_paragraph()
    p_r2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_r2 = p_r2.add_run("Môn: TOÁN — Thời gian làm bài: 90 phút")
    r_r2.font.name = "Times New Roman"
    r_r2.font.size = Pt(10.5)
    r_r2.bold = True

    p_r3 = cell_right.add_paragraph()
    p_r3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_r3 = p_r3.add_run(f"Mã đề thi: {exam_code}")
    r_r3.font.name = "Times New Roman"
    r_r3.font.size = Pt(10)
    r_r3.italic = True

    # Khung thông tin thí sinh (Chỉ hiện khi thi thật hoặc đề ôn tập)
    if mode in {"exam_only", "exam_and_solution"}:
        p_info = doc.add_paragraph()
        p_info.paragraph_format.space_before = Pt(8)
        p_info.paragraph_format.space_after = Pt(10)
        r_info = p_info.add_run(
            "Họ và tên thí sinh: ..........................................................................   Số báo danh: ........................"
        )
        r_info.font.name = "Times New Roman"
        r_info.font.size = Pt(11)
        r_info.italic = True

    # Phân tích danh sách đáp án nhanh (cho bảng tổng kết)
    p1_answers = []
    p2_answers = []
    p3_answers = []
    for q in questions:
        sec = q.get("section", "")
        sol = q.get("solution", "")
        if "PHẦN III" in sec:
            m = re.search(r"Đáp số[^\w0-9\-]*([0-9\-\,\.]+)", sol, re.I)
            p3_answers.append((q["title"], m.group(1).strip() if m else "-"))
        elif "PHẦN II" in sec:
            sub_ans = {}
            for sub_m in re.finditer(r"([a-d])\)\s*(Đúng|Sai)", sol, re.I):
                sub_ans[sub_m.group(1).lower()] = sub_m.group(2).capitalize()
            p2_answers.append((q["title"], sub_ans))
        elif "PHẦN I" in sec:
            m = re.search(r"(?:Đáp án đúng|Chọn)[^\wA-D]*([A-D])\b", sol, re.I)
            p1_answers.append((q["title"], m.group(1) if m else "-"))

    # -------------------------------------------------------------
    # 2. BẢNG TỔNG KẾT ĐÁP ÁN NHANH (NẾU LÀ 'solution_only')
    # -------------------------------------------------------------
    if mode == "solution_only":
        p_table_title = doc.add_paragraph()
        p_table_title.paragraph_format.space_before = Pt(12)
        r_tt = p_table_title.add_run("BẢNG ĐÁP ÁN NHANH TOÀN BỘ ĐỀ THI")
        r_tt.font.name = "Times New Roman"
        r_tt.font.size = Pt(13)
        r_tt.bold = True
        r_tt.font.color.rgb = RGBColor(30, 58, 138)

        # Bảng Phần I: 12 câu
        if p1_answers:
            p_p1 = doc.add_paragraph()
            p_p1.paragraph_format.space_before = Pt(6)
            r = p_p1.add_run("1. PHẦN I (Trắc nghiệm nhiều lựa chọn — 0,25đ/câu):")
            r.font.name = "Times New Roman"
            r.bold = True
            r.font.size = Pt(11)

            t1 = doc.add_table(rows=2, cols=len(p1_answers) + 1)
            t1.alignment = WD_TABLE_ALIGNMENT.CENTER
            _set_table_borders(t1)

            t1.rows[0].cells[0].paragraphs[0].add_run("Câu").bold = True
            t1.rows[1].cells[0].paragraphs[0].add_run("Đ/án").bold = True
            _set_cell_background(t1.rows[0].cells[0], "E2E8F0")
            _set_cell_background(t1.rows[1].cells[0], "E2E8F0")

            for col_idx, (c_name, ans_char) in enumerate(p1_answers, start=1):
                c_num = re.sub(r"[^\d]", "", c_name) or str(col_idx)
                cell_h = t1.rows[0].cells[col_idx]
                cell_v = t1.rows[1].cells[col_idx]
                _set_cell_background(cell_h, "F8FAFC")
                p_h = cell_h.paragraphs[0]
                p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_h.add_run(c_num).bold = True

                p_v = cell_v.paragraphs[0]
                p_v.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r_v = p_v.add_run(ans_char)
                r_v.bold = True
                r_v.font.color.rgb = RGBColor(220, 38, 38)

        # Bảng Phần II: 4 câu Đúng/Sai
        if p2_answers:
            p_p2 = doc.add_paragraph()
            p_p2.paragraph_format.space_before = Pt(8)
            r = p_p2.add_run("2. PHẦN II (Trắc nghiệm Đúng/Sai — 1 ý: 0,1đ; 2 ý: 0,25đ; 3 ý: 0,5đ; 4 ý: 1,0đ):")
            r.font.name = "Times New Roman"
            r.bold = True
            r.font.size = Pt(11)

            t2 = doc.add_table(rows=len(p2_answers) + 1, cols=5)
            t2.alignment = WD_TABLE_ALIGNMENT.CENTER
            _set_table_borders(t2)

            headers_p2 = ["Câu hỏi", "Lệnh hỏi a)", "Lệnh hỏi b)", "Lệnh hỏi c)", "Lệnh hỏi d)"]
            for ci, h_txt in enumerate(headers_p2):
                cell = t2.rows[0].cells[ci]
                _set_cell_background(cell, "E2E8F0")
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.add_run(h_txt).bold = True

            for row_idx, (c_name, sub_d) in enumerate(p2_answers, start=1):
                row = t2.rows[row_idx]
                p0 = row.cells[0].paragraphs[0]
                p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p0.add_run(c_name).bold = True
                _set_cell_background(row.cells[0], "F8FAFC")

                for s_i, s_key in enumerate(["a", "b", "c", "d"], start=1):
                    val = sub_d.get(s_key, "-")
                    cell = row.cells[s_i]
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    r_val = p.add_run(val)
                    r_val.bold = True
                    if val == "Đúng":
                        r_val.font.color.rgb = RGBColor(22, 101, 52)  # Xanh lá
                    elif val == "Sai":
                        r_val.font.color.rgb = RGBColor(220, 38, 38)  # Đỏ

        # Bảng Phần III: 6 câu trả lời ngắn
        if p3_answers:
            p_p3 = doc.add_paragraph()
            p_p3.paragraph_format.space_before = Pt(8)
            r = p_p3.add_run("3. PHẦN III (Trắc nghiệm trả lời ngắn — 0,5đ/câu):")
            r.font.name = "Times New Roman"
            r.bold = True
            r.font.size = Pt(11)

            t3 = doc.add_table(rows=2, cols=len(p3_answers) + 1)
            t3.alignment = WD_TABLE_ALIGNMENT.CENTER
            _set_table_borders(t3)

            t3.rows[0].cells[0].paragraphs[0].add_run("Câu").bold = True
            t3.rows[1].cells[0].paragraphs[0].add_run("Đáp số").bold = True
            _set_cell_background(t3.rows[0].cells[0], "E2E8F0")
            _set_cell_background(t3.rows[1].cells[0], "E2E8F0")

            for col_idx, (c_name, ans_val) in enumerate(p3_answers, start=1):
                c_num = re.sub(r"[^\d]", "", c_name) or str(col_idx)
                cell_h = t3.rows[0].cells[col_idx]
                cell_v = t3.rows[1].cells[col_idx]
                _set_cell_background(cell_h, "F8FAFC")
                p_h = cell_h.paragraphs[0]
                p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_h.add_run(c_num).bold = True

                p_v = cell_v.paragraphs[0]
                p_v.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r_v = p_v.add_run(ans_val)
                r_v.bold = True
                r_v.font.color.rgb = RGBColor(30, 64, 175)

        # Ngăn cách giữa Bảng đáp án và Hướng dẫn giải chi tiết
        p_div = doc.add_paragraph()
        p_div.paragraph_format.space_before = Pt(16)
        r_div = p_div.add_run("HƯỚNG DẪN GIẢI CHI TIẾT TỪNG BÀI TOÁN")
        r_div.font.name = "Times New Roman"
        r_div.font.size = Pt(13)
        r_div.bold = True
        r_div.font.color.rgb = RGBColor(30, 58, 138)

    # -------------------------------------------------------------
    # 3. RENDER TỪNG CÂU HỎI TRONG ĐỀ
    # -------------------------------------------------------------
    current_sec = None
    for q_idx, q in enumerate(questions):
        sec_name = q.get("section", "")
        if sec_name and sec_name != current_sec:
            current_sec = sec_name
            p_sec = doc.add_paragraph()
            p_sec.paragraph_format.space_before = Pt(14)
            p_sec.paragraph_format.space_after = Pt(4)
            r_sec = p_sec.add_run(sec_name.upper())
            r_sec.font.name = "Times New Roman"
            r_sec.font.size = Pt(12)
            r_sec.bold = True
            r_sec.font.color.rgb = RGBColor(30, 58, 138)

        # Khi ở chế độ 'solution_only', không in lại thân đề dài mà chỉ in lời giải
        if mode != "solution_only":
            _render_question_stem(doc, q["title"], q["stem"])

        # Render Lời giải chi tiết (nếu mode là 'exam_and_solution' hoặc 'solution_only')
        if mode in {"exam_and_solution", "solution_only"}:
            sol_text = q.get("solution", "").strip()
            if sol_text:
                if mode == "solution_only":
                    p_sol_h = doc.add_paragraph()
                    p_sol_h.paragraph_format.space_before = Pt(10)
                    p_sol_h.paragraph_format.space_after = Pt(2)
                    r_sh = p_sol_h.add_run(f"★ {q['title']}:")
                    r_sh.font.name = "Times New Roman"
                    r_sh.font.size = Pt(12)
                    r_sh.bold = True
                    r_sh.font.color.rgb = RGBColor(15, 118, 110)

                # Hiển thị từng dòng của lời giải
                sol_lines = sol_text.splitlines()
                s_i = 0
                s_table_lines = []
                s_in_table = False

                while s_i < len(sol_lines):
                    sl = sol_lines[s_i].strip()
                    if sl.startswith("|") and sl.endswith("|") and sl.count("|") >= 2:
                        s_in_table = True
                        s_table_lines.append(sl)
                        s_i += 1
                        continue
                    elif s_in_table:
                        _render_markdown_table(doc, s_table_lines)
                        s_table_lines = []
                        s_in_table = False

                    if not sl:
                        s_i += 1
                        continue

                    # Kiểm tra hình ảnh trong lời giải (![alt](path))
                    sol_img_m = re.search(r"!\[(.*?)\]\((.*?)\)", sl)
                    if sol_img_m:
                        _render_image(doc, sol_img_m.group(2), sol_img_m.group(1))
                        s_i += 1
                        continue

                    # Bỏ dấu gạch đầu dòng '-' nếu nằm ở đầu dòng lời giải cho đẹp
                    clean_sl = re.sub(r"^-\s+", "", sl)

                    p_sol = doc.add_paragraph()
                    p_sol.paragraph_format.left_indent = Inches(0.25)
                    p_sol.paragraph_format.space_before = Pt(1)
                    p_sol.paragraph_format.space_after = Pt(1)
                    _add_inline_formatted(p_sol, clean_sl, font_size=11.5)
                    s_i += 1

                if s_in_table and s_table_lines:
                    _render_markdown_table(doc, s_table_lines)

    # Dòng kết thúc trang
    p_end = doc.add_paragraph()
    p_end.paragraph_format.space_before = Pt(24)
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_end = p_end.add_run("---------- HẾT ----------")
    r_end.font.name = "Times New Roman"
    r_end.font.size = Pt(11)
    r_end.bold = True

    p_note = doc.add_paragraph()
    p_note.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_note = p_note.add_run("(Thí sinh không được sử dụng tài liệu. Cán bộ coi thi không giải thích gì thêm)")
    r_note.font.name = "Times New Roman"
    r_note.font.size = Pt(10)
    r_note.italic = True

    # Lưu file
    if output_path is None:
        output_path = Path("de_xuat.docx")
    output_path.parent.mkdir(exist_ok=True)
    doc.save(str(output_path))
    return output_path
