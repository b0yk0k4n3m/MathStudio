"""
Module: exam_shuffler.py
Hệ thống Trộn & Đảo Đề Thi Toán THPT (Chuẩn THPT 2026 & Công văn 7991/BGDĐT-GDTrH)
- Xáo trộn thứ tự câu hỏi độc lập trong từng PHẦN (Phần I, II, III, IV).
- Hoán vị ngẫu nhiên 4 phương án A, B, C, D của câu hỏi trắc nghiệm Phần I.
- Tự động phát hiện và cập nhật đáp án đúng tương ứng 100% trong lời giải chi tiết.
- Lập Bảng Ma Trận Soi Đáp Án Tổng Hợp (Answer Key Matrix) đa mã đề (101, 102, 103, 104...).
- Xuất bản trọn bộ tài liệu Word (.docx) và đóng gói file .zip tự động.
"""

import copy
import os
import random
import re
import shutil
import zipfile
from pathlib import Path

import docx
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Inches, Pt, RGBColor

from export_docx import export_exam_word

# Regex nhận dạng phương án A, B, C, D
OPT_RE = re.compile(r"^(?:-\s+|\*\s+)?(?:\*\*)?([A-D])(?:\.|\:)\*{0,2}\s*(.*)$")

# Regex nhận dạng mệnh đề Đúng/Sai a), b), c), d)
SUB_RE = re.compile(r"^(?:-\s+|\*\s+)?(?:\*\*)?([a-d])\)\*{0,2}\s*(.*)$")

# Regex trích xuất đáp án trắc nghiệm Phần I
MCQ_ANS_RE = re.compile(r"(?:Đáp án đúng|Đáp án|Chọn)[^A-D\n]*?([A-D])\b", re.IGNORECASE)

# Regex trích xuất đáp án Đúng/Sai Phần II
TF_ANS_RE = re.compile(r"([a-d])\)\s*(?:\*\*)?\s*(Đúng|Sai)\b", re.IGNORECASE)

# Regex trích xuất đáp số ngắn Phần III
SA_ANS_RE = re.compile(
    r"(?:Đáp số|Đáp án đúng|Đáp án|Kết quả)[^\n\w\-+]*[`*]*([A-Za-z0-9_.,/+-]+)",
    re.IGNORECASE,
)


def parse_mcq_options(stem: str) -> tuple[str, dict[str, str], list[str]]:
    """
    Tách nội dung đề bài thành:
    - stem_body: phần văn bản đề bài (không chứa A, B, C, D)
    - options: dict {'A': '...', 'B': '...', 'C': '...', 'D': '...'}
    - raw_lines: danh sách các dòng văn bản không phải phương án
    """
    lines = stem.splitlines()
    body_lines = []
    options = {}

    for line in lines:
        m = OPT_RE.match(line.strip())
        if m:
            options[m.group(1).upper()] = m.group(2).strip()
        else:
            body_lines.append(line)

    stem_body = "\n".join(body_lines).strip()
    return stem_body, options, body_lines


def extract_mcq_answer(solution: str) -> str | None:
    """Trích xuất đáp án đúng (A, B, C hoặc D) từ phần lời giải."""
    if not solution:
        return None
    m = MCQ_ANS_RE.search(solution)
    return m.group(1).upper() if m else None


def extract_tf_answers(solution: str) -> dict[str, str]:
    """Trích xuất kết quả Đúng/Sai của 4 ý a, b, c, d từ lời giải."""
    res = {}
    if not solution:
        return res
    for item in TF_ANS_RE.finditer(solution):
        k = item.group(1).lower()
        v = item.group(2).capitalize()
        if k not in res:
            res[k] = "Đ" if "Đúng" in v else "S"
    return res


def extract_sa_answer(solution: str) -> str | None:
    """Trích xuất đáp số dạng số của Phần III từ lời giải."""
    if not solution:
        return None
    m = SA_ANS_RE.search(solution)
    return m.group(1).strip() if m else None


def shuffle_mcq_question(
    q: dict, rng: random.Random
) -> tuple[dict, str | None, str | None]:
    """
    Xáo trộn 4 phương án A, B, C, D của 1 câu trắc nghiệm Phần I.
    Cập nhật lại đề bài và đáp án đúng trong lời giải.
    Trả về: (câu hỏi mới, đáp án cũ, đáp án mới).
    """
    stem = q["stem"]
    solution = q["solution"]
    stem_body, options, _ = parse_mcq_options(stem)

    # Nếu không nhận diện đủ 4 phương án A, B, C, D thì giữ nguyên
    if len(options) < 4 or not all(k in options for k in ["A", "B", "C", "D"]):
        orig_ans = extract_mcq_answer(solution)
        return copy.deepcopy(q), orig_ans, orig_ans

    orig_ans = extract_mcq_answer(solution) or "A"
    letters = ["A", "B", "C", "D"]

    # Sinh hoán vị ngẫu nhiên của các chữ cái cũ
    perm = list(letters)
    rng.shuffle(perm)

    # perm[i] là phương án cũ sẽ được đặt vào vị trí letters[i]
    new_options = {}
    new_ans = orig_ans

    for i, new_letter in enumerate(letters):
        old_letter = perm[i]
        new_options[new_letter] = options[old_letter]
        if old_letter == orig_ans:
            new_ans = new_letter

    # Tái tạo phần stem với các phương án đã đảo
    new_opt_text = "\n".join(
        [f"- **{let}.** {new_options[let]}" for let in letters]
    )
    new_stem = f"{stem_body}\n\n{new_opt_text}".strip()

    # Cập nhật lời giải với chữ cái đáp án mới
    new_solution = solution
    if solution:

        def _sub_ans(match):
            full = match.group(0)
            st_grp1 = match.start(1) - match.start(0)
            end_grp1 = match.end(1) - match.start(0)
            return full[:st_grp1] + new_ans + full[end_grp1:]

        new_solution = MCQ_ANS_RE.sub(_sub_ans, solution, count=1)

    new_q = copy.deepcopy(q)
    new_q["stem"] = new_stem
    new_q["solution"] = new_solution
    new_q["full_block"] = (
        f"### {new_q['title']}.\n{new_stem}\n\n{new_solution}"
        if new_solution
        else f"### {new_q['title']}.\n{new_stem}"
    )

    return new_q, orig_ans, new_ans


def shuffle_single_exam(
    header_md: str,
    questions: list[dict],
    exam_code: str,
    shuffle_questions: bool = True,
    shuffle_options: bool = True,
    shuffle_tf: bool = False,
    seed: int | None = None,
) -> tuple[str, list[dict], dict]:
    """
    Sinh 1 bản đề thi đảo theo mã đề cụ thể.
    Trả về:
    - new_header_md
    - new_questions (đã đánh số lại từ Câu 1 đến hết)
    - exam_answers: dict tổng hợp đáp án theo từng câu để làm ma trận
    """
    if seed is None:
        try:
            seed = int(re.sub(r"\D", "", exam_code))
        except Exception:
            seed = sum(ord(c) for c in exam_code)

    rng = random.Random(seed)

    # 1. Phân nhóm các câu hỏi theo PHẦN
    # (Đảm bảo câu hỏi thuộc phần nào chỉ đảo trong nội bộ phần đó)
    sections_map: dict[str, list[dict]] = {}
    sec_order: list[str] = []

    for q in questions:
        sec = q.get("section", "PHẦN I").strip()
        if sec not in sections_map:
            sections_map[sec] = []
            sec_order.append(sec)
        sections_map[sec].append(copy.deepcopy(q))

    shuffled_questions: list[dict] = []
    answers_summary: dict = {
        "code": exam_code,
        "mcq": {},  # {1: 'B', 2: 'A', ...}
        "tf": {},  # {13: 'Đ-S-Đ-Đ', ...}
        "sa": {},  # {17: '40', ...}
        "essay": {},  # {23: 'Tự luận'}
    }

    global_q_idx = 1

    for sec in sec_order:
        sec_qs = sections_map[sec]
        sec_upper = sec.upper()

        # A. Xáo trộn thứ tự các câu hỏi trong cùng một phần nếu được bật
        if shuffle_questions:
            rng.shuffle(sec_qs)

        for q_item in sec_qs:
            q_num = global_q_idx
            q_title = f"Câu {q_num}"

            # Xác định loại câu hỏi theo PHẦN
            if (
                "PHẦN I" in sec_upper
                or "MỘT LỰA CHỌN" in sec_upper
                or "LỰA CHỌN" in sec_upper
            ):
                # PHẦN I: Trắc nghiệm 4 lựa chọn
                if shuffle_options:
                    new_q, _, cur_ans = shuffle_mcq_question(q_item, rng)
                else:
                    new_q = copy.deepcopy(q_item)
                    cur_ans = extract_mcq_answer(new_q["solution"])
                answers_summary["mcq"][q_num] = cur_ans or "?"

            elif "PHẦN II" in sec_upper or "ĐÚNG" in sec_upper:
                # PHẦN II: Trắc nghiệm Đúng / Sai
                new_q = copy.deepcopy(q_item)
                tf_dict = extract_tf_answers(new_q["solution"])
                # Định dạng gọn: Đ-S-Đ-Đ
                condensed = "-".join([tf_dict.get(k, "?") for k in ["a", "b", "c", "d"]])
                answers_summary["tf"][q_num] = condensed

            elif "PHẦN III" in sec_upper or "TRẢ LỜI NGẮN" in sec_upper:
                # PHẦN III: Trả lời ngắn
                new_q = copy.deepcopy(q_item)
                cur_sa = extract_sa_answer(new_q["solution"])
                answers_summary["sa"][q_num] = cur_sa or "?"

            else:
                # PHẦN IV: Tự luận (nếu có)
                new_q = copy.deepcopy(q_item)
                answers_summary["essay"][q_num] = "Tự luận"

            # Đổi lại tiêu đề câu hỏi theo số thứ tự mới
            new_q["title"] = q_title
            # Cập nhật số câu trong full_block
            stem = new_q["stem"]
            sol = new_q["solution"]
            new_q["full_block"] = (
                f"### {q_title}.\n{stem}\n\n{sol}"
                if sol
                else f"### {q_title}.\n{stem}"
            )
            shuffled_questions.append(new_q)
            global_q_idx += 1

    # Cập nhật thông tin mã đề trong tiêu đề header_md nếu có
    new_header_md = header_md
    if re.search(r"Mã đề\s*(?:thi)?\s*:\s*\d+", new_header_md, re.IGNORECASE):
        new_header_md = re.sub(
            r"(?i)Mã đề\s*(?:thi)?\s*:\s*\d+",
            f"Mã đề thi: {exam_code}",
            new_header_md,
        )

    return new_header_md, shuffled_questions, answers_summary


def _set_cell_background(cell, fill_hex: str):
    """Đặt màu nền cho một ô trong bảng Word."""
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))


def export_answer_matrix_docx(
    matrix_list: list[dict],
    school_name: str,
    exam_title: str,
    output_path: Path,
) -> Path:
    """
    Xuất file Word (.docx) chứa BẢNG MA TRẬN SOI ĐÁP ÁN TỔNG HỢP cho tất cả các mã đề.
    Chuẩn bảng biểu rõ đẹp, thuận tiện cho giáo viên chấm thi hoặc nạp máy chấm trắc nghiệm.
    """
    doc = Document()

    for sec in doc.sections:
        sec.top_margin = Inches(0.79)
        sec.bottom_margin = Inches(0.79)
        sec.left_margin = Inches(0.79)
        sec.right_margin = Inches(0.79)

    # 1. Header cơ sở giáo dục
    t_head = doc.add_table(rows=1, cols=2)
    t_head.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_l, c_r = t_head.rows[0].cells
    c_l.width = Inches(3.2)
    c_r.width = Inches(3.8)

    p_l = c_l.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_l = p_l.add_run(school_name.upper())
    r_l.font.name = "Times New Roman"
    r_l.font.size = Pt(11)
    r_l.bold = True

    p_r = c_r.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_r1 = p_r.add_run(exam_title.upper() + "\n")
    r_r1.font.name = "Times New Roman"
    r_r1.font.size = Pt(11)
    r_r1.bold = True
    r_r2 = p_r.add_run("BẢNG ĐÁP ÁN TỔNG HỢP CÁC MÃ ĐỀ THI")
    r_r2.font.name = "Times New Roman"
    r_r2.font.size = Pt(10.5)
    r_r2.font.color.rgb = RGBColor(30, 64, 175)
    r_r2.bold = True

    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(8)
    p_div.paragraph_format.space_after = Pt(12)

    codes = [m["code"] for m in matrix_list]

    # -------------------------------------------------------------
    # 2. BẢNG ĐÁP ÁN PHẦN I (TRẮC NGHIỆM 4 LỰA CHỌN)
    # -------------------------------------------------------------
    mcq_keys = sorted(
        list(matrix_list[0].get("mcq", {}).keys()) if matrix_list else []
    )
    if mcq_keys:
        p_p1 = doc.add_paragraph()
        p_p1.paragraph_format.space_before = Pt(6)
        p_p1.paragraph_format.space_after = Pt(4)
        r_p1 = p_p1.add_run(
            "PHẦN I: ĐÁP ÁN TRẮC NGHIỆM NHIỀU LỰA CHỌN (0,25đ / câu)"
        )
        r_p1.font.name = "Times New Roman"
        r_p1.font.size = Pt(12)
        r_p1.bold = True
        r_p1.font.color.rgb = RGBColor(30, 58, 138)

        # Tạo bảng đối chiếu: Cột đầu là Câu, các cột tiếp theo là từng Mã đề
        table_mcq = doc.add_table(rows=len(mcq_keys) + 1, cols=len(codes) + 1)
        table_mcq.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_mcq.autofit = False

        # Header hàng 0
        hdr = table_mcq.rows[0]
        hdr.cells[0].text = "Câu"
        _set_cell_background(hdr.cells[0], "DBEAFE")
        hdr.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr.cells[0].paragraphs[0].runs[0].bold = True
        hdr.cells[0].paragraphs[0].runs[0].font.name = "Times New Roman"

        for c_idx, code in enumerate(codes):
            cell = hdr.cells[c_idx + 1]
            cell.text = f"Mã {code}"
            _set_cell_background(cell, "DBEAFE")
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"

        # Điền đáp án từng câu
        for r_idx, q_num in enumerate(mcq_keys):
            row = table_mcq.rows[r_idx + 1]
            row.cells[0].text = f"Câu {q_num}"
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[0].paragraphs[0].runs[0].font.name = "Times New Roman"
            row.cells[0].paragraphs[0].runs[0].bold = True

            bg_color = "F8FAFC" if r_idx % 2 == 0 else "FFFFFF"
            _set_cell_background(row.cells[0], bg_color)

            for c_idx, m_obj in enumerate(matrix_list):
                ans = m_obj.get("mcq", {}).get(q_num, "")
                cell = row.cells[c_idx + 1]
                cell.text = str(ans)
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                if cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].bold = True
                    cell.paragraphs[0].runs[0].font.name = "Times New Roman"
                    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(
                        29, 78, 216
                    )
                _set_cell_background(cell, bg_color)

    # -------------------------------------------------------------
    # 3. BẢNG ĐÁP ÁN PHẦN II (TRẮC NGHIỆM ĐÚNG / SAI)
    # -------------------------------------------------------------
    tf_keys = sorted(
        list(matrix_list[0].get("tf", {}).keys()) if matrix_list else []
    )
    if tf_keys:
        p_p2 = doc.add_paragraph()
        p_p2.paragraph_format.space_before = Pt(14)
        p_p2.paragraph_format.space_after = Pt(4)
        r_p2 = p_p2.add_run("PHẦN II: ĐÁP ÁN TRẮC NGHIỆM ĐÚNG / SAI")
        r_p2.font.name = "Times New Roman"
        r_p2.font.size = Pt(12)
        r_p2.bold = True
        r_p2.font.color.rgb = RGBColor(6, 95, 70)

        table_tf = doc.add_table(rows=len(tf_keys) + 1, cols=len(codes) + 1)
        table_tf.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_tf.autofit = False

        hdr_tf = table_tf.rows[0]
        hdr_tf.cells[0].text = "Câu hỏi"
        _set_cell_background(hdr_tf.cells[0], "D1FAE5")
        hdr_tf.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_tf.cells[0].paragraphs[0].runs[0].bold = True
        hdr_tf.cells[0].paragraphs[0].runs[0].font.name = "Times New Roman"

        for c_idx, code in enumerate(codes):
            cell = hdr_tf.cells[c_idx + 1]
            cell.text = f"Mã {code} (a - b - c - d)"
            _set_cell_background(cell, "D1FAE5")
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"

        for r_idx, q_num in enumerate(tf_keys):
            row = table_tf.rows[r_idx + 1]
            row.cells[0].text = f"Câu {q_num}"
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[0].paragraphs[0].runs[0].font.name = "Times New Roman"
            row.cells[0].paragraphs[0].runs[0].bold = True

            bg_color = "F0FDF4" if r_idx % 2 == 0 else "FFFFFF"
            _set_cell_background(row.cells[0], bg_color)

            for c_idx, m_obj in enumerate(matrix_list):
                ans = m_obj.get("tf", {}).get(q_num, "")
                cell = row.cells[c_idx + 1]
                cell.text = str(ans)
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                if cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].bold = True
                    cell.paragraphs[0].runs[0].font.name = "Times New Roman"
                _set_cell_background(cell, bg_color)

    # -------------------------------------------------------------
    # 4. BẢNG ĐÁP ÁN PHẦN III (TRẢ LỜI NGẮN)
    # -------------------------------------------------------------
    sa_keys = sorted(
        list(matrix_list[0].get("sa", {}).keys()) if matrix_list else []
    )
    if sa_keys:
        p_p3 = doc.add_paragraph()
        p_p3.paragraph_format.space_before = Pt(14)
        p_p3.paragraph_format.space_after = Pt(4)
        r_p3 = p_p3.add_run("PHẦN III: ĐÁP SỐ TRẢ LỜI NGẮN (0,50đ / câu)")
        r_p3.font.name = "Times New Roman"
        r_p3.font.size = Pt(12)
        r_p3.bold = True
        r_p3.font.color.rgb = RGBColor(146, 64, 14)

        table_sa = doc.add_table(rows=len(sa_keys) + 1, cols=len(codes) + 1)
        table_sa.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_sa.autofit = False

        hdr_sa = table_sa.rows[0]
        hdr_sa.cells[0].text = "Câu"
        _set_cell_background(hdr_sa.cells[0], "FEF3C7")
        hdr_sa.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        hdr_sa.cells[0].paragraphs[0].runs[0].bold = True
        hdr_sa.cells[0].paragraphs[0].runs[0].font.name = "Times New Roman"

        for c_idx, code in enumerate(codes):
            cell = hdr_sa.cells[c_idx + 1]
            cell.text = f"Mã {code}"
            _set_cell_background(cell, "FEF3C7")
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.paragraphs[0].runs[0].bold = True
            cell.paragraphs[0].runs[0].font.name = "Times New Roman"

        for r_idx, q_num in enumerate(sa_keys):
            row = table_sa.rows[r_idx + 1]
            row.cells[0].text = f"Câu {q_num}"
            row.cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            row.cells[0].paragraphs[0].runs[0].font.name = "Times New Roman"
            row.cells[0].paragraphs[0].runs[0].bold = True

            bg_color = "FFFBEB" if r_idx % 2 == 0 else "FFFFFF"
            _set_cell_background(row.cells[0], bg_color)

            for c_idx, m_obj in enumerate(matrix_list):
                ans = m_obj.get("sa", {}).get(q_num, "")
                cell = row.cells[c_idx + 1]
                cell.text = str(ans)
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                if cell.paragraphs[0].runs:
                    cell.paragraphs[0].runs[0].bold = True
                    cell.paragraphs[0].runs[0].font.name = "Times New Roman"
                    cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(
                        180, 83, 9
                    )
                _set_cell_background(cell, bg_color)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    return output_path


def generate_shuffled_package(
    header_md: str,
    questions: list[dict],
    exam_codes: list[str],
    mode: str = "exam_only",  # 'exam_only' | 'exam_and_solution' | 'both'
    school_name: str = "SỞ GIÁO DỤC VÀ ĐÀO TẠO",
    exam_title: str = "ĐỀ THI TỐT NGHIỆP TRUNG HỌC PHỔ THÔNG NĂM 2026",
    shuffle_questions: bool = True,
    shuffle_options: bool = True,
    shuffle_tf: bool = False,
    output_dir: Path | None = None,
    base_filename: str = "de_thi",
) -> dict:
    """
    Tạo trọn bộ các đề thi đảo và bảng ma trận đáp án tổng hợp:
    - Sinh từng file Word theo mã đề.
    - Sinh 1 file Word Bảng Đáp án Tổng hợp.
    - Đóng gói file .zip nén tất cả các file để tải về 1-Click.
    """
    if output_dir is None:
        output_dir = Path("output") / "shuffled"
    output_dir.mkdir(parents=True, exist_ok=True)

    generated_files: list[Path] = []
    matrix_list: list[dict] = []

    # Danh sách các chế độ Word cần xuất
    export_modes = (
        ["exam_only", "exam_and_solution"]
        if mode == "both"
        else [mode]
    )

    for code in exam_codes:
        clean_code = str(code).strip()
        if not clean_code:
            continue

        # Sinh dữ liệu câu hỏi đã xáo trộn
        s_head, s_qs, s_answers = shuffle_single_exam(
            header_md=header_md,
            questions=questions,
            exam_code=clean_code,
            shuffle_questions=shuffle_questions,
            shuffle_options=shuffle_options,
            shuffle_tf=shuffle_tf,
        )
        matrix_list.append(s_answers)

        for m in export_modes:
            prefix = "De_thi" if m == "exam_only" else "De_va_Loi_giai"
            doc_fname = f"{prefix}_{clean_code}_{base_filename[:20]}.docx"
            doc_path = output_dir / doc_fname
            export_exam_word(
                header_md=s_head,
                questions=s_qs,
                mode=m,
                school_name=school_name,
                exam_title=exam_title,
                exam_code=clean_code,
                output_path=doc_path,
            )
            generated_files.append(doc_path)

    # Sinh file Bảng Ma Trận Đáp Án Tổng Hợp
    matrix_fname = f"Bang_Dap_An_Tong_Hop_{len(exam_codes)}_Ma_De.docx"
    matrix_path = output_dir / matrix_fname
    export_answer_matrix_docx(
        matrix_list=matrix_list,
        school_name=school_name,
        exam_title=exam_title,
        output_path=matrix_path,
    )
    generated_files.append(matrix_path)

    # Đóng gói file .ZIP trọn bộ
    zip_fname = f"Tron_Bo_{len(exam_codes)}_Ma_De_{base_filename[:20]}.zip"
    zip_path = output_dir / zip_fname
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in generated_files:
            zf.write(f, arcname=f.name)

    return {
        "zip_path": zip_path,
        "zip_filename": zip_fname,
        "files": generated_files,
        "matrix_path": matrix_path,
        "matrix_list": matrix_list,
        "total_codes": len(exam_codes),
    }
