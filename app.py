import asyncio
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import warnings
from datetime import datetime
from pathlib import Path

warnings.filterwarnings("ignore")

# Vá lỗi [WinError 10054] ConnectionResetError mặc định của asyncio trên Windows khi F5/đóng tab
if sys.platform == "win32":
    try:
        from asyncio.proactor_events import _ProactorBasePipeTransport

        _orig_call_conn_lost = _ProactorBasePipeTransport._call_connection_lost

        def _silent_call_conn_lost(self, *args, **kwargs):
            try:
                _orig_call_conn_lost(self, *args, **kwargs)
            except (ConnectionResetError, OSError):
                pass

        _ProactorBasePipeTransport._call_connection_lost = _silent_call_conn_lost
    except Exception:
        pass

import markdown2
from nicegui import app, ui
from export_docx import export_exam_word
from exam_shuffler import generate_shuffled_package

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_DIR = Path(__file__).resolve().parent
INPUT_DIR = PROJECT_DIR / "input"
BP_IMG_DIR = INPUT_DIR / "blueprint_images"
OUTPUT_DIR = PROJECT_DIR / "output"
HISTORY_DIR = OUTPUT_DIR / "history"
SCRIPTS_DIR = OUTPUT_DIR / "scripts"
INDEX_FILE = OUTPUT_DIR / "exams_index.json"
MATRIX_TEMPLATES_FILE = OUTPUT_DIR / "matrix_templates.json"
BRAIN_DIR = Path.home() / ".gemini" / "antigravity-cli" / "brain"

INPUT_DIR.mkdir(exist_ok=True)
BP_IMG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)
SCRIPTS_DIR.mkdir(exist_ok=True)
(OUTPUT_DIR / "images").mkdir(exist_ok=True)

# Mount thư mục tĩnh để NiceGUI phục vụ hình ảnh đồ thị & hình học
try:
    app.add_static_files("/output", OUTPUT_DIR)
    app.add_static_files("/input", INPUT_DIR)
except Exception:
    pass


def slugify_vn(text: str) -> str:
    """Chuyển chuỗi tiếng Việt có dấu thành tên file không dấu gọn đẹp."""
    s = text.lower().strip()
    s = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", s)
    s = re.sub(r"[èéẹẻẽêềếệểễ]", "e", s)
    s = re.sub(r"[ìíịỉĩ]", "i", s)
    s = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", s)
    s = re.sub(r"[ùúụủũưừứựửữ]", "u", s)
    s = re.sub(r"[ỳýỵỷỹ]", "y", s)
    s = re.sub(r"[đ]", "d", s)
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")[:45] or "bo_de"


# =====================================================================
# CÂY CHUYÊN ĐỀ TOÁN HỌC THPT CHUẨN (TOPIC TREE DATA - GDPT 2018)
# =====================================================================
TOPIC_TREE_DATA = [
    {
        "id": "chap_menh_de_tap_hop",
        "label": "📋 Mệnh đề & Tập hợp",
        "children": [
            {"id": "md_menh_de", "label": "Mệnh đề & Mệnh đề chứa biến"},
            {"id": "md_tap_hop", "label": "Tập hợp và các phép toán trên tập hợp"},
            {"id": "md_sai_so", "label": "Số gần đúng và sai số"},
        ],
    },
    {
        "id": "chap_dai_so_to_hop",
        "label": "🧮 Đại số tổ hợp & Nhị thức Newton",
        "children": [
            {"id": "th_quy_tac_dem", "label": "Quy tắc đếm (Quy tắc cộng & Quy tắc nhân)"},
            {"id": "th_hoan_vi_chinh_hop", "label": "Hoán vị, chỉnh hợp và tổ hợp"},
            {"id": "th_nhi_thuc_newton", "label": "Nhị thức Newton"},
        ],
    },
    {
        "id": "chap_ham_so",
        "label": "📘 Khảo sát hàm số, Đạo hàm & Đồ thị",
        "children": [
            {"id": "hs_don_dieu", "label": "Tính đơn điệu của hàm số (Đồng biến, Nghịch biến)"},
            {"id": "hs_cuc_tri", "label": "Cực trị hàm số (Hàm bậc 3, phân thức, tham số m)"},
            {"id": "hs_gtln_gtnn", "label": "Giá trị lớn nhất và Giá trị nhỏ nhất (GTLN - GTNN)"},
            {"id": "hs_tiem_can", "label": "Đường tiệm cận (Đứng, Ngang & Tiệm cận xiên)"},
            {"id": "hs_do_thi", "label": "Nhận dạng Đồ thị hàm bậc 3, hàm phân thức, hàm f'(x)"},
            {"id": "hs_tuong_giao", "label": "Tương giao đồ thị và số nghiệm phương trình f(x) = m"},
            {"id": "hs_thuc_te", "label": "Bài toán tối ưu hóa kinh tế & đời sống thực tế"},
        ],
    },
    {
        "id": "chap_oxyz",
        "label": "📐 Phương pháp Tọa độ trong Không gian Oxyz",
        "children": [
            {"id": "oxyz_vecto", "label": "Tọa độ điểm, Vectơ, Tích vô hướng & Tích có hướng"},
            {"id": "oxyz_mat_phang", "label": "Phương trình Mặt phẳng (P) & Khoảng cách"},
            {"id": "oxyz_duong_thang", "label": "Phương trình Đường thẳng d & Vị trí tương đối"},
            {"id": "oxyz_mat_cau", "label": "Phương trình Mặt cầu (S), tiếp diện và giao tuyến"},
            {"id": "oxyz_goc_kc", "label": "Góc (đường-mặt, 2 mặt) & Khoảng cách 2 đường chéo nhau"},
            {"id": "oxyz_thuc_te", "label": "Mô hình Oxyz thực tế (Radar, máy bay, kiến trúc)"},
        ],
    },
    {
        "id": "chap_tich_phan",
        "label": "∫ Nguyên hàm, Tích phân & Ứng dụng",
        "children": [
            {"id": "tp_nguyen_ham", "label": "Nguyên hàm & Bảng nguyên hàm hàm số cơ bản"},
            {"id": "tp_xac_dinh", "label": "Tích phân xác định & Tính chất tích phân"},
            {"id": "tp_dien_tich", "label": "Ứng dụng hình học: Tính diện tích hình phẳng"},
            {"id": "tp_the_tich", "label": "Ứng dụng hình học: Thể tích khối tròn xoay & vật thể"},
            {"id": "tp_chuyen_dong", "label": "Bài toán thực tế chuyển động (vận tốc, quãng đường)"},
        ],
    },
    {
        "id": "chap_xac_suat",
        "label": "🎲 Thống kê & Xác suất có điều kiện",
        "children": [
            {"id": "tk_ghep_nhom", "label": "Mẫu số liệu ghép nhóm (Tứ phân vị, Phương sai, Độ lệch chuẩn)"},
            {"id": "xs_dieu_kien", "label": "Xác suất có điều kiện P(A|B)"},
            {"id": "xs_toan_phan_bayes", "label": "Công thức xác suất toàn phần & Công thức Bayes"},
            {"id": "xs_thuc_te", "label": "Bài toán thực tế: Xét nghiệm y tế, tỷ lệ lỗi phân xưởng"},
        ],
    },
    {
        "id": "chap_hhkg",
        "label": "🏛️ Hình học Không gian cổ điển",
        "children": [
            {"id": "hh_goc", "label": "Góc giữa 2 đường thẳng, góc giữa đường thẳng và mặt phẳng"},
            {"id": "hh_nhi_dien", "label": "Góc nhị diện (Góc giữa 2 mặt phẳng)"},
            {"id": "hh_khoang_cach", "label": "Khoảng cách điểm đến mặt phẳng, khoảng cách 2 đường chéo nhau"},
            {"id": "hh_the_tich", "label": "Thể tích khối chóp có cạnh bên vuông góc đáy, khối chóp đều"},
            {"id": "hh_the_tich_lt", "label": "Thể tích khối lăng trụ, hình hộp chữ nhật, hình lập phương"},
            {"id": "hh_tron_xoay", "label": "Khối tròn xoay: Hình nón, hình trụ, mặt cầu"},
        ],
    },
]

ALL_LEAF_IDS = []
ID_TO_LABEL = {}
LABEL_TO_ID = {}
LABEL_TO_CAT = {}
ALL_TOPIC_LABELS = []

for parent in TOPIC_TREE_DATA:
    raw_cat = parent.get("label", "")
    clean_cat = "".join(c for c in raw_cat if ord(c) < 10000 or ord(c) > 130000 or c in " ").strip()
    for ch in parent.get("children", []):
        ALL_LEAF_IDS.append(ch["id"])
        ID_TO_LABEL[ch["id"]] = ch["label"]
        LABEL_TO_ID[ch["label"]] = ch["id"]
        LABEL_TO_CAT[ch["label"]] = clean_cat or raw_cat
        ALL_TOPIC_LABELS.append(ch["label"])


def get_topic_category(topic_name: str) -> str:
    """Trả về tên nhóm/chương của một chuyên đề toán học."""
    if not topic_name:
        return "Chuyên đề"
    if topic_name in LABEL_TO_CAT:
        return LABEL_TO_CAT[topic_name]
    for parent in TOPIC_TREE_DATA:
        raw_cat = parent.get("label", "")
        clean_cat = "".join(c for c in raw_cat if ord(c) < 10000 or ord(c) > 130000 or c in " ").strip()
        for ch in parent.get("children", []):
            if ch.get("label") == topic_name or ch.get("id") == topic_name:
                return clean_cat or raw_cat
    return "Chuyên đề tự chọn"


def load_matrix_templates() -> list[dict]:
    """Tải danh sách các mẫu ma trận đề thi từ file JSON."""
    if MATRIX_TEMPLATES_FILE.exists():
        try:
            data = json.loads(MATRIX_TEMPLATES_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list) and len(data) > 0:
                return data
        except Exception:
            pass
    return []


def save_matrix_templates(templates: list[dict]):
    """Lưu danh sách các mẫu ma trận đề thi vào file JSON."""
    MATRIX_TEMPLATES_FILE.write_text(json.dumps(templates, ensure_ascii=False, indent=2), encoding="utf-8")


def get_default_matrix_sections() -> list[dict]:
    """Khởi tạo danh sách các phần và dòng ma trận câu hỏi mặc định theo mẫu người dùng cung cấp."""
    return [
        {
            "id": "sec_1",
            "title": "Phần 1",
            "subtitle": "Phần 1",
            "type": "Một lựa chọn đúng",
            "rows": [
                {
                    "category": "Mệnh đề và tập hợp",
                    "topic": "Mệnh đề",
                    "nb": 1, "th": 1, "vd": 1, "vdc": 1,
                },
                {
                    "category": "Mệnh đề và tập hợp",
                    "topic": "Tập hợp và các phép toán trên tập hợp",
                    "nb": 1, "th": 1, "vd": 1, "vdc": 1,
                },
                {
                    "category": "Đại số tổ hợp",
                    "topic": "Quy tắc đếm",
                    "nb": 1, "th": 1, "vd": 1, "vdc": 1,
                },
                {
                    "category": "Đại số tổ hợp",
                    "topic": "Hoán vị, chỉnh hợp và tổ hợp",
                    "nb": 0, "th": 2, "vd": 2, "vdc": 0,
                },
                {
                    "category": "Đại số tổ hợp",
                    "topic": "Nhị thức Newton",
                    "nb": 0, "th": 2, "vd": 2, "vdc": 0,
                },
            ],
        },
        {
            "id": "sec_2",
            "title": "Phần 2",
            "subtitle": "Phần 2",
            "type": "Đúng / Sai",
            "rows": [
                {
                    "category": "Mệnh đề và tập hợp",
                    "topic": "Tập hợp và bài toán thực tế",
                    "nb": 0, "th": 1, "vd": 1, "vdc": 0,
                },
                {
                    "category": "Đại số tổ hợp",
                    "topic": "Ứng dụng tổ hợp xác suất trong đời sống",
                    "nb": 0, "th": 0, "vd": 1, "vdc": 1,
                },
            ],
        },
        {
            "id": "sec_3",
            "title": "Phần 3",
            "subtitle": "Phần 3",
            "type": "Trả lời ngắn",
            "rows": [
                {
                    "category": "Đại số tổ hợp",
                    "topic": "Bài toán đếm và tổ hợp nâng cao",
                    "nb": 0, "th": 0, "vd": 2, "vdc": 2,
                },
                {
                    "category": "Mệnh đề và tập hợp",
                    "topic": "Tập hợp số và bài toán chứa tham số m",
                    "nb": 0, "th": 0, "vd": 1, "vdc": 1,
                },
            ],
        },
    ]

# Danh mục các Ý tưởng dạng toán phổ biến gợi ý (Quick-Pick Idea Chips)
QUESTION_IDEA_PRESETS = [
    ("📈 Đồ thị hàm bậc 3", "Đồ thị hàm số bậc ba y = ax^3 + bx^2 + cx + d (nhận dạng dấu hệ số a, c, d, cực trị)"),
    ("📐 Tiệm cận xiên (bậc 2/1)", "Đồ thị hàm phân thức bậc 2 trên bậc 1 y = (ax^2+bx+c)/(px+q) có tiệm cận xiên và tiệm cận đứng"),
    ("⚡ Tiệm cận đứng & ngang", "Đồ thị hàm nhất biến y = (ax+b)/(cx+d) có tiệm cận đứng và tiệm cận ngang"),
    ("📊 Đồ thị đạo hàm f'(x)", "Cho đồ thị hàm số đạo hàm y = f'(x), tìm số điểm cực trị hoặc khoảng đơn điệu của f(x)"),
    ("🎯 Min - Max trên đoạn", "Tìm giá trị lớn nhất và giá trị nhỏ nhất của hàm số trên đoạn [a; b]"),
    ("🔀 Tương giao f(x) = m", "Tương giao đồ thị: Biện luận số nghiệm phương trình f(x) = m theo tham số m"),
    ("🏛️ Chóp SA vuông đáy", "Hình chóp S.ABCD có đáy là hình vuông, SA vuông góc mặt phẳng đáy, tính góc hoặc thể tích"),
    ("💎 Chóp tứ giác đều", "Hình chóp tứ giác đều S.ABCD có cạnh đáy a, cạnh bên 2a, tính thể tích hoặc khoảng cách"),
    ("📦 Lăng trụ đứng tam giác", "Hình lăng trụ đứng ABC.A'B'C' có đáy tam giác vuông, tính khoảng cách giữa 2 đường thẳng chéo nhau"),
    ("✈️ Mô hình Oxyz Radar", "Mô hình thực tế Oxyz: Xác định tọa độ máy bay hoặc trạm radar phát hiện tàu thuyền ngoài khơi"),
    ("🌐 Phương trình Mặt phẳng", "Viết phương trình mặt phẳng (P) đi qua 3 điểm hoặc tiếp xúc với mặt cầu"),
    ("⚪ Phương trình Mặt cầu", "Viết phương trình mặt cầu (S) có tâm I và tiếp xúc mặt phẳng (P)"),
    ("📏 Khoảng cách trong Oxyz", "Tính khoảng cách từ điểm M đến đường thẳng d hoặc mặt phẳng (P)"),
    ("∫ Diện tích hình phẳng", "Tính diện tích hình phẳng giới hạn bởi đường cong parabol và đường thẳng"),
    ("🛢️ Thể tích khối tròn xoay", "Tính thể tích khối tròn xoay tạo thành khi quay hình phẳng quanh trục Ox"),
    ("🏎️ Chuyển động vận tốc v(t)", "Bài toán thực tế chuyển động: Cho hàm vận tốc v(t), tính quãng đường đi được s(t)"),
    ("🎲 Mẫu số liệu Tứ phân vị", "Khoảng biến thiên và khoảng tứ phân vị Delta_Q của mẫu số liệu ghép nhóm"),
    ("📊 Độ lệch chuẩn ghép nhóm", "Tính phương sai và độ lệch chuẩn của mẫu số liệu ghép nhóm thống kê"),
    ("🏥 Xác suất Bayes Y tế", "Ứng dụng công thức Bayes trong xét nghiệm y tế chẩn đoán bệnh"),
    ("🏭 Xác suất Toàn phần Xưởng", "Ứng dụng công thức xác suất toàn phần tính tỷ lệ sản phẩm lỗi của 2 phân xưởng"),
    ("🏢 Tối ưu hóa chi phí thực tế", "Bài toán tối ưu hóa bằng đạo hàm: Thiết kế chi phí sản xuất hoặc diện tích nguyên vật liệu nhỏ nhất"),
]

# Các Mẫu cấu trúc Đề thi nhanh 1-Click
EXAM_PRESETS_DATA = {
    "chuan_2026": {
        "title": "Chuẩn Tốt nghiệp THPT 2026",
        "badge": "22 câu • 90p",
        "desc": "Cấu trúc chuẩn Bộ GD&ĐT: 12 MCQ + 4 TF + 6 SA (Thang 10đ)",
        "mcq": 12, "tf": 4, "sa": 6, "duration": 90,
        "topic": "Tổng hợp chuẩn 5 chuyên đề GDPT 2018 (Hàm số, Oxyz, Tích phân, Xác suất, HHKG)",
        "selected_tree": list(ALL_LEAF_IDS),
    },
    "dothi_hamso": {
        "title": "Chuyên đề Đồ thị & Hàm số",
        "badge": "15 câu • 60p",
        "desc": "Đồ thị bậc 3, Tiệm cận xiên, Cực trị, Min-Max, Tương giao, Ứng dụng thực tế",
        "mcq": 8, "tf": 3, "sa": 4, "duration": 60,
        "topic": "Chuyên đề Đồ thị, Tiệm cận & Ứng dụng Khảo sát sự biến thiên của Hàm số (Toán 12)",
        "selected_tree": [t for t in ALL_LEAF_IDS if t.startswith("hs_")],
    },
    "hinh_hoc_oxyz": {
        "title": "Chuyên đề Hình học & Oxyz",
        "badge": "15 câu • 60p",
        "desc": "Hình học Không gian cổ điển (chóp, lăng trụ) & Phương pháp Tọa độ Oxyz",
        "mcq": 8, "tf": 3, "sa": 4, "duration": 60,
        "topic": "Chuyên đề Hình học Không gian cổ điển & Phương pháp Tọa độ trong Không gian Oxyz",
        "selected_tree": [t for t in ALL_LEAF_IDS if t.startswith("oxyz_") or t.startswith("hh_")],
    },
    "xac_suat_thong_ke": {
        "title": "Chuyên đề Xác suất & Thống kê",
        "badge": "10 câu • 45p",
        "desc": "Xác suất có điều kiện, Công thức Bayes & Mẫu số liệu ghép nhóm",
        "mcq": 6, "tf": 2, "sa": 2, "duration": 45,
        "topic": "Chuyên đề Xác suất có điều kiện, Công thức Bayes & Thống kê Mẫu số liệu ghép nhóm",
        "selected_tree": [t for t in ALL_LEAF_IDS if t.startswith("xs_") or t.startswith("tk_")],
    },
    "giua_ky_1": {
        "title": "Kiểm tra Giữa Học kỳ 1",
        "badge": "11 câu • 45p",
        "desc": "Nửa đầu HK1: Khảo sát hàm số & Khối đa diện không gian (6 MCQ + 2 TF + 3 SA)",
        "mcq": 6, "tf": 2, "sa": 3, "duration": 45,
        "topic": "Kiểm tra Giữa Học kỳ 1: Đạo hàm & Khảo sát hàm số, Khối đa diện không gian",
        "selected_tree": [t for t in ALL_LEAF_IDS if t.startswith("hs_") or t.startswith("hh_the_tich")],
    },
}


def _read_index_json() -> dict[str, dict]:
    if INDEX_FILE.exists():
        try:
            return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _write_index_json(data: dict[str, dict]):
    INDEX_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def sync_and_list_exams() -> list[dict]:
    """Đồng bộ toàn bộ các file .md trong output/ với file quản lý exams_index.json."""
    idx_data = _read_index_json()
    md_files = sorted(
        [f for f in OUTPUT_DIR.glob("*.md") if not f.name.startswith("temp_")],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    changed = False
    active_names = {f.name for f in md_files}

    # Xóa các mục không còn file trên ổ đĩa
    for k in list(idx_data.keys()):
        if k not in active_names:
            del idx_data[k]
            changed = True

    result = []
    for i, f in enumerate(md_files):
        raw = f.read_text(encoding="utf-8", errors="replace")
        header_md, qs = parse_exam_markdown(raw)
        q_count = len(qs)
        mtime_str = datetime.fromtimestamp(f.stat().st_mtime).strftime("%d/%m/%Y %H:%M")

        meta = idx_data.get(f.name, {})
        if not meta.get("title"):
            # Tự động lấy tiêu đề từ dòng # đầu tiên hoặc tên file
            first_line = header_md.splitlines()[0].lstrip("# ").strip() if header_md else ""
            if first_line and len(first_line) < 90:
                meta["title"] = first_line
            else:
                meta["title"] = f"Bộ đề: {f.stem}"
            changed = True

        meta["filename"] = f.name
        meta["path"] = str(f)
        meta["question_count"] = q_count
        meta["updated_at"] = mtime_str
        meta.setdefault("grade", "Toán 12 - THPT 2026")
        meta.setdefault("topic", "Tổng hợp")
        idx_data[f.name] = meta
        result.append(meta)

    if changed:
        _write_index_json(idx_data)
    return result


def register_exam_metadata(
    file_path: Path, title: str = "", grade: str = "", topic: str = ""
):
    idx_data = _read_index_json()
    entry = idx_data.get(file_path.name, {})
    if title:
        entry["title"] = title.strip()
    if grade:
        entry["grade"] = grade
    if topic:
        entry["topic"] = topic
    entry["updated_at"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    idx_data[file_path.name] = entry
    _write_index_json(idx_data)

    # Lưu bản sao verify_math.py riêng cho bộ đề này
    verify_src = PROJECT_DIR / "verify_math.py"
    if verify_src.exists():
        shutil.copy2(verify_src, SCRIPTS_DIR / f"{file_path.stem}_verify.py")


def create_unique_exam_file(title: str) -> tuple[Path, str]:
    """Tạo đường dẫn file .md mới không trùng lặp cho Bộ đề mới."""
    existing = [f for f in OUTPUT_DIR.glob("*.md") if not f.name.startswith("temp_")]
    next_idx = len(existing) + 1
    clean_title = title.strip() or f"Đề số {next_idx:02d} - THPT 2026"
    slug = slugify_vn(clean_title)
    ts = datetime.now().strftime("%H%M")
    fname = f"de_{next_idx:02d}_{slug[:28]}_{ts}.md"
    return OUTPUT_DIR / fname, clean_title


def find_antigravity_ide() -> str | None:
    local_programs = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs"
    candidates = [
        shutil.which("antigravity-ide"),
        str(local_programs / "Antigravity IDE" / "bin" / "antigravity-ide.cmd"),
        str(local_programs / "Antigravity IDE" / "Antigravity IDE.exe"),
        str(local_programs / "antigravity" / "Antigravity.exe"),
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    return None


AGY_CLI_PATH = shutil.which("agy")
AGY_IDE_PATH = find_antigravity_ide()


# =====================================================================
# BỘ CHUYỂN ĐỔI MARKDOWN + LATEX (BẢO VỆ CÔNG THỨC TOÁN 100%)
# =====================================================================
def md_to_math_html(md_text: str, is_solution: bool = False) -> str:
    """
    Chuyển Markdown sang HTML nhưng giữ nguyên 100% các khối công thức $$...$$ và $...$
    - Khi is_solution=False: nếu các phương án A, B, C, D ngắn gọn thì xếp lưới 4 cột; nếu mệnh đề dài (Đúng/Sai) thì xếp 1 cột dọc.
    - Khi is_solution=True: trình bày từng bước lời giải theo chiều dọc rõ ràng, không chia cột ngang.
    """
    if not md_text:
        return ""

    cleaned = md_text.strip()
    if is_solution:
        # Bỏ dòng tiêu đề thừa '**Lời giải:**' ở đầu khung lời giải vì đã có Header của khung
        cleaned = re.sub(r"(?mi)^(?:\*\*Lời giải:?\*\*|Lời giải:?)\s*\n*", "", cleaned).strip()

    math_store: list[str] = []

    def _save_math(match: re.Match) -> str:
        idx = len(math_store)
        math_store.append(html.escape(match.group(0)))
        return f"MATHPLACEHOLDER{idx}END"

    # Bảo vệ $$...$$ trước, sau đó đến $...$
    protected = re.sub(r"\$\$[\s\S]*?\$\$", _save_math, cleaned)
    protected = re.sub(r"\$(?!\$)[^\n\$]+?\$", _save_math, protected)

    rendered = markdown2.markdown(
        protected,
        extras=[
            "tables",
            "fenced-code-blocks",
            "cuddled-lists",
            "break-on-newline",
            "strike",
            "target-blank-links",
        ],
    )

    # Chuẩn hóa đường dẫn ảnh tương đối để hiển thị ngay trong NiceGUI Live Preview
    rendered = re.sub(r'src="(?:\./)?output/', 'src="/output/', rendered)
    rendered = re.sub(r'src="(?:\./)?input/', 'src="/input/', rendered)

    for idx, m_html in enumerate(math_store):
        rendered = rendered.replace(f"MATHPLACEHOLDER{idx}END", m_html)

    if is_solution:
        wrapper_cls = "math-prose solution-prose"
    else:
        # Kiểm tra độ dài dòng của các ý lựa chọn: nếu có ý dài > 65 ký tự (như Đúng/Sai a, b, c, d) thì xếp 1 cột dọc
        list_items = re.findall(r"(?m)^-\s+(.+)$", cleaned)
        has_long_option = any(len(item) > 65 for item in list_items)
        wrapper_cls = "math-prose stem-list" if has_long_option else "math-prose stem-grid"

    return f'<div class="{wrapper_cls}">{rendered}</div>'


def trigger_mathjax():
    ui.run_javascript("if (window.renderAllMathNow) { window.renderAllMathNow(); }")


# =====================================================================
# BỘ PHÂN TÍCH ĐỀ TOÁN THÔNG MINH (HỖ TRỢ CẢ LỜI GIẢI GỘP & LỜI GIẢI CUỐI ĐỀ)
# =====================================================================
def parse_exam_markdown(md_text: str) -> tuple[str, list[dict]]:
    """
    Tách nội dung file Markdown đề toán thành danh sách các câu hỏi độc lập.
    Tự động ghép lời giải ở phần '## LỜI GIẢI CHI TIẾT' cuối đề (nếu có) vào đúng từng câu.
    """
    if not md_text.strip():
        return "", []

    # Tách riêng khu vực BẢNG ĐÁP ÁN / LỜI GIẢI CHI TIẾT ở cuối file (nếu có)
    sol_section_match = re.search(
        r"(?mi)^##\s+(?:BẢNG ĐÁP ÁN|LỜI GIẢI CHI TIẾT).*$", md_text
    )
    if sol_section_match:
        main_part = md_text[: sol_section_match.start()].strip()
        tail_part = md_text[sol_section_match.start() :].strip()
    else:
        main_part = md_text.strip()
        tail_part = ""

    # Trích xuất các lời giải nằm ở cuối đề (nếu có) theo (Phần, Câu)
    external_solutions: list[str] = []
    if tail_part:
        detail_match = re.search(r"(?mi)^##\s+LỜI GIẢI CHI TIẾT.*$", tail_part)
        detail_text = tail_part[detail_match.start() :] if detail_match else tail_part
        sol_q_matches = list(
            re.finditer(r"(?m)^####\s+(Câu\s+\d+[^\n]*)$", detail_text)
        )
        for idx, sm in enumerate(sol_q_matches):
            s_start = sm.start()
            s_end = (
                sol_q_matches[idx + 1].start()
                if idx + 1 < len(sol_q_matches)
                else len(detail_text)
            )
            sol_chunk = detail_text[s_start:s_end].strip()
            # Cắt bỏ dòng tiêu đề ### PHẦN tiếp theo nếu dính vào cuối câu
            sol_chunk = re.sub(r"(?m)^---\s*\n+###\s+PHẦN[\s\S]*$", "", sol_chunk).strip()
            sol_chunk = re.sub(r"(?m)^###\s+PHẦN[\s\S]*$", "", sol_chunk).strip()
            external_solutions.append(sol_chunk)

    # Tìm tất cả các câu hỏi trong phần đề chính
    q_pattern = re.compile(r"(?m)^###\s+(Câu\s+\d+[^\n]*)$")
    q_matches = list(q_pattern.finditer(main_part))
    if not q_matches:
        return md_text.strip(), []

    # Xác định Phần (Phần I, Phần II, Phần III) của từng câu
    sec_matches = list(re.finditer(r"(?m)^##\s+(PHẦN\s+[I|V|X|\d]+[^\n]*)$", main_part))
    header_end = sec_matches[0].start() if sec_matches else q_matches[0].start()
    header_text = main_part[:header_end].strip()

    questions: list[dict] = []
    inline_sol_pattern = re.compile(
        r"(?mi)^(?:#{1,4}\s*|\*\*|- )?(?:Lời giải|Hướng dẫn giải|Đáp án chi tiết)\s*:?"
    )

    for i, qm in enumerate(q_matches):
        q_start = qm.start()
        q_end = q_matches[i + 1].start() if i + 1 < len(q_matches) else len(main_part)

        # Tìm xem câu này thuộc PHẦN nào
        current_section = ""
        for sm in sec_matches:
            if sm.start() < q_start:
                current_section = sm.group(1).strip()

        raw_block = main_part[q_start:q_end].strip()
        # Loại bỏ tiêu đề ## PHẦN của phần kế tiếp nếu nằm ở cuối raw_block
        raw_block = re.sub(r"(?m)^---\s*\n+##\s+PHẦN[\s\S]*$", "", raw_block).strip()
        raw_block = re.sub(r"(?m)^##\s+PHẦN[\s\S]*$", "", raw_block).strip()
        raw_block = re.sub(r"(?m)^---\s*$", "", raw_block).strip()

        lines = raw_block.splitlines()
        title_line = qm.group(1).strip().rstrip(".")
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        # Kiểm tra lời giải nội tuyến (inline) hoặc lời giải cuối đề
        inl_match = inline_sol_pattern.search(body)
        if inl_match:
            stem = body[: inl_match.start()].strip()
            solution = body[inl_match.start() :].strip()
        else:
            stem = body
            solution = external_solutions[i] if i < len(external_solutions) else ""

        full_combined = f"### {title_line}\n{stem}"
        if solution:
            if not inline_sol_pattern.match(solution):
                full_combined += f"\n\n**Lời giải:**\n{solution}"
            else:
                full_combined += f"\n\n{solution}"

        questions.append(
            {
                "index": i,
                "section": current_section,
                "title": title_line,
                "stem": stem,
                "solution": solution,
                "full_block": full_combined,
            }
        )

    return header_text, questions


def rebuild_exam_markdown(header_text: str, questions: list[dict]) -> str:
    """Ghép danh sách câu hỏi thành file Markdown chuẩn."""
    parts: list[str] = []
    if header_text.strip():
        parts.append(header_text.strip())

    current_sec = None
    sec_counter = 0
    for idx, q in enumerate(questions):
        sec = q.get("section", "")
        if sec and sec != current_sec:
            current_sec = sec
            sec_counter = 1
            parts.append(f"## {sec}")
        else:
            sec_counter = (sec_counter + 1) if current_sec else (idx + 1)

        block = q["full_block"].strip()
        # Chuẩn hóa tiêu đề ### Câu X
        num_to_use = sec_counter if current_sec else (idx + 1)
        block = re.sub(
            r"(?m)^###\s+Câu\s+\d+[^\n]*",
            f"### Câu {num_to_use}.",
            block,
            count=1,
        )
        parts.append(block)

    return "\n\n---\n\n".join(parts) + "\n"


def save_version_backup(out_file: Path, label: str = "backup"):
    if out_file.exists():
        ts = datetime.now().strftime("%H%M%S")
        backup_file = HISTORY_DIR / f"{out_file.stem}_{ts}_{label}.md"
        backup_file.write_text(out_file.read_text(encoding="utf-8"), encoding="utf-8")


def list_backups(out_file: Path) -> list[Path]:
    return sorted(
        HISTORY_DIR.glob(f"{out_file.stem}_*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def format_tool_call_vn(tc: dict) -> str:
    name = tc.get("name", "")
    args = tc.get("args", {})
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except Exception:
            args = {}
    if name == "read_file":
        p = str(args.get("Path", "")).strip('"')
        return f"📖 Đọc file `{Path(p).name if p else p}`"
    elif name == "write_file":
        p = str(args.get("Path", "")).strip('"')
        return f"📝 Ghi file `{Path(p).name if p else p}`"
    elif name == "edit_file":
        p = str(args.get("Path", "")).strip('"')
        return f"✏️ Chỉnh sửa file `{Path(p).name if p else p}`"
    elif name == "run_command":
        cmd = str(args.get("CommandLine", "")).strip('"')
        return f"💻 Chạy lệnh `{cmd}`"
    elif name == "call_mcp_tool":
        raw_args = str(args.get("Arguments", ""))
        if "verify_single.py" in raw_args:
            return "📐 Thẩm định toán học & tính toán nghiệm câu hỏi"
        if "verify_math.py" in raw_args:
            return "📐 Kiểm tra tính đúng đắn toán học toàn bộ đề thi"
        return f"🔧 Xử lý công cụ tính toán..."
    return f"🛠️ Gọi `{name}`"


def find_newest_transcript(started_after: float) -> Path | None:
    if not BRAIN_DIR.exists():
        return None
    candidates = []
    for t_file in BRAIN_DIR.glob("*/.system_generated/logs/transcript.jsonl"):
        try:
            mtime = t_file.stat().st_mtime
            if mtime >= started_after - 2.0:
                candidates.append((mtime, t_file))
        except OSError:
            pass
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[0], reverse=True)
    return candidates[0][1]


# =====================================================================
# GIAO DIỆN CHÍNH NICEGUI (SINGLE-PAGE APP, KHÔNG NHÁY TRANG)
# =====================================================================
@ui.page("/")
def main_page():
    ui.add_head_html(
        """
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
        <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
        <script>
        window.renderAllMathNow = function() {
            if (typeof renderMathInElement === 'function') {
                document.querySelectorAll('.math-prose').forEach(function(el) {
                    renderMathInElement(el, {
                        delimiters: [
                            {left: '$$', right: '$$', display: true},
                            {left: '$', right: '$', display: false},
                            {left: '\\\\(', right: '\\\\)', display: false},
                            {left: '\\\\[', right: '\\\\]', display: true}
                        ],
                        throwOnError: false
                    });
                });
            }
        };
        document.addEventListener("DOMContentLoaded", function() {
            setTimeout(window.renderAllMathNow, 150);
            setTimeout(window.renderAllMathNow, 500);
            var obs = new MutationObserver(function(mutations) {
                var shouldRender = false;
                for (var i = 0; i < mutations.length; i++) {
                    if (mutations[i].addedNodes.length > 0) {
                        shouldRender = true;
                        break;
                    }
                }
                if (shouldRender) {
                    setTimeout(window.renderAllMathNow, 30);
                }
            });
            obs.observe(document.body, { childList: true, subtree: true });
        });
        </script>
        <style>
        body {
            background-color: #f8fafc;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        .math-prose {
            font-size: 0.98rem;
            line-height: 1.65;
            color: #1e293b;
        }
        .math-prose h1 {
            font-size: 1.25rem !important;
            line-height: 1.4 !important;
            font-weight: 700 !important;
            color: #1e3a8a !important;
            margin: 0 0 0.35rem 0 !important;
            letter-spacing: normal !important;
        }
        .math-prose h2 {
            font-size: 1.1rem !important;
            line-height: 1.4 !important;
            font-weight: 700 !important;
            color: #1e40af !important;
            margin: 0.4rem 0 0.3rem 0 !important;
        }
        .math-prose h3, .math-prose h4 {
            font-size: 1rem !important;
            line-height: 1.4 !important;
            font-weight: 600 !important;
            color: #0f172a !important;
            margin: 0.3rem 0 0.25rem 0 !important;
        }
        .math-prose p {
            margin-bottom: 0.45rem;
        }
        .math-prose hr {
            margin: 0.5rem 0;
            border: 0;
            border-top: 1px solid #e2e8f0;
        }
        .stem-grid ul {
            list-style-type: none;
            padding-left: 0;
            margin-top: 0.55rem;
            margin-bottom: 0.25rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 0.5rem;
        }
        .stem-grid li {
            padding: 0.45rem 0.75rem;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }
        .stem-list ul {
            list-style-type: none;
            padding-left: 0;
            margin-top: 0.55rem;
            margin-bottom: 0.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }
        .stem-list li {
            padding: 0.5rem 0.85rem;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
        }
        .solution-prose ul {
            list-style-type: none;
            padding-left: 0;
            margin-top: 0.35rem;
            margin-bottom: 0.2rem;
            display: flex;
            flex-direction: column;
            gap: 0.45rem;
        }
        .solution-prose li {
            padding: 0.5rem 0.85rem;
            background: rgba(255, 255, 255, 0.85);
            border-left: 3px solid #10b981;
            border-radius: 0 8px 8px 0;
            overflow-x: auto;
        }
        .solution-prose .katex-display {
            margin: 0.4rem 0 !important;
            overflow-x: auto;
            overflow-y: hidden;
        }
        .math-prose table {
            border-collapse: collapse;
            width: 100%;
            margin: 0.75rem 0;
        }
        .math-prose th, .math-prose td {
            border: 1px solid #cbd5e1;
            padding: 0.45rem 0.75rem;
            text-align: center;
        }
        .math-prose th {
            background-color: #f1f5f9;
            font-weight: 600;
        }
        </style>
        """
    )

    exams_init = sync_and_list_exams()
    default_active_file = exams_init[0]["path"] if exams_init else str(OUTPUT_DIR / "de_ma_tran.md")

    matrix_templates_list = load_matrix_templates()
    active_tpl = matrix_templates_list[0] if matrix_templates_list else None

    state = {
        "active_file": default_active_file,
        "save_as_new": True,
        "save_clone_as_new": True,
        "last_conv_id": None,
        "exec_mode": "live",  # live | ide | terminal
        "is_running": False,
        "open_solutions": set(),
        "editing_idx": None,
        "exam_preset": "Chuẩn Tốt nghiệp THPT 2026 (22 câu - 90p)",
        "active_matrix_id": active_tpl["id"] if active_tpl else "mat_chuan_thpt_2026",
        "active_matrix_title": active_tpl["title"] if active_tpl else "Chuẩn Tốt nghiệp THPT 2026 (Bộ GD&ĐT)",
        "grade": active_tpl.get("grade", "Toán 12 - Tốt nghiệp THPT 2026") if active_tpl else "Toán 12 - Tốt nghiệp THPT 2026",
        "topic": "Tổng hợp chuẩn 5 chuyên đề GDPT 2018",
        "duration": active_tpl.get("duration", 90) if active_tpl else 90,
        "mcq": 12,
        "tf": 4,
        "sa": 6,
        "num_clone": 5,
        "clone_type": "Thay số liệu (Giữ nguyên dạng toán, số đẹp)",
        "uploaded_image": (INPUT_DIR / "cau_mau.png").exists(),
        "blueprint_items": [],
        "card_ideas": {},
        "selected_topics": list(active_tpl.get("selected_topics", [])) if active_tpl else [],
        "matrix_sections": json.loads(json.dumps(active_tpl.get("sections", []))) if active_tpl else get_default_matrix_sections(),
    }

    # -----------------------------------------------------------------
    # HỘP THOẠI KIỂM TRA ĐÁP SỐ TOÁN HỌC (verify_single.py & verify_math.py)
    # -----------------------------------------------------------------
    sympy_dialog = ui.dialog()
    sympy_modal_state = {"target": "verify_single.py"}
    with sympy_dialog, ui.card().classes("w-[860px] max-w-[95vw] p-5 rounded-2xl"):
        with ui.row().classes("w-full items-center justify-between mb-2"):
            ui.label("📐 Công cụ Thẩm định & Kiểm tra Đáp án").classes(
                "text-lg font-bold text-slate-800"
            )
            ui.button(icon="close", on_click=sympy_dialog.close).props("flat round dense")

        def load_sympy_file(fname: str):
            sympy_modal_state["target"] = fname
            fpath = PROJECT_DIR / fname
            if fpath.exists():
                sympy_editor.value = fpath.read_text(encoding="utf-8")
            else:
                sympy_editor.value = f"# Chưa có mã nguồn kiểm tra {fname}\n"

        with ui.row().classes("w-full gap-2 mb-2"):
            ui.button(
                "🎯 Kiểm định câu đơn (verify_single)",
                on_click=lambda: load_sympy_file("verify_single.py"),
                color="indigo-50",
            ).props("unelevated no-caps size=sm").classes("text-indigo-900 font-semibold")
            ui.button(
                "📋 Kiểm định toàn bộ đề (verify_math)",
                on_click=lambda: load_sympy_file("verify_math.py"),
                color="slate-100",
            ).props("unelevated no-caps size=sm").classes("text-slate-700 font-semibold")

        sympy_editor = ui.codemirror(language="Python", theme="vscodeLight").classes(
            "w-full h-80 border rounded-lg"
        )
        sympy_output = ui.code("", language="text").classes("w-full max-h-48 overflow-auto hidden")

        async def run_sympy_script():
            fname = sympy_modal_state["target"]
            verify_path = PROJECT_DIR / fname
            verify_path.write_text(sympy_editor.value, encoding="utf-8")
            sympy_output.classes(remove="hidden")
            sympy_output.set_content(f"⏳ Đang chạy thẩm định...")
            proc = await asyncio.create_subprocess_exec(
                "python",
                fname,
                cwd=str(PROJECT_DIR),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            out_b, err_b = await proc.communicate()
            out_txt = out_b.decode("utf-8", errors="replace")
            err_txt = err_b.decode("utf-8", errors="replace")
            if proc.returncode == 0:
                ui.notify(f"Kiểm tra thành công (Exit Code: 0)!", type="positive")
                sympy_output.set_content(f"✅ KẾT QUẢ KIỂM ĐỊNH THÀNH CÔNG (Exit Code: 0):\n{out_txt}")
            else:
                ui.notify(f"Phát hiện lỗi kiểm định (Exit Code: {proc.returncode})", type="negative")
                sympy_output.set_content(f"❌ KẾT QUẢ KIỂM ĐỊNH (Exit Code: {proc.returncode}):\n{err_txt}\n{out_txt}")

        with ui.row().classes("w-full justify-end gap-2 mt-3"):
            ui.button(
                "▶️ Lưu & Chạy kiểm tra đáp án",
                on_click=run_sympy_script,
                color="emerald",
            ).classes("px-4 font-semibold")

    def open_sympy_modal():
        if (PROJECT_DIR / "verify_single.py").exists():
            load_sympy_file("verify_single.py")
        else:
            load_sympy_file("verify_math.py")
        sympy_output.classes(add="hidden")
        sympy_dialog.open()

    # -----------------------------------------------------------------
    # HỘP THOẠI GIỚI THIỆU SẢN PHẨM & TÁC GIẢ (MODULE GIỚI THIỆU)
    # -----------------------------------------------------------------
    about_dialog = ui.dialog()
    with about_dialog, ui.card().classes(
        "w-[880px] max-w-[95vw] p-6 rounded-2xl shadow-xl border border-slate-200 gap-4"
    ):
        with ui.row().classes("w-full items-center justify-between pb-3 border-b border-slate-100"):
            with ui.row().classes("items-center gap-3"):
                ui.icon("school", size="32px").classes("text-blue-700")
                with ui.column().classes("gap-0"):
                    ui.label("Giới thiệu Math Studio").classes("text-xl font-bold text-slate-900")
                    ui.label("Hệ Thống Biên Soạn & Thẩm Định Đề Thi Toán THPT Chuẩn 2026").classes(
                        "text-xs text-slate-500 font-medium"
                    )
            ui.button(icon="close", on_click=about_dialog.close).props("flat round dense")

        with ui.tabs().classes("w-full text-sm font-semibold") as about_sub_tabs:
            at_prod = ui.tab("🌟 Giới thiệu Sản phẩm")
            at_author = ui.tab("👨‍🏫 Tác giả & Định hướng")
            at_format = ui.tab("📊 Chuẩn Đề THPT 2026 & CV 7991")

        with ui.tab_panels(about_sub_tabs, value=at_prod).classes("w-full p-1"):
            # TAB 1: SẢN PHẨM
            with ui.tab_panel(at_prod).classes("p-0 gap-4 flex flex-col"):
                with ui.card().classes(
                    "w-full p-4 rounded-xl bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200"
                ):
                    with ui.row().classes("items-center justify-between w-full"):
                        with ui.column().classes("gap-1"):
                            ui.label("Math Studio - Nền tảng Biên soạn & Thẩm định Đề Toán").classes(
                                "text-base font-bold text-blue-900"
                            )
                            ui.label(
                                "Tích hợp đồng thời Chuẩn Đề Tốt nghiệp THPT 2026 và Chuẩn Kiểm tra Định kỳ Công văn 7991/BGDĐT-GDTrH."
                            ).classes("text-xs text-slate-700")
                        ui.badge("GDPT 2018 - CV 7991", color="blue-700").classes("text-xs px-3 py-1 font-bold")

                with ui.grid(columns=2).classes("w-full gap-3"):
                    features = [
                        (
                            "🎯 Chuẩn hóa Ma trận GDPT 2018 & CV 7991",
                            "Tự động xây dựng đề bám sát tuyệt đối ma trận năng lực theo 3 mức độ: Biết, Hiểu, Vận dụng và xuất Khung Ma trận (PL1) - Bản đặc tả (PL2).",
                        ),
                        (
                            "📐 Thẩm định Toán học Độc lập",
                            "Giải nghiệm hình thức tự động, triệt tiêu rủi ro nhầm lẫn, nghiệm vô lý hoặc đáp án trùng lặp trong các mã đề.",
                        ),
                        (
                            "📊 Dựng Đồ thị & Hình học Sư phạm",
                            "Tự động mô phỏng và vẽ đồ thị hàm số, khối chóp, lăng trụ theo đúng chuẩn mực sư phạm (nét liền, nét đứt, nhãn đỉnh).",
                        ),
                        (
                            "📝 Xuất Microsoft Word Bản địa (OMML)",
                            "Tạo file .docx với công thức toán học có thể nhấp đúp chỉnh sửa trực tiếp, hỗ trợ đảo đề, bảng đáp án và ma trận chi tiết.",
                        ),
                    ]
                    for f_title, f_desc in features:
                        with ui.card().classes("p-3.5 rounded-xl border border-slate-200 bg-white gap-1 shadow-xs"):
                            ui.label(f_title).classes("text-sm font-bold text-slate-800")
                            ui.label(f_desc).classes("text-xs text-slate-600 leading-relaxed")

            # TAB 2: TÁC GIẢ & ĐỊNH HƯỚNG
            with ui.tab_panel(at_author).classes("p-0 gap-4 flex flex-col"):
                with ui.card().classes("w-full p-4 rounded-xl border border-slate-200 bg-white gap-3 shadow-xs"):
                    with ui.row().classes("items-center gap-3 pb-3 border-b border-slate-100"):
                        ui.avatar("person", color="primary", text_color="white", size="48px")
                        with ui.column().classes("gap-0.5"):
                            ui.label("Tác giả: Nguyễn Minh Trung").classes("text-base font-bold text-slate-900")
                            ui.label("Nghiên cứu & Phát triển Công nghệ Giáo dục (EdTech)").classes(
                                "text-xs text-blue-700 font-semibold"
                            )
                            ui.label("Email liên hệ: minhtrung.mis@gmail.com").classes(
                                "text-xs text-slate-500 font-mono"
                            )

                    ui.label("💡 Sứ mệnh & Mục đích Phát triển:").classes(
                        "text-xs font-bold text-slate-700 uppercase tracking-wide mt-1"
                    )
                    ui.label(
                        "Math Studio được phát triển với tâm huyết đồng hành cùng quý thầy cô giáo viên, tổ chuyên môn và học sinh "
                        "trên cả nước trong quá trình đổi mới căn bản, toàn diện giáo dục theo Chương trình GDPT 2018. "
                        "Hệ thống giúp tiết kiệm hàng chục giờ đồng hồ soạn thảo, chuẩn hóa quy trình ra đề theo Công văn 7991/BGDĐT-GDTrH, "
                        "tự động hóa khâu vẽ hình, thẩm định tính đúng đắn toán học và xuất bản văn bản Word chuyên nghiệp."
                    ).classes("text-xs text-slate-700 leading-relaxed text-justify")

                    with ui.row().classes(
                        "w-full items-center justify-between p-3 rounded-xl bg-slate-50 border border-slate-200 mt-1"
                    ):
                        with ui.column().classes("gap-0"):
                            ui.label("Bản quyền & Ứng dụng").classes("text-xs font-bold text-slate-800")
                            ui.label("Phục vụ mục đích nghiên cứu, giảng dạy và học tập môn Toán THPT.").classes(
                                "text-[11px] text-slate-500"
                            )
                        ui.badge("Bản quyền © 2026", color="slate-200").classes("text-slate-700 text-xs font-bold")

            # TAB 3: CẤU TRÚC ĐỀ THPT 2026 & CÔNG VĂN 7991
            with ui.tab_panel(at_format).classes("p-0 gap-3 flex flex-col"):
                with ui.tabs().classes("w-full text-xs font-bold") as sub_fmt_tabs:
                    ft_7991 = ui.tab("📋 Đề Định Kỳ CV 7991 (70% TN + 30% TL)")
                    ft_2026 = ui.tab("🎓 Đề Tốt Nghiệp THPT 2026 (100% TN)")

                with ui.tab_panels(sub_fmt_tabs, value=ft_7991).classes("w-full p-0 mt-2"):
                    # SUB-PANEL 1: CÔNG VĂN 7991/BGDĐT-GDTrH
                    with ui.tab_panel(ft_7991).classes("p-0 gap-2.5 flex flex-col"):
                        with ui.card().classes("w-full p-3 rounded-xl border border-indigo-200 bg-indigo-50/70 gap-1"):
                            ui.label("Chuẩn Công văn 7991/BGDĐT-GDTrH ngày 17/12/2024 (Áp dụng từ HK2 năm học 2024-2025)").classes(
                                "text-xs font-bold text-indigo-900"
                            )
                            ui.label(
                                "Cấu trúc kết hợp: 70% Trắc nghiệm (7.0đ) + 30% Tự luận (3.0đ) | 90 phút | Bắt buộc Khung Ma trận (PL1) & Bản đặc tả (PL2)"
                            ).classes("text-[11px] text-slate-700 font-medium")

                        cv_parts = [
                            ("PHẦN I: Trắc nghiệm Nhiều lựa chọn", "12 câu • 3.0 điểm (0.25đ / câu)", "Mỗi câu 4 phương án chọn 1 đúng. Đánh giá mức độ Biết và Hiểu."),
                            ("PHẦN II: Trắc nghiệm Đúng / Sai", "2 câu • 2.0 điểm (Tối đa 1.0đ / câu)", "Mỗi câu gồm 4 ý a,b,c,d theo thang nhận thức. Đúng 1 ý: 0.1đ; 2 ý: 0.25đ; 3 ý: 0.5đ; 4 ý: 1.0đ."),
                            ("PHẦN III: Trắc nghiệm Trả lời ngắn", "4 câu • 2.0 điểm (0.50đ / câu)", "Thí sinh tự tính toán và điền đáp số gọn gàng. Đánh giá mức độ Hiểu và Vận dụng."),
                            ("PHẦN IV: Tự luận", "2 - 3 bài toán • 3.0 điểm", "Trình bày các bước lập luận, giải toán chi tiết, mô hình hóa toán học giải quyết vấn đề thực tiễn."),
                        ]
                        for p_n, p_s, p_d in cv_parts:
                            with ui.card().classes("p-2.5 rounded-xl border border-slate-200 bg-white gap-0.5"):
                                with ui.row().classes("items-center justify-between w-full"):
                                    ui.label(p_n).classes("text-xs font-bold text-slate-900")
                                    ui.badge(p_s, color="indigo-100").classes("text-indigo-800 text-[10px] font-semibold")
                                ui.label(p_d).classes("text-[11px] text-slate-600 leading-snug")

                    # SUB-PANEL 2: ĐỀ TỐT NGHIỆP THPT 2026
                    with ui.tab_panel(ft_2026).classes("p-0 gap-2.5 flex flex-col"):
                        with ui.card().classes("w-full p-3 rounded-xl border border-blue-200 bg-blue-50/70 gap-1"):
                            ui.label("Chuẩn Đề thi Tốt nghiệp THPT từ năm 2025 - 2026 (Bộ GD&ĐT)").classes(
                                "text-xs font-bold text-blue-900"
                            )
                            ui.label("Cấu trúc: 100% Trắc nghiệm khách quan | 22 câu | 10.00 điểm | 90 phút").classes(
                                "text-[11px] text-slate-700 font-medium"
                            )

                        parts_info = [
                            ("PHẦN I: Trắc nghiệm Nhiều lựa chọn", "12 câu • 3.0 điểm (0.25đ / câu)", "Mỗi câu 4 phương án chọn 1 đúng. Đánh giá năng lực Nhận biết và Thông hiểu."),
                            ("PHẦN II: Trắc nghiệm Đúng / Sai", "4 câu • 4.0 điểm (Tối đa 1.0đ / câu)", "Mỗi câu gồm 4 ý a,b,c,d. Điểm lũy tiến: Đúng 1 ý: 0.1đ; 2 ý: 0.25đ; 3 ý: 0.5đ; 4 ý: 1.0đ."),
                            ("PHẦN III: Trắc nghiệm Trả lời ngắn", "6 câu • 3.0 điểm (0.50đ / câu)", "Thí sinh tự tính toán và điền kết quả dạng số (nguyên hoặc thập phân tối đa 4 ký tự)."),
                        ]
                        for p_name, p_pts, p_desc in parts_info:
                            with ui.card().classes("p-2.5 rounded-xl border border-slate-200 bg-white gap-0.5"):
                                with ui.row().classes("items-center justify-between w-full"):
                                    ui.label(p_name).classes("text-xs font-bold text-slate-900")
                                    ui.badge(p_pts, color="blue-100").classes("text-blue-800 text-[10px] font-semibold")
                                ui.label(p_desc).classes("text-[11px] text-slate-600 leading-snug")

    # -----------------------------------------------------------------
    # HỘP THOẠI CÂY CHUYÊN ĐỀ RIÊNG BIỆT (MODAL DIALOG - TOPIC TREE)
    # -----------------------------------------------------------------
    tree_dialog = ui.dialog()
    tree_dialog_container = None
    new_chap_input_state = {"name": ""}

    # -----------------------------------------------------------------
    # HÀM TÍNH TOÁN TÓM TẮT MA TRẬN ĐỀ THI
    # -----------------------------------------------------------------
    def calc_matrix_summary(sections=None):
        if sections is None:
            sections = state.get("matrix_sections", [])
        total_q = 0
        p1_q, p2_q, p3_q, p4_q = 0, 0, 0, 0
        total_nb, total_th, total_vd, total_vdc = 0, 0, 0, 0

        for sec in sections:
            sec_type = sec.get("type", "Một lựa chọn đúng")
            s_nb = sum(int(r.get("nb") or 0) for r in sec.get("rows", []))
            s_th = sum(int(r.get("th") or 0) for r in sec.get("rows", []))
            s_vd = sum(int(r.get("vd") or 0) for r in sec.get("rows", []))
            s_vdc = sum(int(r.get("vdc") or 0) for r in sec.get("rows", []))
            s_tot = s_nb + s_th + s_vd + s_vdc
            total_q += s_tot
            total_nb += s_nb
            total_th += s_th
            total_vd += s_vd
            total_vdc += s_vdc

            if "Một lựa chọn" in sec_type:
                p1_q += s_tot
            elif "Đúng" in sec_type:
                p2_q += s_tot
            elif "Tự luận" in sec_type:
                p4_q += s_tot
            else:
                p3_q += s_tot

        if sections is state.get("matrix_sections"):
            state["mcq"] = p1_q
            state["tf"] = p2_q
            state["sa"] = p3_q
            state["essay"] = p4_q
        points = p1_q * 0.25 + p2_q * 1.0 + p3_q * 0.5 + p4_q * 1.5
        return {
            "total_q": total_q,
            "p1_q": p1_q,
            "p2_q": p2_q,
            "p3_q": p3_q,
            "p4_q": p4_q,
            "points": points,
            "nb": total_nb,
            "th": total_th,
            "vd": total_vd,
            "vdc": total_vdc,
        }
    # -----------------------------------------------------------------
    with ui.header().classes(
        "bg-gradient-to-r from-blue-900 via-indigo-800 to-blue-700 text-white shadow-md px-6 py-3 items-center justify-between"
    ):
        with ui.row().classes("items-center gap-3"):
            ui.icon("calculate", size="32px").classes("text-blue-200")
            with ui.column().classes("gap-0"):
                ui.label("Math Studio").classes("text-xl font-bold tracking-tight")
                ui.label("Hệ thống Biên soạn Đề thi, Tinh chỉnh Câu hỏi & Kiểm định Tự động").classes(
                    "text-xs text-blue-200"
                )

        with ui.row().classes("items-center gap-2"):
            ui.button(
                "ℹ️ Giới thiệu",
                on_click=lambda: about_dialog.open(),
                color="white",
            ).props("outline size=sm").classes("text-white font-semibold")
            ui.button(
                "📐 Kiểm định Toán",
                on_click=open_sympy_modal,
                color="white",
            ).props("outline size=sm").classes("text-white font-semibold")

    # -----------------------------------------------------------------
    # BANNER THEO DÕI TIẾN ĐỘ AI TRỰC TIẾP (LIVE STREAM)
    # -----------------------------------------------------------------
    live_banner = ui.card().classes(
        "w-full max-w-[1440px] mx-auto mt-4 p-4 rounded-2xl border-2 border-blue-400 bg-blue-50/90 shadow-md hidden"
    )
    with live_banner:
        with ui.row().classes("w-full items-center justify-between"):
            with ui.row().classes("items-center gap-3"):
                ui.spinner("dots", size="lg", color="primary")
                live_title_lbl = ui.label("🤖 AI đang xử lý yêu cầu...").classes(
                    "text-base font-bold text-blue-900"
                )
            with ui.row().classes("items-center gap-4"):
                live_step_badge = ui.badge("Bước: 0", color="blue").classes("text-xs px-2.5 py-1")
                live_time_badge = ui.badge("0.0s", color="indigo").classes("text-xs px-2.5 py-1")
                live_sympy_badge = ui.badge("Kiểm định: Chờ", color="amber").classes(
                    "text-xs px-2.5 py-1"
                )

        live_thinking_lbl = ui.label("Đang khởi tạo phiên làm việc và phân tích đề bài...").classes(
            "text-sm text-slate-700 italic bg-white/80 p-2.5 rounded-lg border border-blue-200 w-full mt-2"
        )
        live_feed_col = ui.column().classes("w-full gap-1 mt-2 max-h-36 overflow-y-auto")

    # -----------------------------------------------------------------
    # BỐ CỤC 2 CỘT CHÍNH
    # -----------------------------------------------------------------
    with ui.row().classes("w-full max-w-[1440px] mx-auto px-4 py-4 gap-6 items-start no-wrap"):

        # =============================================================
        # CỘT TRÁI: BẢNG ĐIỀU KHIỂN TẠO ĐỀ & CÂY CHUYÊN ĐỀ (400px)
        # =============================================================
        with ui.column().classes("w-[400px] shrink-0 gap-4"):
            with ui.card().classes("w-full p-4 rounded-2xl shadow-sm border border-slate-200 bg-white"):
                with ui.row().classes("w-full items-center justify-between mb-1"):
                    with ui.row().classes("items-center gap-2"):
                        ui.icon("tune", size="22px").classes("text-blue-700")
                        ui.label("Thiết lập Ma trận & Đề thi").classes("text-base font-bold text-slate-800")
                    ui.badge("GDPT 2018", color="blue-100").classes("text-blue-800 text-[11px] font-bold px-2 py-0.5 rounded-full")

                with ui.tabs().classes("w-full text-xs font-semibold mt-1") as left_tabs:
                    t_matrix = ui.tab("🎯 Ma trận Đề thi")
                    t_clone = ui.tab("📸 Từ Ảnh mẫu")
                    t_about = ui.tab("ℹ️ Giới thiệu")

                with ui.tab_panels(left_tabs, value=t_matrix).classes("w-full p-0 mt-3"):
                    # ---------------------------------------------------------
                    # TAB 1: MA TRẬN & ĐỀ MẪU
                    # ---------------------------------------------------------
                    with ui.tab_panel(t_matrix).classes("p-0 gap-3 flex flex-col"):
                        # Thẻ Ma trận Đang Sử Dụng
                        with ui.card().classes("w-full p-3.5 rounded-2xl bg-gradient-to-br from-blue-50/90 to-indigo-50/90 border border-blue-200 gap-2.5 shadow-xs"):
                            with ui.row().classes("w-full items-start justify-between no-wrap gap-2"):
                                with ui.column().classes("gap-0.5 flex-1"):
                                    with ui.row().classes("items-center gap-1.5"):
                                        ui.icon("table_chart", size="18px").classes("text-blue-700")
                                        ui.label("Ma trận Đang Sử Dụng:").classes("text-xs font-bold text-blue-900 uppercase tracking-wide")
                                    active_matrix_title_lbl = ui.label(state.get("active_matrix_title", "Ma trận Chuẩn THPT 2026")).classes("text-sm font-bold text-slate-900 leading-snug")
                                matrix_total_badge = ui.badge("22 câu • 10.00đ", color="blue-700").classes("text-[10px] font-bold px-2 py-0.5 rounded-md shrink-0")

                            matrix_overview_container = ui.column().classes("w-full gap-1 text-xs text-slate-700 pt-1 border-t border-blue-100")

                            def render_matrix_overview():
                                matrix_overview_container.clear()
                                stats = calc_matrix_summary()
                                active_matrix_title_lbl.set_text(state.get("active_matrix_title", "Ma trận Đề thi"))
                                matrix_total_badge.set_text(f"{stats['total_q']} câu • {stats['points']:.2f}đ")
                                with matrix_overview_container:
                                    for s_idx, sec in enumerate(state.get("matrix_sections", [])):
                                        s_nb = sum(int(r.get("nb") or 0) for r in sec.get("rows", []))
                                        s_th = sum(int(r.get("th") or 0) for r in sec.get("rows", []))
                                        s_vd = sum(int(r.get("vd") or 0) for r in sec.get("rows", []))
                                        s_vdc = sum(int(r.get("vdc") or 0) for r in sec.get("rows", []))
                                        s_tot = s_nb + s_th + s_vd + s_vdc
                                        pts = s_tot * 0.25 if "Một lựa chọn" in sec.get("type", "") else (s_tot * 1.0 if "Đúng" in sec.get("type", "") else (s_tot * 1.5 if "Tự luận" in sec.get("type", "") else s_tot * 0.5))
                                        with ui.row().classes("w-full items-center justify-between py-0.5 border-b border-blue-50 last:border-0"):
                                            ui.label(f"• {sec.get('title', 'Phần')} ({sec.get('type', '')}):").classes("font-semibold text-slate-800 truncate max-w-[210px]")
                                            ui.label(f"{len(sec.get('rows', []))} CĐ | {s_tot} câu ({pts:.2f}đ)").classes("font-mono text-[11px] text-blue-800")

                            render_matrix_overview()

                            # 3 Nút bấm Thao tác Ma trận Đề thi
                            with ui.column().classes("w-full gap-1.5 mt-1"):
                                ui.button(
                                    "📋 Quản lý Danh sách Ma trận Đề thi",
                                    on_click=lambda: open_matrix_list_dialog(),
                                    color="blue-700",
                                ).props("unelevated no-caps").classes(
                                    "w-full py-2 text-white font-bold rounded-xl shadow-xs hover:bg-blue-800"
                                )

                                with ui.row().classes("w-full gap-2"):
                                    ui.button(
                                        "➕ Tạo Ma trận Mới",
                                        on_click=lambda: start_new_matrix_wizard(),
                                        color="emerald-600",
                                    ).props("unelevated no-caps size=sm").classes(
                                        "flex-1 py-1.5 text-white font-bold rounded-xl shadow-xs hover:bg-emerald-700"
                                    ).tooltip("Quy trình 2 bước: Tick chọn chuyên đề -> Thiết lập combobox số câu & dạng bài")

                                    ui.button(
                                        "📊 Sửa Ma trận Này",
                                        on_click=lambda: edit_current_matrix_wizard(),
                                        color="white",
                                    ).props("outline no-caps size=sm").classes(
                                        "flex-1 py-1.5 text-blue-900 border-blue-300 font-semibold rounded-xl hover:bg-blue-50"
                                    )

                        # Thời gian làm bài
                        with ui.card().classes("w-full p-2.5 rounded-xl bg-white border border-slate-200"):
                            with ui.row().classes("w-full items-center justify-between"):
                                ui.label("⏱️ Thời gian làm bài:").classes("text-xs font-semibold text-slate-800")
                                with ui.row().classes("items-center gap-1.5"):
                                    ui.button("-15", on_click=lambda: (state.update({"duration": max(15, int(state['duration']) - 15)}), update_matrix_ui())).props("flat dense size=sm").classes("px-1.5 py-0.5 rounded-md bg-slate-100 hover:bg-slate-200 text-xs font-semibold")
                                    dur_lbl = ui.label(f"{state['duration']} phút").classes("text-xs font-bold text-indigo-700 w-16 text-center")
                                    ui.button("+15", on_click=lambda: (state.update({"duration": min(180, int(state['duration']) + 15)}), update_matrix_ui())).props("flat dense size=sm").classes("px-1.5 py-0.5 rounded-md bg-slate-100 hover:bg-slate-200 text-xs font-semibold")

                        # Nút mở Kịch bản Blueprint
                        ui.button(
                            "🎯 Thiết lập Kịch bản từng câu (Gợi ý 1-Click)",
                            on_click=lambda: open_blueprint_modal(),
                            color="indigo-50",
                        ).props("unelevated no-caps").classes(
                            "w-full py-2 text-indigo-800 font-bold rounded-xl border border-indigo-200 hover:bg-indigo-100"
                        )

                        ui.checkbox(
                            "Tạo thành Bộ đề mới (Không ghi đè đề cũ)",
                            value=True,
                        ).bind_value(state, "save_as_new").classes("text-xs text-indigo-900 font-semibold")

                        def update_matrix_ui():
                            dur_lbl.set_text(f"{state['duration']} phút")
                            render_matrix_overview()

                        def update_score_summary():
                            update_matrix_ui()

                        def format_matrix_prompt_detail():
                            lines = []
                            stats = calc_matrix_summary()
                            lines.append(f"TỔNG CỘNG ĐỀ THI: {stats['total_q']} câu | Thang điểm 10 ({stats['points']:.2f} điểm)")
                            lines.append(f"Mức độ toàn đề: Nhận biết: {stats['nb']} câu, Thông hiểu: {stats['th']} câu, Vận dụng: {stats['vd']} câu, Vận dụng cao: {stats['vdc']} câu.\n")
                            for s_idx, sec in enumerate(state.get("matrix_sections", [])):
                                s_nb = sum(int(r.get("nb") or 0) for r in sec.get("rows", []))
                                s_th = sum(int(r.get("th") or 0) for r in sec.get("rows", []))
                                s_vd = sum(int(r.get("vd") or 0) for r in sec.get("rows", []))
                                s_vdc = sum(int(r.get("vdc") or 0) for r in sec.get("rows", []))
                                s_tot = s_nb + s_th + s_vd + s_vdc
                                sec_title = sec.get("title", f"Phần {s_idx+1}")
                                sec_sub = sec.get("subtitle", "")
                                sec_type = sec.get("type", "Một lựa chọn đúng")
                                lines.append(f"### {sec_title}. {sec_sub} (Hình thức: {sec_type} - Tổng {s_tot} câu):")
                                for r in sec.get("rows", []):
                                    c_nb = int(r.get("nb") or 0)
                                    c_th = int(r.get("th") or 0)
                                    c_vd = int(r.get("vd") or 0)
                                    c_vdc = int(r.get("vdc") or 0)
                                    c_tot = c_nb + c_th + c_vd + c_vdc
                                    cat = r.get("category", "")
                                    top = r.get("topic", "")
                                    breakdown = []
                                    if c_nb > 0: breakdown.append(f"{c_nb} câu Nhận biết")
                                    if c_th > 0: breakdown.append(f"{c_th} câu Thông hiểu")
                                    if c_vd > 0: breakdown.append(f"{c_vd} câu Vận dụng")
                                    if c_vdc > 0: breakdown.append(f"{c_vdc} câu Vận dụng cao")
                                    bd_str = ", ".join(breakdown) if breakdown else "Tự chọn mức độ"
                                    note = r.get("note", "").strip()
                                    note_str = f" [Yêu cầu/Dạng câu riêng: {note}]" if note else ""
                                    lines.append(f"  - Chủ đề '{top}' (Nhóm: {cat}): Tổng {c_tot} câu [{bd_str}]{note_str}")
                                lines.append(f"  * Tổng kết {sec_title}: NB: {s_nb}, TH: {s_th}, VD: {s_vd}, VDC: {s_vdc}.\n")
                            return "\n".join(lines)

                        async def on_generate_matrix():
                            stats = calc_matrix_summary()
                            total_q = stats["total_q"]
                            if total_q == 0:
                                ui.notify("Vui lòng thiết lập ít nhất 1 câu hỏi trong ma trận đề!", type="warning")
                                return

                            matrix_detail_text = format_matrix_prompt_detail()
                            topic_clean = state.get("active_matrix_title", "").strip() or state.get("topic", "").strip() or "Tổng hợp"
                            exam_title = f"{topic_clean}"
                            if state.get("save_as_new", True):
                                out_f, auto_title = create_unique_exam_file(exam_title)
                            else:
                                out_f = Path(state["active_file"]) if state.get("active_file") else OUTPUT_DIR / "de_ma_tran.md"

                            state["active_file"] = str(out_f)
                            bp_lines = []
                            for item in state.get("blueprint_items", []):
                                idea_txt = item.get("idea", "").strip()
                                lvl_txt = item.get("level", "Thông hiểu")
                                img_info = ""
                                if item.get("image") and Path(item["image"]).exists():
                                    try:
                                        img_rel = Path(item["image"]).relative_to(PROJECT_DIR).as_posix()
                                    except Exception:
                                        img_rel = Path(item["image"]).as_posix()
                                    img_info = f" [KÈM ẢNH MINH HỌA/Ý TƯỞNG: `{img_rel}` — Bắt buộc dùng read_file đọc file ảnh này để bám sát mô hình/đồ thị/hình vẽ tương ứng]"

                                if idea_txt:
                                    bp_lines.append(
                                        f"  + {item['part']} - {item['label']} [Mức độ: {lvl_txt}]: {idea_txt}{img_info}"
                                    )
                                elif img_info:
                                    bp_lines.append(
                                        f"  + {item['part']} - {item['label']} [Mức độ: {lvl_txt}]: Thiết kế câu toán bám sát hình ảnh ý tưởng đính kèm.{img_info}"
                                    )

                            bp_section = (
                                "KỊCH BẢN Ý TƯỞNG RIÊNG CHO TỪNG CÂU (BẮT BUỘC TUÂN THỦ):\n"
                                + "\n".join(bp_lines)
                                + "\n\n"
                                if bp_lines
                                else ""
                            )
                            prompt = (
                                f"Tạo đề thi chuẩn cấu trúc Tốt nghiệp THPT 2026 ({state['grade']}) theo ĐÚNG BẢNG MA TRẬN CHI TIẾT SAU ĐÂY:\n\n"
                                f"--- BẢNG MA TRẬN ĐỀ THI BẮT BUỘC TUÂN THỦ TỪNG CHUYÊN ĐỀ VÀ MỨC ĐỘ ---\n"
                                f"{matrix_detail_text}\n"
                                f"----------------------------------------------------------------------\n\n"
                                f"Thời gian làm bài: {state['duration']} phút | Tổng số câu: {total_q} câu | Tổng điểm: {stats['points']:.2f} điểm.\n\n"
                                f"{bp_section}"
                                f"YÊU CẦU ĐỊNH DẠNG VÀ PHƯƠNG PHÁP BẮT BUỘC:\n"
                                f"1. Chia các phần đúng theo ma trận trên (PHẦN I, PHẦN II, PHẦN III,...).\n"
                                f"2. Đối với dạng trắc nghiệm Đúng / Sai: Mỗi câu lớn là một bài toán mạch lạc gồm 4 ý a), b), c), d) theo tiến trình tư duy giải toán.\n"
                                f"3. Số liệu bài toán phải đẹp, nghiệm nguyên hoặc phân số gọn gàng.\n"
                                f"4. Mỗi câu bắt đầu bằng tiêu đề `### Câu 1.`, `### Câu 2.`, ...\n"
                                f"5. Ngay dưới mỗi câu có dòng `**Lời giải:**` trình bày đáp án đúng và lời giải chi tiết của câu đó.\n"
                                f"6. Viết code Python SymPy vào `verify_math.py` và chạy kiểm chứng đáp án từng câu.\n"
                                f"7. Lưu đề hoàn chỉnh vào `{out_f.as_posix()}`."
                            )
                            await execute_ai_task(prompt, out_f, f"Đang tạo đề theo ma trận ({total_q} câu)...")

                        ui.button(
                            "🚀 Tạo Đề Theo Ma Trận Này & Kiểm Định",
                            on_click=on_generate_matrix,
                            color="primary",
                        ).classes("w-full py-2.5 font-bold rounded-xl mt-1 shadow-md")

                    # ---------------------------------------------------------
                    # TAB 2: TỪ ẢNH MẪU
                    # ---------------------------------------------------------
                    with ui.tab_panel(t_clone).classes("p-0 gap-3 flex flex-col"):
                        img_preview = ui.image().classes("w-full rounded-lg border hidden max-h-44 object-contain")
                        if (INPUT_DIR / "cau_mau.png").exists():
                            img_preview.set_source(str(INPUT_DIR / "cau_mau.png"))
                            img_preview.classes(remove="hidden")

                        def handle_upload(e):
                            target_img = INPUT_DIR / "cau_mau.png"
                            target_img.write_bytes(e.content.read())
                            state["uploaded_image"] = True
                            img_preview.set_source(str(target_img))
                            img_preview.force_reload()
                            img_preview.classes(remove="hidden")
                            ui.notify("Đã tải ảnh câu mẫu lên!", type="positive")

                        ui.upload(
                            label="Tải ảnh câu toán mẫu (PNG/JPG)",
                            on_upload=handle_upload,
                            auto_upload=True,
                        ).props("accept=.png,.jpg,.jpeg flat bordered").classes("w-full")

                        ui.number("Số câu tương tự cần tạo", value=5, min=1, max=15).bind_value(
                            state, "num_clone"
                        ).classes("w-full")

                        ui.select(
                            [
                                "Thay số liệu (Giữ nguyên dạng toán, số đẹp)",
                                "Đổi hàm số tương đương",
                                "Phát triển lên Vận dụng cao",
                            ],
                            label="Mức độ biến đổi",
                            value=state["clone_type"],
                        ).bind_value(state, "clone_type").classes("w-full")

                        ui.checkbox(
                            "Tạo thành Bộ đề mới (Không ghi đè đề cũ)",
                            value=True,
                        ).bind_value(state, "save_clone_as_new").classes("text-xs text-indigo-900 font-semibold")

                        async def on_generate_clone():
                            if not (INPUT_DIR / "cau_mau.png").exists():
                                ui.notify("Hãy tải ảnh câu mẫu lên trước!", type="warning")
                                return
                            if state.get("save_clone_as_new", True):
                                out_f, auto_title = create_unique_exam_file("Đề nhân bản từ ảnh mẫu")
                            else:
                                out_f = OUTPUT_DIR / "de_nhan_ban.md"
                            state["active_file"] = str(out_f)
                            prompt = (
                                f"Đọc ảnh câu toán tại input/cau_mau.png.\n"
                                f"Tạo {int(state['num_clone'])} câu tương tự theo kiểu '{state['clone_type']}'.\n"
                                f"Mỗi câu bắt đầu bằng `### Câu 1.`, `### Câu 2.` và có `**Lời giải:**` ngay bên dưới.\n"
                                f"Bắt buộc viết code Python SymPy vào `verify_math.py` chạy kiểm tra đáp án và lưu vào `{out_f.as_posix()}`."
                            )
                            await execute_ai_task(prompt, out_f, "Đang nhân bản câu hỏi từ ảnh mẫu...")

                        ui.button(
                            "🚀 Nhân bản & Kiểm Định",
                            on_click=on_generate_clone,
                            color="primary",
                        ).classes("w-full py-2.5 font-semibold rounded-xl mt-1")

                    # ---------------------------------------------------------
                    # TAB 3: GIỚI THIỆU SẢN PHẨM & TÁC GIẢ
                    # ---------------------------------------------------------
                    with ui.tab_panel(t_about).classes("p-0 gap-3 flex flex-col"):
                        with ui.card().classes(
                            "w-full p-4 rounded-2xl bg-gradient-to-br from-blue-50 to-indigo-50 border border-blue-200 gap-2 shadow-xs"
                        ):
                            with ui.row().classes("items-center gap-2"):
                                ui.icon("school", size="22px").classes("text-blue-700")
                                ui.label("Math Studio THPT 2026").classes("text-sm font-bold text-blue-900")
                            ui.label(
                                "Hệ thống biên soạn và thẩm định đề thi môn Toán chuẩn cấu trúc chương trình GDPT 2018 của Bộ Giáo dục & Đào tạo."
                            ).classes("text-xs text-slate-700 leading-relaxed")

                        with ui.card().classes("w-full p-3.5 rounded-2xl border border-slate-200 bg-white gap-2 shadow-xs"):
                            ui.label("👨‍💻 THÔNG TIN TÁC GIẢ").classes("text-[11px] font-bold text-slate-500 uppercase tracking-wider")
                            ui.label("Tác giả: Nguyễn Minh Trung").classes("text-sm font-bold text-slate-900")
                            with ui.row().classes("items-center gap-1.5"):
                                ui.icon("mail", size="16px").classes("text-slate-400")
                                ui.label("minhtrung.mis@gmail.com").classes("text-xs font-mono text-slate-600")
                            ui.label("Lĩnh vực: EdTech & Khảo thí Toán học THPT").classes("text-xs text-blue-700 font-medium")

                        ui.button(
                            "📖 Mở Cửa Sổ Giới Thiệu Chi Tiết",
                            on_click=lambda: about_dialog.open(),
                            color="blue-700",
                        ).props("unelevated no-caps").classes(
                            "w-full py-2.5 font-bold text-white rounded-xl shadow-xs hover:bg-blue-800"
                        )

            # Card chọn Chế độ thực thi & File đề
            with ui.card().classes("w-full p-4 rounded-2xl shadow-sm border border-slate-200 bg-white gap-3"):
                ui.label("⚙️ Chế độ Xử lý Hệ thống").classes("text-sm font-bold text-slate-700")
                ui.radio(
                    {
                        "live": "⚡ Trực tiếp & Tự động trên Web",
                        "ide": "🖥️ Không gian Làm việc Chuyên sâu (IDE)",
                        "terminal": "🪟 Cửa sổ Dòng lệnh Nâng cao",
                    },
                    value="live",
                ).bind_value(state, "exec_mode").classes("text-xs")

                ui.separator()
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label("📚 Thư viện Quản lý Bộ đề").classes("text-sm font-bold text-slate-800")
                file_select_container = ui.column().classes("w-full")

        # =============================================================
        # CỘT PHẢI: DANH SÁCH THẺ CÂU HỎI TƯƠNG TÁC (QUESTION CARDS)
        # =============================================================
        right_column = ui.column().classes("flex-1 min-w-0 gap-4")

    # -----------------------------------------------------------------
    # HÀM CHẠY AI TRỰC TIẾP BẤT ĐỒNG BỘ (ASYNCIO LIVE STREAM)
    # -----------------------------------------------------------------
    async def execute_ai_task(
        prompt_text: str,
        out_file: Path,
        task_title: str,
        use_continue: bool = False,
        skip_backup: bool = False,
        on_complete=None,
    ):
        if state["is_running"]:
            with right_column:
                ui.notify("AI đang xử lý một tác vụ khác, vui lòng đợi!", type="warning")
            return

        Path("CURRENT_TASK.md").write_text(prompt_text, encoding="utf-8")

        if state["exec_mode"] == "ide":
            with right_column:
                if not AGY_IDE_PATH:
                    ui.notify("Không tìm thấy môi trường IDE trên máy!", type="negative")
                    return
                subprocess.Popen(
                    [AGY_IDE_PATH, str(PROJECT_DIR), str(PROJECT_DIR / "CURRENT_TASK.md")],
                    cwd=str(PROJECT_DIR),
                )
                ui.notify("Đã mở không gian làm việc IDE! Hãy gửi yêu cầu trong khung chat.", type="positive")
            return

        if state["exec_mode"] == "terminal":
            with right_column:
                if not AGY_CLI_PATH:
                    ui.notify("Không tìm thấy công cụ xử lý dòng lệnh!", type="negative")
                    return
                subprocess.Popen(
                    [
                        "cmd",
                        "/c",
                        "start",
                        "Math Studio CLI",
                        AGY_CLI_PATH,
                        "-i",
                        "Thực hiện nhiệm vụ trong CURRENT_TASK.md theo quy trình /tao-de",
                        "--dangerously-skip-permissions",
                    ],
                    cwd=str(PROJECT_DIR),
                )
                ui.notify("Đã mở cửa sổ dòng lệnh!", type="positive")
            return

        # Chế độ Live Stream ngay trên Web
        if not AGY_CLI_PATH:
            with right_column:
                ui.notify("Không tìm thấy công cụ xử lý nền trong PATH!", type="negative")
            return

        if not skip_backup:
            save_version_backup(out_file, "truoc_AI")
        state["is_running"] = True
        live_banner.classes(remove="hidden")
        live_title_lbl.set_text(f"🤖 {task_title}")
        live_thinking_lbl.set_text("Đang phân tích bài toán và khởi tạo tiến trình...")
        live_step_badge.set_text("Bước: 0")
        live_time_badge.set_text("0.0s")
        live_sympy_badge.set_text("Kiểm định: Chờ")
        live_feed_col.clear()

        cmd = [
            AGY_CLI_PATH,
            "-p",
            prompt_text,
            "--output-format",
            "stream-json",
            "--mode",
            "auto",
            "--dangerously-skip-permissions",
        ]
        if use_continue and state.get("last_conv_id"):
            cmd.extend(["--conversation", state["last_conv_id"]])

        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        start_ts = time.time()

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=str(PROJECT_DIR),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            env=env,
        )

        seen_steps: set[int] = set()
        step_count = 0
        detected_conv_id = state.get("last_conv_id") if use_continue else None

        async def _read_stdout():
            nonlocal detected_conv_id
            assert proc.stdout is not None
            while True:
                line_b = await proc.stdout.readline()
                if not line_b:
                    break
                raw = line_b.decode("utf-8", errors="replace").strip()
                if not raw:
                    continue
                try:
                    evt = json.loads(raw)
                    if evt.get("conversation_id"):
                        detected_conv_id = evt["conversation_id"]
                        state["last_conv_id"] = detected_conv_id
                except Exception:
                    pass

        stdout_task = asyncio.create_task(_read_stdout())

        try:
            while proc.returncode is None:
                elapsed = time.time() - start_ts
                live_time_badge.set_text(f"{elapsed:.1f}s")

                t_file = (
                    BRAIN_DIR / detected_conv_id / ".system_generated" / "logs" / "transcript.jsonl"
                    if detected_conv_id
                    else find_newest_transcript(start_ts)
                )
                if t_file and t_file.exists():
                    if not detected_conv_id:
                        detected_conv_id = t_file.parent.parent.parent.name
                        state["last_conv_id"] = detected_conv_id
                    try:
                        lines = t_file.read_text(encoding="utf-8", errors="replace").splitlines()
                        for ln in lines:
                            if not ln.strip():
                                continue
                            step_obj = json.loads(ln)
                            s_idx = step_obj.get("step_index", -1)
                            if s_idx in seen_steps:
                                continue
                            seen_steps.add(s_idx)
                            now_str = datetime.now().strftime("%H:%M:%S")

                            if step_obj.get("type") == "PLANNER_RESPONSE":
                                step_count += 1
                                live_step_badge.set_text(f"Bước: {step_count}")
                                th = step_obj.get("thinking", "").strip()
                                if th:
                                    live_thinking_lbl.set_text(f"🧠 Suy luận: {th}")
                                for tc in step_obj.get("tool_calls", []):
                                    desc = format_tool_call_vn(tc)
                                    live_title_lbl.set_text(f"🤖 Bước {step_count}: {desc}")
                                    with live_feed_col:
                                        ui.label(f"[{now_str}] {desc}").classes(
                                            "text-xs text-slate-700 font-mono"
                                        )
                                    if "verify_math.py" in desc or "verify_single.py" in desc:
                                        live_sympy_badge.set_text("Kiểm định: Đang xử lý")
                            elif step_obj.get("type") == "GENERIC":
                                c_txt = step_obj.get("content", "")
                                if "Exit Code: 0" in c_txt and (
                                    "verify_math.py" in c_txt or "verify_single.py" in c_txt
                                ):
                                    live_sympy_badge.set_text("Kiểm định: ✓ Đạt chuẩn")
                                    with live_feed_col:
                                        ui.label(
                                            f"[{now_str}] 🎯 Đã kiểm định nghiệm chính xác (Exit Code: 0)"
                                        ).classes("text-xs text-emerald-700 font-semibold")
                    except Exception:
                        pass

                await asyncio.sleep(0.4)

            await stdout_task
            if on_complete is not None:
                try:
                    on_complete()
                except Exception as exc:
                    print("on_complete error:", exc)
        finally:
            state["is_running"] = False
            live_banner.classes(add="hidden")
            if out_file.exists():
                register_exam_metadata(
                    out_file,
                    grade=state.get("grade", "Toán 12 - THPT 2026"),
                    topic=state.get("topic", "Tổng hợp"),
                )
            with right_column:
                ui.notify("🎉 Đã hoàn tất xử lý và kiểm định toán học!", type="positive")
            render_File_selector()
            render_questions_workspace()

    # -----------------------------------------------------------------
    # HỘP THOẠI YÊU CẦU AI SỬA RIÊNG 1 CÂU HỎI (CÔ LẬP 1 CÂU + SYMPY RIÊNG)
    # -----------------------------------------------------------------
    ai_fix_dialog = ui.dialog()
    ai_fix_state = {"q_idx": 0, "q_title": "", "q_stem": "", "custom_req": ""}

    with ai_fix_dialog, ui.card().classes("w-[680px] max-w-[95vw] p-6 rounded-2xl gap-3"):
        with ui.row().classes("w-full items-center justify-between"):
            ai_fix_header = ui.label("🤖 Yêu cầu AI Sửa riêng Câu hỏi").classes(
                "text-lg font-bold text-slate-800"
            )
            ui.button(icon="close", on_click=ai_fix_dialog.close).props("flat round dense")

        ai_fix_preview = ui.html("", sanitize=False).classes(
            "w-full p-3 rounded-xl bg-slate-50 border border-slate-200 text-sm max-h-44 overflow-y-auto"
        )

        ui.label("⚡ Chọn nhanh kiểu biến đổi (1-Click):").classes(
            "text-xs font-bold text-slate-500 uppercase tracking-wider mt-1"
        )

        async def trigger_ai_single_question(instruction: str):
            ai_fix_dialog.close()
            active_path = Path(state["active_file"])
            header_md, qs = parse_exam_markdown(active_path.read_text(encoding="utf-8"))
            idx = ai_fix_state["q_idx"]
            if idx < 0 or idx >= len(qs):
                return

            save_version_backup(active_path, f"truoc_sua_cau_{idx+1}")
            target_q = qs[idx]
            temp_q_file = PROJECT_DIR / "temp_single_q.md"
            temp_q_file.write_text(target_q["full_block"], encoding="utf-8")

            sec_info = f" thuộc {target_q['section']}" if target_q.get("section") else ""
            q_prompt = (
                f"Bạn chỉ cần xử lý DUY NHẤT 1 câu toán dưới đây ({target_q['title']}{sec_info}). KHÔNG đọc hay kiểm tra các câu khác của đề.\n\n"
                f"--- NỘI DUNG CÂU HIỆN TẠI ---\n"
                f"{target_q['full_block']}\n"
                f"-----------------------------\n\n"
                f"YÊU CẦU CHỈNH SỬA: \"{instruction}\"\n\n"
                f"QUY TRÌNH BẮT BUỘC (3 BƯỚC NGẮN GỌN):\n"
                f"1. Viết file `verify_single.py` bằng `sympy` để tính toán và kiểm chứng CHỈ RIÊNG câu hỏi mới này.\n"
                f"2. Không cần đọc file schema, hãy gọi trực tiếp `call_mcp_tool` với `ServerName: \"local-runner\"`, `ToolName: \"run_command\"`, `Arguments: {{\"executable\": \"python\", \"args\": [\"verify_single.py\"], \"cwd\": \"D:\\\\MathAI\\\\de-toan-ai\"}}` để lấy đáp án chính xác 100%.\n"
                f"3. Ghi nội dung câu hỏi mới KÈM ĐÁP ÁN MỚI VÀ LỜI GIẢI CHI TIẾT MỚI vào file `{temp_q_file.as_posix()}` theo đúng cấu trúc:\n"
                f"### {target_q['title']}.\n"
                f"<Đề bài mới và các phương án lựa chọn mới>\n\n"
                f"**Lời giải:**\n"
                f"- **Đáp án đúng:** <Đáp án mới khớp kết quả SymPy>\n"
                f"- <Trình bày lời giải chi tiết từng bước của bài toán mới>"
            )

            def _merge_single_q():
                if temp_q_file.exists():
                    new_block = temp_q_file.read_text(encoding="utf-8").strip()
                    if new_block:
                        curr_h, curr_qs = parse_exam_markdown(active_path.read_text(encoding="utf-8"))
                        if 0 <= idx < len(curr_qs):
                            curr_qs[idx]["full_block"] = new_block
                            active_path.write_text(
                                rebuild_exam_markdown(curr_h, curr_qs), encoding="utf-8"
                            )
                            state["open_solutions"].add(idx)
                    temp_q_file.unlink(missing_ok=True)

            asyncio.create_task(
                execute_ai_task(
                    q_prompt,
                    active_path,
                    f"Đang sửa & tính lại đáp án riêng {target_q['title']} ({instruction[:40]}...)",
                    use_continue=False,
                    skip_backup=True,
                    on_complete=_merge_single_q,
                )
            )

        with ui.grid(columns=2).classes("w-full gap-2 mt-1"):
            presets = [
                ("🎲 Đổi số liệu nghiệm đẹp", "Đổi bộ số liệu/hệ số khác sao cho nghiệm nguyên đẹp hoặc phân số tối giản gọn gàng, tính lại đáp án mới và lời giải mới"),
                ("📈 Thêm Hình vẽ Đồ thị", "Chuyển thành câu hỏi nhận dạng đồ thị hàm số (hoặc BBT), tự động gọi math_draw sinh ảnh PNG vào output/images/ và nhúng vào đề"),
                ("📐 Thêm Hình vẽ Không gian", "Chuyển thành câu hỏi hình học không gian, tự động gọi math_draw vẽ khối chóp/lăng trụ với nét khuất nét liền chuẩn SGK và nhúng vào đề"),
                ("🔥 Nâng lên Vận dụng cao", "Phát triển câu hỏi này lên mức độ Vận dụng cao (kết hợp tham số m, cực trị hoặc tối ưu hóa)"),
                ("🌱 Hạ độ khó (Thông hiểu)", "Đơn giản hóa câu hỏi này xuống mức Thông hiểu, áp dụng công thức trực tiếp, số liệu dễ tính"),
                ("🏢 Gắn bài toán thực tế", "Chuyển bài toán thành tình huống ứng dụng thực tế sinh động (kinh tế, kiến trúc, chuyển động, y tế)"),
                ("🎯 Sửa phương án nhiễu", "Thiết kế lại 3 phương án nhiễu sai lầm kinh điển của học sinh, đảm bảo 4 phương án khác nhau đôi một"),
                ("📖 Giải chi tiết từng bước", "Viết lại phần lời giải chi tiết, rõ ràng từng bước biến đổi và nêu phương pháp giải tổng quát"),
            ]
            for label_txt, prompt_val in presets:
                with ui.card().classes(
                    "p-2.5 rounded-xl border border-blue-200 bg-blue-50/60 hover:bg-blue-100/90 cursor-pointer transition-all gap-0.5"
                ).on("click", lambda _, p=prompt_val: trigger_ai_single_question(p)):
                    ui.label(label_txt).classes("text-xs font-bold text-blue-900")

        ui.label("✍️ Hoặc nhập yêu cầu chỉnh sửa cụ thể của bạn:").classes(
            "text-xs font-bold text-slate-500 uppercase tracking-wider mt-2"
        )
        custom_req_input = ui.textarea(
            placeholder="VD: Đổi hàm số thành y = (2x - 1)/(x + 1), yêu cầu tìm GTLN trên đoạn [0; 3]...",
        ).bind_value(ai_fix_state, "custom_req").classes("w-full")

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Hủy", on_click=ai_fix_dialog.close).props("flat no-caps")
            ui.button(
                "✨ Yêu cầu Chỉnh sửa & Tính lại Đáp án",
                on_click=lambda: trigger_ai_single_question(
                    ai_fix_state["custom_req"].strip() or "Đổi bộ số liệu mới có nghiệm đẹp, tính lại đáp án và lời giải mới"
                ),
                color="primary",
            ).props("no-caps").classes("px-4 font-semibold")

    def open_ai_fix_modal(q_idx: int, q_obj: dict):
        ai_fix_state["q_idx"] = q_idx
        ai_fix_state["q_title"] = q_obj["title"]
        ai_fix_state["q_stem"] = q_obj["stem"]
        ai_fix_state["custom_req"] = ""
        sec_badge = f" [{q_obj['section']}]" if q_obj.get("section") else ""
        ai_fix_header.set_text(f"🤖 Yêu cầu AI sửa riêng: {q_obj['title']}{sec_badge}")
        ai_fix_preview.set_content(md_to_math_html(q_obj["stem"]))
        ai_fix_dialog.open()
        trigger_mathjax()

    # -----------------------------------------------------------------
    # MODAL 1: CÂY CHUYÊN ĐỀ & QUẢN LÝ CHUYÊN ĐỀ MỚI (TREE MODAL)
    # -----------------------------------------------------------------
    add_custom_lesson_dialog = ui.dialog()
    custom_lesson_state = {"chap_idx": 0, "name": ""}
    with add_custom_lesson_dialog, ui.card().classes("w-[420px] max-w-[95vw] p-5 rounded-2xl gap-3"):
        ui.label("➕ Thêm Chuyên đề mới vào nhóm").classes("text-base font-bold text-slate-800")
        custom_lesson_input = ui.input(label="Tên chuyên đề bài học mới", placeholder="VD: Nhị thức Newton nâng cao...").bind_value(custom_lesson_state, "name").props("outlined dense autofocus").classes("w-full")
        def confirm_add_lesson():
            name = custom_lesson_state["name"].strip()
            if name:
                c_idx = custom_lesson_state["chap_idx"]
                if 0 <= c_idx < len(TOPIC_TREE_DATA):
                    new_id = f"custom_l_{int(time.time()*1000)}"
                    TOPIC_TREE_DATA[c_idx]["children"].append({"id": new_id, "label": name})
                    ID_TO_LABEL[new_id] = name
                    ALL_LEAF_IDS.append(new_id)
                    state["selected_topics"].append(new_id)
                    ui.notify(f"✓ Đã thêm chuyên đề '{name}'!", type="positive")
                    render_tree_modal_content()
            add_custom_lesson_dialog.close()
        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Hủy", on_click=add_custom_lesson_dialog.close).props("flat no-caps")
            ui.button("Thêm ngay", on_click=confirm_add_lesson, color="primary").props("unelevated no-caps")

    add_custom_chap_dialog = ui.dialog()
    custom_chap_state = {"name": ""}
    with add_custom_chap_dialog, ui.card().classes("w-[420px] max-w-[95vw] p-5 rounded-2xl gap-3"):
        ui.label("➕ Thêm Nhóm / Chương mới").classes("text-base font-bold text-slate-800")
        ui.input(label="Tên Nhóm / Chương mới", placeholder="VD: 📗 Đại số tuyến tính & Ma trận...").bind_value(custom_chap_state, "name").props("outlined dense autofocus").classes("w-full")
        def confirm_add_chap():
            name = custom_chap_state["name"].strip()
            if name:
                new_c_id = f"custom_chap_{int(time.time()*1000)}"
                TOPIC_TREE_DATA.append({"id": new_c_id, "label": name, "children": []})
                ui.notify(f"✓ Đã thêm nhóm '{name}'!", type="positive")
                render_tree_modal_content()
            add_custom_chap_dialog.close()
        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Hủy", on_click=add_custom_chap_dialog.close).props("flat no-caps")
            ui.button("Thêm chương", on_click=confirm_add_chap, color="primary").props("unelevated no-caps")

    with tree_dialog, ui.card().classes("w-[920px] max-w-[96vw] max-h-[92vh] p-6 rounded-2xl gap-3.5 flex flex-col"):
        with ui.row().classes("w-full items-center justify-between pb-2 border-b border-slate-200"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("account_tree", size="24px").classes("text-indigo-700")
                with ui.column().classes("gap-0"):
                    ui.label("Cây Chuyên đề & Ngân hàng Kiến thức GDPT 2018").classes("text-lg font-bold text-slate-800")
                    ui.label("Mặc định không tick. Chọn chuyên đề để đưa vào ma trận hoặc tự thêm chuyên đề mới vào từng nhóm.").classes("text-xs text-slate-500")
            ui.button(icon="close", on_click=tree_dialog.close).props("flat round dense")

        # Thanh thao tác nhanh trên cây chuyên đề
        with ui.row().classes("w-full items-center justify-between gap-1 flex-wrap bg-slate-50 p-2 rounded-xl border border-slate-200"):
            with ui.row().classes("items-center gap-1.5 flex-wrap"):
                def bulk_tree(mode: str):
                    if mode == "all":
                        state["selected_topics"] = list(ALL_LEAF_IDS)
                    elif mode == "none":
                        state["selected_topics"] = []
                    elif mode == "ham_so":
                        state["selected_topics"] = [t for t in ALL_LEAF_IDS if t.startswith("hs_")]
                    elif mode == "hhkg":
                        state["selected_topics"] = [t for t in ALL_LEAF_IDS if t.startswith("hh_") or t.startswith("oxyz_")]
                    elif mode == "xs":
                        state["selected_topics"] = [t for t in ALL_LEAF_IDS if t.startswith("xs_") or t.startswith("tk_")]
                    render_tree_modal_content()

                ui.button("✅ Chọn tất cả", on_click=lambda: bulk_tree("all")).props("unelevated size=xs no-caps").classes("bg-blue-600 text-white font-semibold px-2.5 py-1 rounded-lg")
                ui.button("🗑️ Bỏ chọn toàn bộ", on_click=lambda: bulk_tree("none")).props("unelevated size=xs no-caps").classes("bg-slate-200 text-slate-700 font-medium px-2.5 py-1 rounded-lg")
                ui.button("📘 Khảo sát hàm số", on_click=lambda: bulk_tree("ham_so")).props("unelevated size=xs no-caps").classes("bg-indigo-100 text-indigo-900 font-medium px-2.5 py-1 rounded-lg")
                ui.button("📐 HHKG & Oxyz", on_click=lambda: bulk_tree("hhkg")).props("unelevated size=xs no-caps").classes("bg-emerald-100 text-emerald-900 font-medium px-2.5 py-1 rounded-lg")
                ui.button("🎲 Xác suất", on_click=lambda: bulk_tree("xs")).props("unelevated size=xs no-caps").classes("bg-amber-100 text-amber-900 font-medium px-2.5 py-1 rounded-lg")

            with ui.row().classes("items-center gap-2"):
                ui.button("➕ Thêm Nhóm/Chương mới", on_click=add_custom_chap_dialog.open, color="indigo-700").props("unelevated size=xs no-caps").classes("text-white font-semibold px-2.5 py-1 rounded-lg")
                tree_badge_count = ui.badge(f"Đã chọn: {len(state.get('selected_topics', []))} bài học", color="blue-700").classes("text-xs px-2.5 py-1 rounded-lg font-bold")

        tree_content_scroll = ui.column().classes("w-full max-h-[58vh] overflow-y-auto gap-3 pr-1")

        def render_tree_modal_content():
            tree_content_scroll.clear()
            sel_set = set(state.get("selected_topics", []))
            tree_badge_count.set_text(f"Đã chọn: {len(sel_set)} / {len(ALL_LEAF_IDS)} bài học")
            with tree_content_scroll:
                for c_idx, chap in enumerate(TOPIC_TREE_DATA):
                    ch_children = chap.get("children", [])
                    c_checked_count = sum(1 for c in ch_children if c["id"] in sel_set)

                    with ui.card().classes("w-full p-3 rounded-xl border border-slate-200 bg-white gap-2"):
                        with ui.row().classes("w-full items-center justify-between no-wrap bg-slate-50 p-2 rounded-lg border border-slate-200"):
                            with ui.row().classes("items-center gap-2"):
                                ui.label(chap["label"]).classes("text-sm font-bold text-slate-800")
                                ui.badge(f"{c_checked_count}/{len(ch_children)}", color="indigo-700" if c_checked_count > 0 else "slate-400").classes("text-[10px] px-1.5 py-0.5 rounded-md")
                            
                            def open_add_l(idx=c_idx):
                                custom_lesson_state["chap_idx"] = idx
                                custom_lesson_state["name"] = ""
                                add_custom_lesson_dialog.open()

                            ui.button(
                                "➕ Thêm chuyên đề vào nhóm này",
                                on_click=open_add_l,
                                color="indigo-50",
                            ).props("unelevated size=xs no-caps").classes("text-indigo-800 font-bold border border-indigo-200 hover:bg-indigo-100 px-2.5 py-1 rounded-lg")

                        with ui.grid(columns=2).classes("w-full gap-2 px-1"):
                            for child in ch_children:
                                is_ticked = child["id"] in sel_set
                                def on_toggle_box(val, cid=child["id"]):
                                    if val and cid not in state["selected_topics"]:
                                        state["selected_topics"].append(cid)
                                    elif not val and cid in state["selected_topics"]:
                                        state["selected_topics"].remove(cid)
                                    sel_now = set(state["selected_topics"])
                                    tree_badge_count.set_text(f"Đã chọn: {len(sel_now)} / {len(ALL_LEAF_IDS)} bài học")

                                with ui.row().classes("items-center gap-2 p-1 rounded-lg hover:bg-slate-50"):
                                    ui.checkbox(
                                        text=child["label"],
                                        value=is_ticked,
                                        on_change=lambda e, cid=child["id"]: on_toggle_box(e.value, cid),
                                    ).classes("text-xs text-slate-800")

        # Nút áp dụng ở chân modal
        with ui.row().classes("w-full items-center justify-between pt-3 border-t border-slate-200"):
            ui.button("Đóng", on_click=tree_dialog.close).props("flat no-caps").classes("text-slate-600 px-4")
            
            def apply_selected_to_matrix():
                sel_ids = state.get("selected_topics", [])
                if not sel_ids:
                    ui.notify("Bạn chưa chọn chuyên đề nào!", type="warning")
                    return
                # Thêm các chuyên đề đã chọn vào Phần 1 của Ma trận
                sec_list = state.get("matrix_sections", [])
                if not sec_list:
                    sec_list.append({
                        "id": "sec_1", "title": "Phần I", "subtitle": "Một lựa chọn đúng",
                        "type": "Một lựa chọn đúng", "rows": []
                    })
                target_sec = sec_list[0]
                existing_topics = {r["topic"] for r in target_sec.get("rows", [])}
                added_count = 0
                for cid in sel_ids:
                    lbl = ID_TO_LABEL.get(cid, cid)
                    if lbl not in existing_topics:
                        cat_name = get_topic_category(lbl)
                        target_sec.setdefault("rows", []).append({
                            "category": cat_name,
                            "topic": lbl,
                            "note": "",
                            "nb": 1, "th": 1, "vd": 1, "vdc": 0,
                        })
                        added_count += 1
                ui.notify(f"✓ Đã đưa {added_count} chuyên đề vào Ma trận đề thi!", type="positive")
                tree_dialog.close()
                update_matrix_ui()
                edit_current_matrix_wizard()

            ui.button(
                "✓ Đưa các chuyên đề đã chọn vào Ma trận Đề",
                on_click=apply_selected_to_matrix,
                color="primary",
            ).props("unelevated no-caps").classes("font-bold px-5 py-2 rounded-xl")

    # -----------------------------------------------------------------
    # MODAL 2A: QUẢN LÝ DANH SÁCH MA TRẬN ĐỀ THI
    # -----------------------------------------------------------------
    matrix_list_dialog = ui.dialog()
    matrix_list_container = None

    def render_matrix_list():
        if matrix_list_container is None:
            return
        matrix_list_container.clear()
        templates = load_matrix_templates()
        active_id = state.get("active_matrix_id", "")
        with matrix_list_container:
            if not templates:
                ui.label("Chưa có mẫu ma trận nào trong danh sách.").classes("text-slate-500 italic p-4 text-center")
                return

            for idx, tpl in enumerate(templates):
                is_active = tpl.get("id") == active_id
                border_cls = "border-2 border-blue-600 bg-blue-50/50 shadow-sm" if is_active else "border border-slate-200 bg-white hover:border-slate-300"
                
                with ui.card().classes(f"w-full p-4 rounded-2xl {border_cls} gap-2.5 transition-all"):
                    with ui.row().classes("w-full items-start justify-between no-wrap gap-2"):
                        with ui.column().classes("gap-1 flex-1"):
                            with ui.row().classes("items-center gap-2"):
                                ui.label(tpl.get("title", "Ma trận không tên")).classes("text-base font-bold text-slate-900")
                                if is_active:
                                    ui.badge("✓ ĐANG ÁP DỤNG", color="emerald-700").classes("text-[10px] font-bold px-2 py-0.5 rounded-full")
                            if tpl.get("desc"):
                                ui.label(tpl["desc"]).classes("text-xs text-slate-500 line-clamp-2")
                        
                        # Thống kê câu & điểm
                        stats = calc_matrix_summary(tpl.get("sections", []))
                        with ui.row().classes("items-center gap-1.5 shrink-0"):
                            ui.badge(f"{stats['total_q']} câu • {stats['points']:.2f}đ", color="blue-800").classes("text-xs font-bold px-2.5 py-1 rounded-lg")
                            ui.badge(f"⏱️ {tpl.get('duration', 90)}p", color="indigo-700").classes("text-xs font-bold px-2.5 py-1 rounded-lg")

                    # Chi tiết các phần
                    with ui.row().classes("w-full items-center gap-2 py-1 flex-wrap"):
                        for sec in tpl.get("sections", []):
                            sec_q = sum(int(r.get("nb") or 0) + int(r.get("th") or 0) + int(r.get("vd") or 0) + int(r.get("vdc") or 0) for r in sec.get("rows", []))
                            ui.badge(f"{sec.get('title', 'Phần')}: {sec_q} câu ({len(sec.get('rows', []))} CĐ)", color="slate-100").classes("text-slate-700 text-[11px] font-semibold border border-slate-200")

                    # Hàng nút hành động
                    with ui.row().classes("w-full items-center justify-between pt-2 border-t border-slate-100"):
                        with ui.row().classes("items-center gap-2"):
                            def do_apply(t=tpl):
                                apply_matrix_template(t)
                                matrix_list_dialog.close()
                                ui.notify(f"✓ Đã áp dụng ma trận '{t.get('title')}'!", type="positive")

                            if not is_active:
                                ui.button("✓ Áp dụng", on_click=do_apply, color="primary").props("unelevated size=sm no-caps").classes("font-bold px-3 py-1 rounded-lg")
                            else:
                                ui.button("✓ Đang dùng", color="emerald-600").props("flat size=sm no-caps").classes("font-bold text-emerald-800")

                            def do_edit(t=tpl):
                                matrix_list_dialog.close()
                                edit_matrix_wizard(t)

                            ui.button("✏️ Chỉnh sửa", on_click=do_edit, color="slate-100").props("unelevated size=sm no-caps").classes("text-slate-800 font-semibold px-3 py-1 rounded-lg border border-slate-200")

                            def do_clone(t=tpl):
                                cloned = json.loads(json.dumps(t))
                                cloned["id"] = f"mat_{int(time.time()*1000)}"
                                cloned["title"] = f"{t.get('title', 'Ma trận')} (Bản sao)"
                                all_tpls = load_matrix_templates()
                                all_tpls.append(cloned)
                                save_matrix_templates(all_tpls)
                                render_matrix_list()
                                ui.notify(f"✓ Đã nhân bản thành '{cloned['title']}'!", type="positive")

                            ui.button("📋 Nhân bản", on_click=do_clone, color="slate-50").props("flat size=sm no-caps").classes("text-slate-700 font-medium px-2 py-1 rounded-lg hover:bg-slate-100")

                        def do_delete(t_id=tpl.get("id"), t_title=tpl.get("title")):
                            all_tpls = load_matrix_templates()
                            if len(all_tpls) <= 1:
                                ui.notify("Cần giữ lại ít nhất 1 ma trận đề thi trong hệ thống!", type="warning")
                                return
                            new_tpls = [x for x in all_tpls if x.get("id") != t_id]
                            save_matrix_templates(new_tpls)
                            if state.get("active_matrix_id") == t_id and new_tpls:
                                apply_matrix_template(new_tpls[0])
                            render_matrix_list()
                            ui.notify(f"✓ Đã xóa ma trận '{t_title}'!", type="info")

                        ui.button("🗑️ Xóa", on_click=do_delete).props("flat dense size=sm color=red-400 no-caps").classes("hover:bg-red-50 px-2 py-1 rounded-lg")

    with matrix_list_dialog, ui.card().classes("w-[960px] max-w-[97vw] max-h-[92vh] p-6 rounded-2xl gap-4 flex flex-col"):
        with ui.row().classes("w-full items-center justify-between pb-2 border-b border-slate-200"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("folder_special", size="26px").classes("text-blue-700")
                with ui.column().classes("gap-0"):
                    ui.label("Quản lý Danh sách Ma trận Đề thi").classes("text-lg font-bold text-slate-800")
                    ui.label("Danh sách các mẫu ma trận đề thi đã lưu. Chọn để sử dụng, sửa đổi hoặc tạo mới theo quy trình.").classes("text-xs text-slate-500")
            ui.button(icon="close", on_click=matrix_list_dialog.close).props("flat round dense")

        matrix_list_container = ui.column().classes("w-full max-h-[65vh] overflow-y-auto gap-3 pr-1")

        with ui.row().classes("w-full items-center justify-between pt-3 border-t border-slate-200"):
            def on_click_create_from_list():
                matrix_list_dialog.close()
                start_new_matrix_wizard()

            ui.button("➕ Tạo Ma trận Đề thi Mới", on_click=on_click_create_from_list, color="emerald-600").props("unelevated no-caps").classes("text-white font-bold px-4 py-2 rounded-xl shadow-xs hover:bg-emerald-700")
            ui.button("Đóng", on_click=matrix_list_dialog.close).props("flat no-caps").classes("text-slate-600 font-semibold px-4")

    # -----------------------------------------------------------------
    # MODAL 2B: QUY TRÌNH THIẾT LẬP MA TRẬN ĐỀ THI (2 BƯỚC: CHỌN CĐ -> BẢNG MA TRẬN)
    # -----------------------------------------------------------------
    matrix_wizard_dialog = ui.dialog()
    wizard_state = {
        "step": 1,  # 1: Tick chuyên đề -> 2: Thiết lập số câu & combobox
        "id": "",
        "title": "",
        "desc": "",
        "duration": 90,
        "grade": "Toán 12 - Tốt nghiệp THPT 2026",
        "selected_topics": [],
        "sections": [],
        "filter_kw": "",
    }
    wizard_body_container = None

    def render_wizard_content():
        if wizard_body_container is None:
            return
        wizard_body_container.clear()
        step = wizard_state.get("step", 1)

        with wizard_body_container:
            # Thanh tiến trình 2 Bước (Stepper Header)
            with ui.row().classes("w-full items-center justify-center gap-4 py-2 px-4 rounded-xl bg-slate-50 border border-slate-200 mb-1"):
                # Bước 1
                b1_active = step == 1
                b1_cls = "bg-blue-600 text-white font-bold" if b1_active else "bg-blue-100 text-blue-900 font-semibold cursor-pointer"
                with ui.row().classes(f"items-center gap-2 px-3 py-1.5 rounded-lg {b1_cls}").on("click", lambda: switch_step(1)):
                    ui.label("1").classes("w-5 h-5 rounded-full bg-white text-blue-800 text-xs font-bold flex items-center justify-center")
                    ui.label("Bước 1: Tick chọn Chuyên đề").classes("text-xs")
                    step1_badge = ui.badge(f"{len(wizard_state['selected_topics'])} CĐ", color="white").classes("text-[10px] text-blue-900 font-bold px-1.5 py-0.5 rounded")

                ui.icon("arrow_forward", size="18px").classes("text-slate-400")

                # Bước 2
                b2_active = step == 2
                b2_cls = "bg-blue-600 text-white font-bold" if b2_active else "bg-slate-200 text-slate-700 font-semibold cursor-pointer"
                with ui.row().classes(f"items-center gap-2 px-3 py-1.5 rounded-lg {b2_cls}").on("click", lambda: switch_step(2)):
                    ui.label("2").classes("w-5 h-5 rounded-full bg-white text-blue-800 text-xs font-bold flex items-center justify-center")
                    ui.label("Bước 2: Bảng Ma trận (Số câu & Combobox)").classes("text-xs")

            def switch_step(target_step):
                if target_step == 2:
                    if not wizard_state.get("selected_topics"):
                        ui.notify("Vui lòng tick chọn ít nhất 1 chuyên đề ở Bước 1 trước!", type="warning")
                        return
                    proceed_to_step_2()
                    return
                wizard_state["step"] = target_step
                render_wizard_content()

            # =========================================================
            # NỘI DUNG BƯỚC 1: TICK CHỌN CHUYÊN ĐỀ
            # =========================================================
            if step == 1:
                chk_map = {}
                chap_badge_map = {}
                sel_set = set(wizard_state.get("selected_topics", []))

                def refresh_counts():
                    cnt = len(wizard_state["selected_topics"])
                    step1_badge.set_text(f"{cnt} CĐ")
                    if "footer_count_lbl" in locals():
                        footer_count_lbl.set_text(f"Đã chọn: {cnt} / {len(ALL_LEAF_IDS)} chuyên đề")
                    for c_i, ch_data in enumerate(TOPIC_TREE_DATA):
                        c_kids = ch_data.get("children", [])
                        c_hit = sum(1 for k in c_kids if k["id"] in wizard_state["selected_topics"])
                        if c_i in chap_badge_map:
                            chap_badge_map[c_i].set_text(f"{c_hit}/{len(c_kids)}")
                            chap_badge_map[c_i].props(f"color={'indigo-700' if c_hit > 0 else 'slate-400'}")

                with ui.column().classes("w-full gap-3"):
                    with ui.row().classes("w-full items-center justify-between gap-2 flex-wrap"):
                        with ui.column().classes("gap-0"):
                            ui.label("📋 Bước 1: Tick chọn danh sách chuyên đề cần ra đề").classes("text-base font-bold text-slate-800")
                            ui.label("Chỉ những chuyên đề được tick ở đây mới xuất hiện trong Combobox chọn chủ đề ở Bước 2.").classes("text-xs text-blue-700 font-medium")

                        with ui.row().classes("items-center gap-1.5 flex-wrap"):
                            def set_wizard_topics(mode: str):
                                wizard_state["manually_deleted"] = {}
                                if mode == "all":
                                    new_sel = list(ALL_LEAF_IDS)
                                elif mode == "none":
                                    new_sel = []
                                elif mode == "ham_so":
                                    new_sel = [t for t in ALL_LEAF_IDS if t.startswith("hs_")]
                                elif mode == "hhkg":
                                    new_sel = [t for t in ALL_LEAF_IDS if t.startswith("hh_") or t.startswith("oxyz_")]
                                elif mode == "xs":
                                    new_sel = [t for t in ALL_LEAF_IDS if t.startswith("xs_") or t.startswith("tk_")]
                                wizard_state["selected_topics"] = new_sel
                                target_set = set(new_sel)
                                for c_id, chk_w in chk_map.items():
                                    chk_w.value = (c_id in target_set)
                                refresh_counts()

                            ui.button("✅ Chọn tất cả", on_click=lambda: set_wizard_topics("all")).props("unelevated size=xs no-caps").classes("bg-blue-600 text-white font-semibold px-2.5 py-1 rounded-lg")
                            ui.button("🗑️ Bỏ chọn hết", on_click=lambda: set_wizard_topics("none")).props("unelevated size=xs no-caps").classes("bg-slate-200 text-slate-700 font-medium px-2.5 py-1 rounded-lg")
                            ui.button("📘 Khảo sát hàm số", on_click=lambda: set_wizard_topics("ham_so")).props("unelevated size=xs no-caps").classes("bg-indigo-100 text-indigo-900 font-medium px-2.5 py-1 rounded-lg")
                            ui.button("📐 HHKG & Oxyz", on_click=lambda: set_wizard_topics("hhkg")).props("unelevated size=xs no-caps").classes("bg-emerald-100 text-emerald-900 font-medium px-2.5 py-1 rounded-lg")
                            ui.button("🎲 Xác suất", on_click=lambda: set_wizard_topics("xs")).props("unelevated size=xs no-caps").classes("bg-amber-100 text-amber-900 font-medium px-2.5 py-1 rounded-lg")

                    # Danh sách cây chuyên đề có Checkbox
                    tree_scroll = ui.column().classes("w-full max-h-[50vh] overflow-y-auto gap-3 pr-1")
                    with tree_scroll:
                        for c_idx, chap in enumerate(TOPIC_TREE_DATA):
                            ch_children = chap.get("children", [])
                            c_checked_count = sum(1 for c in ch_children if c["id"] in sel_set)

                            with ui.card().classes("w-full p-3 rounded-xl border border-slate-200 bg-white gap-2"):
                                with ui.row().classes("w-full items-center justify-between no-wrap bg-slate-50 p-2 rounded-lg border border-slate-200"):
                                    with ui.row().classes("items-center gap-2"):
                                        ui.label(chap["label"]).classes("text-sm font-bold text-slate-800")
                                        c_bg = ui.badge(f"{c_checked_count}/{len(ch_children)}", color="indigo-700" if c_checked_count > 0 else "slate-400").classes("text-[10px] px-1.5 py-0.5 rounded-md")
                                        chap_badge_map[c_idx] = c_bg
                                    
                                    # Toggle cả chương
                                    def toggle_chap(c_obj=chap):
                                        c_ids = [c["id"] for c in c_obj.get("children", [])]
                                        all_in = all(cid in wizard_state["selected_topics"] for cid in c_ids)
                                        new_target = not all_in
                                        for cid in c_ids:
                                            lbl = ID_TO_LABEL.get(cid, cid)
                                            if new_target and cid not in wizard_state["selected_topics"]:
                                                wizard_state["selected_topics"].append(cid)
                                                for dset in wizard_state.get("manually_deleted", {}).values():
                                                    dset.discard(lbl)
                                            elif not new_target and cid in wizard_state["selected_topics"]:
                                                wizard_state["selected_topics"].remove(cid)
                                                for dset in wizard_state.get("manually_deleted", {}).values():
                                                    dset.discard(lbl)
                                            if cid in chk_map:
                                                chk_map[cid].value = new_target
                                        refresh_counts()

                                    ui.button("Chọn/Bỏ nhóm này", on_click=toggle_chap).props("flat dense size=xs no-caps").classes("text-indigo-800 font-semibold px-2")

                                with ui.grid(columns=2).classes("w-full gap-2 px-1"):
                                    for child in ch_children:
                                        cid = child["id"]
                                        is_ticked = cid in sel_set

                                        def make_on_change(child_id=cid):
                                            def on_toggle_wiz_box(e):
                                                val = e.value
                                                lbl = ID_TO_LABEL.get(child_id, child_id)
                                                if val and child_id not in wizard_state["selected_topics"]:
                                                    wizard_state["selected_topics"].append(child_id)
                                                    for dset in wizard_state.get("manually_deleted", {}).values():
                                                        dset.discard(lbl)
                                                elif not val and child_id in wizard_state["selected_topics"]:
                                                    wizard_state["selected_topics"].remove(child_id)
                                                    for dset in wizard_state.get("manually_deleted", {}).values():
                                                        dset.discard(lbl)
                                                refresh_counts()
                                            return on_toggle_wiz_box

                                        with ui.row().classes("items-center gap-2 p-1 rounded-lg hover:bg-slate-50"):
                                            chk = ui.checkbox(
                                                text=child["label"],
                                                value=is_ticked,
                                                on_change=make_on_change(cid),
                                            ).classes("text-xs text-slate-800")
                                            chk_map[cid] = chk

                    # Chân bước 1
                    with ui.row().classes("w-full items-center justify-between pt-3 border-t border-slate-200"):
                        ui.button("Hủy & Đóng", on_click=matrix_wizard_dialog.close).props("flat no-caps").classes("text-slate-600 px-4")
                        footer_count_lbl = ui.label(f"Đã chọn: {len(wizard_state['selected_topics'])} / {len(ALL_LEAF_IDS)} chuyên đề").classes("text-xs font-bold text-blue-900")

                        def proceed_to_step_2():
                            if not wizard_state.get("selected_topics"):
                                ui.notify("Vui lòng tick chọn ít nhất 1 chuyên đề!", type="warning")
                                return
                            sel_labels = []
                            for cid in wizard_state["selected_topics"]:
                                lbl = ID_TO_LABEL.get(cid, cid)
                                if lbl and lbl not in sel_labels:
                                    sel_labels.append(lbl)
                            if not sel_labels:
                                sel_labels = list(wizard_state["selected_topics"])

                            sel_set = set(sel_labels)
                            sel_ids = set(wizard_state["selected_topics"])

                            # Đồng bộ TẤT CẢ các Phần thi (sections) với danh sách chuyên đề đã chọn
                            for s_idx, sec in enumerate(wizard_state.get("sections", [])):
                                old_rows = sec.get("rows", [])

                                # 1. TỰ ĐỘNG BỎ các dòng có chuyên đề KHÔNG còn nằm trong danh sách đã tick ở Bước 1
                                # (Dù dòng đó đã nhập số câu hay ghi chú thì vẫn tự động bỏ để khớp 100% với Bước 1)
                                kept_rows = []
                                for r in old_rows:
                                    r_top = r.get("topic", "")
                                    r_top_lbl = ID_TO_LABEL.get(r_top, r_top)
                                    if r_top in sel_set or r_top in sel_ids or r_top_lbl in sel_set:
                                        r["topic"] = r_top_lbl  # Chuẩn hóa về label
                                        r["category"] = get_topic_category(r_top_lbl)
                                        kept_rows.append(r)

                                # 2. ĐẢM BẢO MỖI PHẦN CÓ ĐỦ DÒNG TƯƠNG ỨNG VỚI CÁC CHỦ ĐỀ ĐÃ CHỌN Ở BƯỚC 1
                                existing_tops = {r.get("topic") for r in kept_rows}
                                sec_type = sec.get("type", "Một lựa chọn đúng")
                                deleted_here = wizard_state.get("manually_deleted", {}).get(s_idx, set())

                                for top in sel_labels:
                                    if top not in existing_tops and top not in deleted_here:
                                        if "Một lựa chọn" in sec_type:
                                            nb_def, th_def, vd_def, vdc_def = 1, 0, 0, 0
                                            note_def = ""
                                        elif "Đúng" in sec_type:
                                            nb_def, th_def, vd_def, vdc_def = 0, 0, 1, 0
                                            note_def = "Bài toán thực tế 4 ý a,b,c,d"
                                        else:
                                            nb_def, th_def, vd_def, vdc_def = 0, 0, 1, 0
                                            note_def = "Đáp số nguyên hoặc thập phân gọn"

                                        kept_rows.append({
                                            "category": get_topic_category(top),
                                            "topic": top,
                                            "note": note_def,
                                            "nb": nb_def,
                                            "th": th_def,
                                            "vd": vd_def,
                                            "vdc": vdc_def,
                                        })

                                sec["rows"] = kept_rows

                            wizard_state["step"] = 2
                            render_wizard_content()

                        ui.button(
                            "Tiếp tục: Thiết lập Bảng Ma trận (Số câu & Dạng bài) ➜",
                            on_click=proceed_to_step_2,
                            color="primary",
                        ).props("unelevated no-caps").classes("font-bold px-5 py-2 rounded-xl")

            # =========================================================
            # NỘI DUNG BƯỚC 2: BẢNG MA TRẬN (SỐ CÂU & COMBOBOX CHỌN CĐ)
            # =========================================================
            elif step == 2:
                # Danh sách các lựa chọn trong combobox: BẮT BUỘC chỉ theo các chuyên đề đã tick chọn ở Bước 1
                sel_labels = []
                for cid in wizard_state.get("selected_topics", []):
                    lbl = ID_TO_LABEL.get(cid, cid)
                    if lbl and lbl not in sel_labels:
                        sel_labels.append(lbl)
                
                # Nếu chưa có sel_labels (ví dụ template cũ nạp vào), suy ra từ các dòng hiện có
                if not sel_labels:
                    for s in wizard_state.get("sections", []):
                        for r in s.get("rows", []):
                            t = r.get("topic")
                            if t and t not in sel_labels:
                                sel_labels.append(t)

                combobox_options = list(sel_labels) if sel_labels else list(ALL_TOPIC_LABELS)

                row_tot_labels = {}
                sec_summary_widgets = {}

                def update_step2_stats():
                    for s_i, s_obj in enumerate(wizard_state.get("sections", [])):
                        s_rows = s_obj.get("rows", [])
                        for r_i, r_obj in enumerate(s_rows):
                            rt = int(r_obj.get("nb") or 0) + int(r_obj.get("th") or 0) + int(r_obj.get("vd") or 0) + int(r_obj.get("vdc") or 0)
                            if (s_i, r_i) in row_tot_labels:
                                row_tot_labels[(s_i, r_i)].set_text(str(rt))

                        s_nb = sum(int(r.get("nb") or 0) for r in s_rows)
                        s_th = sum(int(r.get("th") or 0) for r in s_rows)
                        s_vd = sum(int(r.get("vd") or 0) for r in s_rows)
                        s_vdc = sum(int(r.get("vdc") or 0) for r in s_rows)
                        s_tot = s_nb + s_th + s_vd + s_vdc
                        p_nb = f"{(s_nb/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                        p_th = f"{(s_th/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                        p_vd = f"{(s_vd/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                        p_vdc = f"{(s_vdc/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                        s_pts = s_tot * 0.25 if "Một lựa chọn" in s_obj.get("type", "") else (s_tot * 1.0 if "Đúng" in s_obj.get("type", "") else s_tot * 0.5)

                        if s_i in sec_summary_widgets:
                            sw = sec_summary_widgets[s_i]
                            sw["pts_title"].set_text(f"Tổng kết {s_obj.get('title', 'Phần')} ({s_pts:.2f} điểm)")
                            sw["nb"].set_text(str(s_nb))
                            sw["p_nb"].set_text(p_nb)
                            sw["th"].set_text(str(s_th))
                            sw["p_th"].set_text(p_th)
                            sw["vd"].set_text(str(s_vd))
                            sw["p_vd"].set_text(p_vd)
                            sw["vdc"].set_text(str(s_vdc))
                            sw["p_vdc"].set_text(p_vdc)
                            sw["tot"].set_text(str(s_tot))

                    tot_st = calc_matrix_summary(wizard_state.get("sections", []))
                    dur = wizard_state.get("duration", 90)
                    global_badge.set_text(f"{tot_st['total_q']} câu • {tot_st['points']:.2f} điểm • ⏱️ {dur} phút")
                    t_tot = tot_st['total_q']
                    nb_p = f"{(tot_st['nb']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                    th_p = f"{(tot_st['th']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                    vd_p = f"{(tot_st['vd']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                    vdc_p = f"{(tot_st['vdc']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                    global_distrib_lbl.set_text(
                        f"Nhận biết: {tot_st['nb']} câu ({nb_p}) | Thông hiểu: {tot_st['th']} câu ({th_p}) | Vận dụng: {tot_st['vd']} câu ({vd_p}) | Vận dụng cao: {tot_st['vdc']} câu ({vdc_p})"
                    )

                with ui.column().classes("w-full gap-3"):
                    # Thông tin chung ma trận
                    with ui.row().classes("w-full items-center justify-between gap-3 p-3 rounded-xl bg-slate-50 border border-slate-200 flex-wrap"):
                        with ui.row().classes("items-center gap-2 flex-1"):
                            ui.input(label="Tên Ma trận Đề thi").bind_value(wizard_state, "title").props("outlined dense").classes("flex-1 bg-white text-sm font-semibold")
                            dur_inp = ui.number(label="Thời gian (phút)", min=15, max=180).bind_value(wizard_state, "duration").props("outlined dense").classes("w-32 bg-white text-sm font-semibold")
                            dur_inp.on("update:model-value", lambda _: update_step2_stats())
                            ui.select(
                                ["Toán 12 - Tốt nghiệp THPT 2026", "Toán 11 - GDPT 2018", "Toán 10 - GDPT 2018"],
                                label="Khối / Lớp",
                            ).bind_value(wizard_state, "grade").props("outlined dense").classes("w-56 bg-white text-sm")

                        ui.button("⬅ Chọn lại Chuyên đề (Bước 1)", on_click=lambda: switch_step(1), color="slate-200").props("unelevated no-caps size=sm").classes("text-slate-800 font-semibold px-3 py-2 rounded-xl")

                    # Danh sách các Phần thi (Sections)
                    sections_scroll = ui.column().classes("w-full max-h-[50vh] overflow-y-auto gap-4 pr-1")
                    with sections_scroll:
                        for s_idx, sec in enumerate(wizard_state.get("sections", [])):
                            with ui.card().classes("w-full p-4 rounded-2xl border border-slate-300 bg-white gap-3 shadow-xs"):
                                # Header Phần
                                with ui.row().classes("w-full items-center justify-between no-wrap gap-3 pb-1 border-b border-slate-100"):
                                    with ui.row().classes("items-center gap-2 flex-1"):
                                        ui.label(f"{sec.get('title', f'Phần {s_idx+1}')}").classes("text-base font-bold text-slate-900 shrink-0")
                                        ui.input(placeholder="Mô tả phần").bind_value(sec, "subtitle").props("rounded outlined dense").classes("w-44 text-sm bg-white")
                                        sec_type_sel = ui.select(
                                            ["Một lựa chọn đúng", "Đúng / Sai", "Trả lời ngắn"],
                                            value=sec.get("type", "Một lựa chọn đúng"),
                                        ).bind_value(sec, "type").props("rounded outlined dense").classes("w-48 text-sm bg-white")
                                        sec_type_sel.on("update:model-value", lambda _: update_step2_stats())

                                    def remove_sec(idx=s_idx):
                                        if len(wizard_state["sections"]) > 1:
                                            del wizard_state["sections"][idx]
                                            render_wizard_content()
                                        else:
                                            ui.notify("Cần giữ lại ít nhất 1 Phần thi!", type="warning")

                                    ui.button(icon="delete", on_click=remove_sec).props("flat round dense size=sm color=red-400").tooltip("Xóa Phần này")

                                # Bảng câu hỏi của phần này
                                with ui.column().classes("w-full gap-2 mt-1"):
                                    # Header các cột
                                    with ui.row().classes("w-full items-center px-2 text-xs font-semibold text-slate-600 gap-2"):
                                        ui.label("Chủ đề / Chuyên đề (Combobox chọn)").classes("w-64")
                                        ui.label("Dạng câu hỏi / Ý tưởng riêng ('câu gì câu gì')").classes("flex-1")
                                        ui.label("NB").classes("w-14 text-center")
                                        ui.label("TH").classes("w-14 text-center")
                                        ui.label("VD").classes("w-14 text-center")
                                        ui.label("VDC").classes("w-14 text-center")
                                        ui.label("Tổng").classes("w-10 text-center font-bold")
                                        ui.label("").classes("w-7")

                                    # Danh sách dòng
                                    for r_idx, row in enumerate(sec.get("rows", [])):
                                        with ui.column().classes("w-full gap-0.5"):
                                            # Hiển thị tên nhóm / chương nhỏ phía trên
                                            init_cat = row.get("category") or get_topic_category(row.get("topic", ""))
                                            cat_lbl = ui.label(init_cat).classes("text-[10px] text-slate-400 italic pl-3 -mb-1")

                                            with ui.row().classes("w-full items-center gap-2"):
                                                # Cột 1: COMBOBOX CHỌN CHỦ ĐỀ (CHỈ HIỂN THỊ CÁC CHỦ ĐỀ ĐÃ TICK Ở BƯỚC 1)
                                                curr_topic = row.get("topic")
                                                if (not curr_topic or curr_topic not in combobox_options) and combobox_options:
                                                    curr_topic = combobox_options[0]
                                                    row["topic"] = curr_topic
                                                    row["category"] = get_topic_category(curr_topic)
                                                    cat_lbl.set_text(row["category"])

                                                top_sel = ui.select(
                                                    options=combobox_options,
                                                    value=curr_topic,
                                                    with_input=True,
                                                    new_value_mode="add-unique",
                                                ).props("rounded outlined dense options-dense").classes("w-64 text-xs bg-white font-medium")

                                                def on_topic_pick(e, r_ref=row, c_w=cat_lbl):
                                                    r_ref["topic"] = e.value
                                                    r_ref["category"] = get_topic_category(e.value)
                                                    c_w.set_text(r_ref["category"])

                                                top_sel.on("update:model-value", on_topic_pick)

                                                # Cột 2: DẠNG CÂU HỎI / GỢI Ý RIÊNG ('CÂU GÌ CÂU GÌ')
                                                ui.input(
                                                    placeholder="Dạng câu (VD: Nhận dạng đồ thị, Cực trị chứa m...)",
                                                    value=row.get("note", ""),
                                                ).bind_value(row, "note").props("rounded outlined dense").classes("flex-1 text-xs bg-white").tooltip("Ghi chú dạng câu hỏi cụ thể ('câu gì câu gì')")

                                                # 4 Ô số mức độ: NB, TH, VD, VDC (Cập nhật in-place, KHÔNG nhảy scroll)
                                                def make_w_box(field_name, r_ref=row):
                                                    inp = ui.number(
                                                        value=r_ref.get(field_name, 0),
                                                        min=0, max=50,
                                                    ).bind_value(r_ref, field_name).props("rounded outlined dense").classes("w-14 text-center font-semibold bg-white")
                                                    inp.on("update:model-value", lambda _: update_step2_stats())
                                                    return inp

                                                make_w_box("nb")
                                                make_w_box("th")
                                                make_w_box("vd")
                                                make_w_box("vdc")

                                                # Tổng câu của dòng
                                                row_tot = int(row.get("nb") or 0) + int(row.get("th") or 0) + int(row.get("vd") or 0) + int(row.get("vdc") or 0)
                                                rt_lbl = ui.label(str(row_tot)).classes("w-10 text-center font-bold text-slate-800")
                                                row_tot_labels[(s_idx, r_idx)] = rt_lbl

                                                # Nút xóa dòng
                                                def delete_w_row(s_i=s_idx, r_i=r_idx):
                                                    del_topic = wizard_state["sections"][s_i]["rows"][r_i].get("topic")
                                                    del wizard_state["sections"][s_i]["rows"][r_i]
                                                    if del_topic:
                                                        wizard_state.setdefault("manually_deleted", {}).setdefault(s_i, set()).add(del_topic)
                                                    render_wizard_content()

                                                ui.button("✕", on_click=delete_w_row).props("flat dense round size=xs").classes(
                                                    "w-7 h-7 rounded-full border border-red-300 text-red-500 hover:bg-red-50 font-bold shrink-0"
                                                )

                                    # Footer tổng kết của phần này
                                    s_nb = sum(int(r.get("nb") or 0) for r in sec.get("rows", []))
                                    s_th = sum(int(r.get("th") or 0) for r in sec.get("rows", []))
                                    s_vd = sum(int(r.get("vd") or 0) for r in sec.get("rows", []))
                                    s_vdc = sum(int(r.get("vdc") or 0) for r in sec.get("rows", []))
                                    s_tot = s_nb + s_th + s_vd + s_vdc
                                    p_nb = f"{(s_nb/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                                    p_th = f"{(s_th/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                                    p_vd = f"{(s_vd/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                                    p_vdc = f"{(s_vdc/s_tot*100):.0f}%" if s_tot > 0 else "0%"
                                    s_pts = s_tot * 0.25 if "Một lựa chọn" in sec.get("type", "") else (s_tot * 1.0 if "Đúng" in sec.get("type", "") else s_tot * 0.5)

                                    with ui.row().classes("w-full items-center px-2 py-2 border-t border-dashed border-slate-300 mt-2 text-slate-800 gap-2"):
                                        pts_t_lbl = ui.label(f"Tổng kết {sec.get('title', 'Phần')} ({s_pts:.2f} điểm)").classes("flex-1 font-bold text-xs text-blue-900")

                                        with ui.column().classes("w-14 items-center gap-0"):
                                            w_nb = ui.label(str(s_nb)).classes("font-bold text-xs")
                                            w_p_nb = ui.label(p_nb).classes("text-[9px] text-slate-500")

                                        with ui.column().classes("w-14 items-center gap-0"):
                                            w_th = ui.label(str(s_th)).classes("font-bold text-xs")
                                            w_p_th = ui.label(p_th).classes("text-[9px] text-slate-500")

                                        with ui.column().classes("w-14 items-center gap-0"):
                                            w_vd = ui.label(str(s_vd)).classes("font-bold text-xs")
                                            w_p_vd = ui.label(p_vd).classes("text-[9px] text-slate-500")

                                        with ui.column().classes("w-14 items-center gap-0"):
                                            w_vdc = ui.label(str(s_vdc)).classes("font-bold text-xs")
                                            w_p_vdc = ui.label(p_vdc).classes("text-[9px] text-slate-500")

                                        w_tot = ui.label(str(s_tot)).classes("w-10 text-center font-bold text-sm text-slate-900")
                                        ui.label("").classes("w-7")

                                        sec_summary_widgets[s_idx] = {
                                            "pts_title": pts_t_lbl,
                                            "nb": w_nb, "p_nb": w_p_nb,
                                            "th": w_th, "p_th": w_p_th,
                                            "vd": w_vd, "p_vd": w_p_vd,
                                            "vdc": w_vdc, "p_vdc": w_p_vdc,
                                            "tot": w_tot,
                                        }

                                # Các nút thêm dòng trong phần này
                                with ui.row().classes("w-full items-center gap-2 pt-1"):
                                    def add_row_to_sec(s_i=s_idx):
                                        default_top = combobox_options[0] if combobox_options else "Chuyên đề mới"
                                        wizard_state["sections"][s_i].setdefault("rows", []).append({
                                            "category": get_topic_category(default_top),
                                            "topic": default_top,
                                            "note": "",
                                            "nb": 1, "th": 1, "vd": 0, "vdc": 0,
                                        })
                                        render_wizard_content()

                                    ui.button(
                                        "➕ Thêm dòng chủ đề",
                                        on_click=add_row_to_sec,
                                        color="slate-100",
                                    ).props("unelevated size=xs no-caps").classes("text-slate-800 font-semibold px-2.5 py-1 rounded-lg border border-slate-200")

                                    def auto_fill_sec_topics(s_i=s_idx):
                                        existing = {r["topic"] for r in wizard_state["sections"][s_i].get("rows", [])}
                                        wizard_state.setdefault("manually_deleted", {})[s_i] = set()
                                        count = 0
                                        for cid in wizard_state.get("selected_topics", []):
                                            lbl = ID_TO_LABEL.get(cid, cid)
                                            if lbl not in existing:
                                                wizard_state["sections"][s_i].setdefault("rows", []).append({
                                                    "category": get_topic_category(lbl),
                                                    "topic": lbl,
                                                    "note": "",
                                                    "nb": 1, "th": 0, "vd": 0, "vdc": 0,
                                                })
                                                count += 1
                                        if count > 0:
                                            ui.notify(f"✓ Đã thêm {count} chuyên đề đã tick vào phần này!", type="positive")
                                            render_wizard_content()
                                        else:
                                            ui.notify("Tất cả chuyên đề đã tick đều đã có trong phần này!", type="info")

                                    ui.button(
                                        "⚡ Thêm nhanh tất cả CĐ đã tick vào phần này",
                                        on_click=auto_fill_sec_topics,
                                        color="indigo-50",
                                    ).props("unelevated size=xs no-caps").classes("text-indigo-800 font-semibold px-2.5 py-1 rounded-lg border border-indigo-200")

                        # Nút thêm Phần mới
                        def add_new_wizard_sec():
                            sec_n = len(wizard_state["sections"]) + 1
                            sec_rows = []
                            for top in combobox_options:
                                sec_rows.append({
                                    "category": get_topic_category(top),
                                    "topic": top,
                                    "note": "",
                                    "nb": 1, "th": 0, "vd": 0, "vdc": 0,
                                })
                            wizard_state["sections"].append({
                                "id": f"sec_{sec_n}",
                                "title": f"Phần {sec_n}",
                                "subtitle": f"Phần {sec_n}",
                                "type": "Một lựa chọn đúng",
                                "rows": sec_rows,
                            })
                            render_wizard_content()

                        ui.button("➕ Thêm Phần thi mới (Section)", on_click=add_new_wizard_sec, color="slate-100").props(
                            "unelevated no-caps size=sm"
                        ).classes("text-slate-800 font-bold px-3 py-1.5 rounded-xl border border-slate-200")

                    # Thẻ tóm tắt toàn bộ ma trận ở chân bảng
                    total_stats = calc_matrix_summary(wizard_state.get("sections", []))
                    with ui.card().classes("w-full p-3 rounded-xl bg-gradient-to-r from-blue-900 via-indigo-900 to-blue-800 text-white gap-1"):
                        with ui.row().classes("w-full items-center justify-between"):
                            ui.label("🎯 TỔNG CỘNG TOÀN BỘ MA TRẬN ĐỀ THI:").classes("text-xs font-bold text-blue-200 uppercase tracking-wider")
                            global_badge = ui.badge(f"{total_stats['total_q']} câu • {total_stats['points']:.2f} điểm • ⏱️ {wizard_state['duration']} phút", color="emerald-600").classes("text-xs font-bold px-3 py-1")
                        with ui.row().classes("w-full items-center justify-between text-xs text-blue-100 pt-1"):
                            t_tot = total_stats['total_q']
                            nb_p = f"{(total_stats['nb']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                            th_p = f"{(total_stats['th']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                            vd_p = f"{(total_stats['vd']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                            vdc_p = f"{(total_stats['vdc']/t_tot*100):.1f}%" if t_tot > 0 else "0%"
                            global_distrib_lbl = ui.label(f"Nhận biết: {total_stats['nb']} câu ({nb_p}) | Thông hiểu: {total_stats['th']} câu ({th_p}) | Vận dụng: {total_stats['vd']} câu ({vd_p}) | Vận dụng cao: {total_stats['vdc']} câu ({vdc_p})")

                    # Chân Bước 2: Nút lưu & áp dụng
                    with ui.row().classes("w-full items-center justify-between pt-3 border-t border-slate-200"):
                        ui.button("⬅ Quay lại Bước 1: Chọn chuyên đề", on_click=lambda: switch_step(1)).props("flat no-caps").classes("text-slate-700 font-semibold px-4")

                        def save_matrix_template_data(and_generate=False):
                            curr_tot = calc_matrix_summary(wizard_state.get("sections", []))
                            m_id = wizard_state.get("id") or f"mat_{int(time.time()*1000)}"
                            m_title = wizard_state.get("title", "").strip() or "Ma trận Đề thi"
                            tpl_data = {
                                "id": m_id,
                                "title": m_title,
                                "desc": f"Cấu trúc: {curr_tot['total_q']} câu ({curr_tot['points']:.2f}đ), {wizard_state['duration']} phút",
                                "duration": int(wizard_state.get("duration", 90)),
                                "grade": wizard_state.get("grade", "Toán 12 - Tốt nghiệp THPT 2026"),
                                "selected_topics": list(wizard_state.get("selected_topics", [])),
                                "sections": json.loads(json.dumps(wizard_state.get("sections", []))),
                                "updated_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            }
                            # Lưu vào danh sách templates
                            all_tpls = load_matrix_templates()
                            idx = next((i for i, x in enumerate(all_tpls) if x.get("id") == m_id), None)
                            if idx is not None:
                                all_tpls[idx] = tpl_data
                            else:
                                all_tpls.append(tpl_data)
                            save_matrix_templates(all_tpls)

                            # Áp dụng vào state hiện tại
                            apply_matrix_template(tpl_data)
                            matrix_wizard_dialog.close()
                            ui.notify(f"✓ Đã lưu Ma trận '{m_title}' vào danh sách!", type="positive")
                            return tpl_data

                        with ui.row().classes("items-center gap-2"):
                            ui.button("💾 Lưu vào Danh sách Ma trận", on_click=lambda: save_matrix_template_data(False), color="slate-200").props(
                                "unelevated no-caps"
                            ).classes("text-slate-800 font-semibold px-4 py-2 rounded-xl")

                            async def save_and_gen():
                                save_matrix_template_data(True)
                                await on_generate_matrix()

                            ui.button("🚀 Áp dụng & Tạo Đề Ngay", on_click=save_and_gen, color="primary").props(
                                "unelevated no-caps"
                            ).classes("font-bold px-5 py-2 rounded-xl shadow-md")

    with matrix_wizard_dialog, ui.card().classes("w-[1140px] max-w-[98vw] max-h-[94vh] p-6 rounded-2xl gap-3 flex flex-col"):
        with ui.row().classes("w-full items-center justify-between pb-1 border-b border-slate-200"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("table_view", size="26px").classes("text-blue-700")
                with ui.column().classes("gap-0"):
                    ui.label("Thiết lập Ma trận Đề thi Chuẩn GDPT 2018").classes("text-lg font-bold text-slate-800")
                    ui.label("Quy trình 2 bước: Tick chọn chuyên đề -> Thiết lập combobox chủ đề, số câu & dạng câu hỏi.").classes("text-xs text-slate-500")
            ui.button(icon="close", on_click=matrix_wizard_dialog.close).props("flat round dense")

        wizard_body_container = ui.column().classes("w-full flex-1 overflow-y-auto pr-1 gap-2")

    def start_new_matrix_wizard():
        wizard_state["id"] = f"mat_{int(time.time()*1000)}"
        wizard_state["title"] = "Ma trận Đề thi Mới"
        wizard_state["desc"] = ""
        wizard_state["duration"] = 90
        wizard_state["grade"] = "Toán 12 - Tốt nghiệp THPT 2026"
        wizard_state["selected_topics"] = []
        wizard_state["manually_deleted"] = {}
        wizard_state["sections"] = [
            {"id": "sec_1", "title": "Phần I", "subtitle": "Một lựa chọn đúng", "type": "Một lựa chọn đúng", "rows": []},
            {"id": "sec_2", "title": "Phần II", "subtitle": "Đúng / Sai", "type": "Đúng / Sai", "rows": []},
            {"id": "sec_3", "title": "Phần III", "subtitle": "Trả lời ngắn", "type": "Trả lời ngắn", "rows": []},
        ]
        wizard_state["step"] = 1
        render_wizard_content()
        matrix_wizard_dialog.open()

    def edit_matrix_wizard(tpl: dict):
        wizard_state["id"] = tpl.get("id", f"mat_{int(time.time()*1000)}")
        wizard_state["title"] = tpl.get("title", "Ma trận Đề thi")
        wizard_state["desc"] = tpl.get("desc", "")
        wizard_state["duration"] = tpl.get("duration", 90)
        wizard_state["grade"] = tpl.get("grade", "Toán 12 - Tốt nghiệp THPT 2026")
        wizard_state["manually_deleted"] = {}

        sel_t = list(tpl.get("selected_topics", []))
        if not sel_t:
            for s in tpl.get("sections", []):
                for r in s.get("rows", []):
                    top = r.get("topic")
                    if top:
                        m_id = next((k for k, v in ID_TO_LABEL.items() if v == top), top)
                        if m_id not in sel_t:
                            sel_t.append(m_id)
        wizard_state["selected_topics"] = sel_t
        wizard_state["sections"] = json.loads(json.dumps(tpl.get("sections", [])))
        wizard_state["step"] = 2
        render_wizard_content()
        matrix_wizard_dialog.open()

    def edit_current_matrix_wizard():
        current_tpl = {
            "id": state.get("active_matrix_id", "mat_curr"),
            "title": state.get("active_matrix_title", "Ma trận Đang Sử Dụng"),
            "desc": "",
            "duration": state.get("duration", 90),
            "grade": state.get("grade", "Toán 12 - Tốt nghiệp THPT 2026"),
            "selected_topics": list(state.get("selected_topics", [])),
            "sections": json.loads(json.dumps(state.get("matrix_sections", []))),
        }
        edit_matrix_wizard(current_tpl)

    def apply_matrix_template(tpl: dict):
        state["active_matrix_id"] = tpl.get("id", "")
        state["active_matrix_title"] = tpl.get("title", "Ma trận Đề thi")
        state["duration"] = tpl.get("duration", 90)
        state["grade"] = tpl.get("grade", "Toán 12 - Tốt nghiệp THPT 2026")
        state["selected_topics"] = list(tpl.get("selected_topics", []))
        state["matrix_sections"] = json.loads(json.dumps(tpl.get("sections", [])))
        stats = calc_matrix_summary()
        state["mcq"] = stats["p1_q"]
        state["tf"] = stats["p2_q"]
        state["sa"] = stats["p3_q"]
        update_matrix_ui()

    def open_matrix_modal():
        edit_current_matrix_wizard()

    def open_matrix_list_dialog():
        render_matrix_list()
        matrix_list_dialog.open()

    def open_tree_modal():
        render_tree_modal_content()
        tree_dialog.open()

    # -----------------------------------------------------------------
    # HỘP THOẠI THIẾT LẬP Ý TƯỞNG RIÊNG CHO TỪNG CÂU (BLUEPRINT BUILDER)
    # -----------------------------------------------------------------
    blueprint_dialog = ui.dialog()

    def sync_blueprint_items():
        n_mcq = int(state.get("mcq") or 0)
        n_tf = int(state.get("tf") or 0)
        n_sa = int(state.get("sa") or 0)
        old_map = {
            (it["part"], it["label"]): it for it in state.get("blueprint_items", [])
        }
        new_items = []
        for i in range(1, n_mcq + 1):
            key = ("PHẦN I (4 lựa chọn)", f"Câu {i}")
            default_lvl = "Nhận biết" if i <= 2 else ("Thông hiểu" if i <= 4 else "Vận dụng")
            new_items.append(
                old_map.get(
                    key,
                    {"part": key[0], "label": key[1], "level": default_lvl, "idea": "", "image": None},
                )
            )
        for i in range(1, n_tf + 1):
            key = ("PHẦN II (Đúng/Sai)", f"Câu {i}")
            new_items.append(
                old_map.get(
                    key,
                    {"part": key[0], "label": key[1], "level": "Thông hiểu", "idea": "", "image": None},
                )
            )
        for i in range(1, n_sa + 1):
            key = ("PHẦN III (Trả lời ngắn)", f"Câu {i}")
            default_lvl = "Vận dụng" if i == 1 else "Vận dụng cao"
            new_items.append(
                old_map.get(
                    key,
                    {"part": key[0], "label": key[1], "level": default_lvl, "idea": "", "image": None},
                )
            )
        state["blueprint_items"] = new_items

    # Hộp thoại phóng to xem ảnh ý tưởng
    bp_image_viewer_dialog = ui.dialog()
    with bp_image_viewer_dialog, ui.card().classes("w-[720px] max-w-[95vw] p-4 rounded-2xl gap-2 items-center"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("🔍 Ảnh ý tưởng / hình vẽ minh họa").classes("text-sm font-bold text-slate-700")
            ui.button(icon="close", on_click=bp_image_viewer_dialog.close).props("flat round dense")
        large_bp_preview = ui.image().classes("w-full max-h-[75vh] object-contain rounded-xl border border-slate-200")

    def open_image_viewer(path_str):
        large_bp_preview.set_source(str(path_str))
        large_bp_preview.force_reload()
        bp_image_viewer_dialog.open()

    # Hộp thoại tải ảnh ý tưởng cho từng câu
    upload_bp_img_dialog = ui.dialog()
    upload_bp_img_state = {"item": None, "title": ""}
    with upload_bp_img_dialog, ui.card().classes("w-[480px] max-w-[92vw] p-5 rounded-2xl gap-3"):
        with ui.row().classes("w-full items-center justify-between"):
            upload_bp_lbl = ui.label("📷 Đính kèm Ảnh Ý tưởng").classes("text-base font-bold text-slate-800")
            ui.button(icon="close", on_click=upload_bp_img_dialog.close).props("flat round dense")

        bp_upload_preview = ui.image().classes("w-full max-h-52 object-contain rounded-xl border border-slate-200 hidden bg-slate-50")

        def handle_bp_upload(e):
            it = upload_bp_img_state["item"]
            if not it:
                return
            ext = Path(e.name).suffix or ".png"
            slug = slugify_vn(f"{it['part']}_{it['label']}")
            save_name = f"{slug}_{int(time.time())}{ext}"
            target_path = BP_IMG_DIR / save_name
            target_path.write_bytes(e.content.read())
            it["image"] = str(target_path)
            bp_upload_preview.set_source(str(target_path))
            bp_upload_preview.force_reload()
            bp_upload_preview.classes(remove="hidden")
            ui.notify(f"✓ Đã lưu ảnh ý tưởng cho {it['label']}!", type="positive")
            render_blueprint_rows()

        ui.upload(
            label="Chọn hoặc kéo thả ảnh minh họa (PNG, JPG, JPEG)",
            on_upload=handle_bp_upload,
            auto_upload=True,
        ).props("accept=.png,.jpg,.jpeg flat bordered").classes("w-full")

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Đóng", on_click=upload_bp_img_dialog.close, color="primary").props("unelevated no-caps")

    def open_upload_bp_img(item):
        upload_bp_img_state["item"] = item
        upload_bp_img_state["title"] = f"{item['part']} - {item['label']}"
        upload_bp_lbl.set_text(f"📷 Đính kèm Ảnh Ý tưởng ({item['part']} - {item['label']})")
        if item.get("image") and Path(item["image"]).exists():
            bp_upload_preview.set_source(str(item["image"]))
            bp_upload_preview.force_reload()
            bp_upload_preview.classes(remove="hidden")
        else:
            bp_upload_preview.classes(add="hidden")
        upload_bp_img_dialog.open()

    with blueprint_dialog, ui.card().classes("w-[920px] max-w-[96vw] p-6 rounded-2xl gap-3"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.column().classes("gap-0"):
                ui.label("🎯 Thiết lập Ý tưởng, Mức độ & Ảnh mẫu cho từng câu hỏi").classes(
                    "text-lg font-bold text-slate-800"
                )
                ui.label(
                    "Nhập yêu cầu dạng toán riêng hoặc đính kèm ảnh mẫu (đồ thị, hình vẽ, sơ đồ). Câu nào để trống AI sẽ tự sáng tạo theo chuyên đề."
                ).classes("text-xs text-slate-500")
            ui.button(icon="close", on_click=blueprint_dialog.close).props("flat round dense")

        bp_rows_container = ui.column().classes(
            "w-full max-h-[58vh] overflow-y-auto gap-2.5 pr-2 py-1"
        )

        def fill_sample_blueprint():
            sync_blueprint_items()
            mcq_samples_2026 = [
                "Đồ thị & Bảng biến thiên: Nhận dạng đồ thị hàm số bậc 3 y = ax^3 + bx^2 + cx + d (dấu a, c, d, cực trị)",
                "Đồ thị & Tiệm cận: Nhận dạng đồ thị hàm nhất biến y = (ax+b)/(cx+d) hoặc tiệm cận xiên hàm bậc 2/1",
                "Đồ thị Đạo hàm: Cho đồ thị hàm số đạo hàm y = f'(x), tìm khoảng đơn điệu hoặc số điểm cực trị của f(x)",
                "Hình học không gian: Tính góc giữa hai mặt phẳng hoặc góc giữa đường thẳng và mặt phẳng trong khối chóp",
                "Hình học không gian: Tính thể tích khối chóp tứ giác đều hoặc lăng trụ tam giác đứng",
                "Hình học Oxyz: Tọa độ vectơ, tích vô hướng hoặc tọa độ tâm và bán kính mặt cầu (S)",
                "Hình học Oxyz: Viết phương trình mặt phẳng đi qua 3 điểm hoặc tiếp xúc mặt cầu",
                "Hình học Oxyz: Viết phương trình đường thẳng là giao tuyến hoặc đường vuông góc chung",
                "Mũ & Logarit: Tập nghiệm phương trình hoặc bất phương trình logarit cơ bản",
                "Nguyên hàm - Tích phân: Tìm họ nguyên hàm hoặc tính tích phân xác định hàm phân thức/lượng giác",
                "Ứng dụng Tích phân: Tính diện tích hình phẳng giới hạn bởi parabol và đường thẳng",
                "Thống kê ghép nhóm: Tính khoảng biến thiên, khoảng tứ phân vị Delta_Q hoặc độ lệch chuẩn",
            ]
            tf_samples_2026 = [
                "Khảo sát hàm số & Phân tích Đồ thị/BBT (4 ý a,b,c,d từ Nhận biết đến Vận dụng cao: tiệm cận đứng/ngang/xiên, cực trị, tương giao f(x) = m, bài toán min-max trên đoạn)",
                "Hình học không gian & Gắn hệ trục Oxyz (4 ý a,b,c,d: thiết lập tọa độ các đỉnh khối chóp/hộp, tính góc nhị diện, khoảng cách giữa 2 đường chéo nhau, thể tích)",
                "Hình học thực tế ứng dụng (4 ý a,b,c,d: mô hình kiến trúc mái vòm/ngọn hải đăng/radar, tính toán góc nghiêng đón nắng, chi phí sơn/vật liệu tối ưu)",
                "Xác suất có điều kiện & Công thức Bayes trong đời sống (4 ý a,b,c,d: xét nghiệm y tế, tỷ lệ sản phẩm lỗi của 2 phân xưởng, xác suất hậu nghiệm)",
            ]
            sa_samples_2026 = [
                "Hình học không gian: Tính khoảng cách giữa hai đường thẳng chéo nhau trong khối lăng trụ đứng",
                "Hình học Oxyz thực tiễn: Thiết lập hệ tọa độ Oxyz xác định tọa độ va chạm của máy bay hoặc trạm radar phát hiện tàu thuyền",
                "Bài toán tối ưu hóa hình học bằng Đạo hàm (Thiết kế bể chứa nước, lều bạt hình chóp có diện tích vải bạt nhỏ nhất)",
                "Ứng dụng Tích phân thực tế: Tính thể tích chiếc thùng rượu gỗ dạng khối tròn xoay hoặc khối bê tông uốn lượn",
                "Đồ thị & Tương giao hàm số: Tìm số giá trị nguyên của tham số m để phương trình f(x) = m có 4 nghiệm phân biệt",
                "Xác suất nâng cao: Bài toán công thức Bayes hoặc xác suất toàn phần trong mô hình kinh tế/đầu tư rủi ro",
            ]
            m_i, t_i, s_i = 0, 0, 0
            for item in state["blueprint_items"]:
                if item["part"].startswith("PHẦN I"):
                    item["idea"] = mcq_samples_2026[m_i % len(mcq_samples_2026)]
                    item["level"] = "Nhận biết" if m_i < 6 else ("Thông hiểu" if m_i < 10 else "Vận dụng")
                    m_i += 1
                elif "PHẦN II" in item["part"]:
                    item["idea"] = tf_samples_2026[t_i % len(tf_samples_2026)]
                    item["level"] = "Vận dụng"
                    t_i += 1
                else:
                    item["idea"] = sa_samples_2026[s_i % len(sa_samples_2026)]
                    item["level"] = "Vận dụng" if s_i < 3 else "Vận dụng cao"
                    s_i += 1
            render_blueprint_rows()

        def clear_blueprint():
            for item in state["blueprint_items"]:
                item["idea"] = ""
                item["image"] = None
            render_blueprint_rows()

        def render_blueprint_rows():
            bp_rows_container.clear()
            with bp_rows_container:
                curr_part = None
                for idx, item in enumerate(state["blueprint_items"]):
                    if item["part"] != curr_part:
                        curr_part = item["part"]
                        ui.label(f"📌 {curr_part}").classes(
                            "text-xs font-bold text-indigo-800 uppercase tracking-wider mt-2"
                        )
                    with ui.column().classes("w-full bg-slate-50 p-2.5 rounded-xl border border-slate-200 gap-1.5"):
                        with ui.row().classes("w-full items-center gap-2 no-wrap"):
                            ui.badge(item["label"], color="blue-700").classes(
                                "px-2.5 py-1 text-xs font-bold shrink-0"
                            )
                            ui.select(
                                ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"],
                                value=item["level"],
                                label="Mức độ",
                            ).bind_value(item, "level").props("dense outlined").classes("w-32 shrink-0")
                            ui.input(
                                label=f"Ý tưởng / Dạng toán riêng ({item['label']})",
                                placeholder="Bấm chip gợi ý bên dưới hoặc tự nhập...",
                                value=item["idea"],
                            ).bind_value(item, "idea").props("dense outlined clearable").classes("flex-1 min-w-0")

                            # Nút / Thumbnail đính kèm ảnh ý tưởng riêng từng câu
                            has_img = bool(item.get("image") and Path(item["image"]).exists())
                            if has_img:
                                img_path_str = item["image"]
                                with ui.row().classes(
                                    "items-center gap-1.5 shrink-0 px-2 py-1 bg-indigo-50/80 rounded-xl border border-indigo-200"
                                ):
                                    thumb = ui.image(str(img_path_str)).classes(
                                        "w-8 h-8 rounded-lg object-cover cursor-pointer border border-indigo-300 hover:scale-105 transition-transform"
                                    )
                                    thumb.on("click", lambda _, p=img_path_str: open_image_viewer(p))
                                    thumb.tooltip("🔍 Bấm để xem ảnh phóng to")

                                    def remove_item_img(it=item):
                                        it["image"] = None
                                        render_blueprint_rows()

                                    ui.button(icon="delete", on_click=remove_item_img).props(
                                        "flat round dense size=xs color=red-500"
                                    ).tooltip("Gỡ bỏ ảnh này")
                            else:
                                btn = ui.button(
                                    icon="add_photo_alternate",
                                ).props("flat round dense size=sm color=indigo-700").classes(
                                    "shrink-0 bg-white hover:bg-indigo-50 p-1.5 rounded-xl border border-slate-200 hover:border-indigo-300"
                                ).tooltip("📷 Đính kèm ảnh ý tưởng / hình vẽ mẫu")
                                btn.on("click", lambda _, it=item: open_upload_bp_img(it))

                        # Hàng chips gợi ý chọn nhanh 1-Click
                        with ui.row().classes("w-full items-center gap-1 flex-wrap pl-1"):
                            ui.label("⚡ Gợi ý:").classes("text-[10px] font-bold text-slate-400 self-center mr-0.5")
                            rel_suggestions = QUESTION_IDEA_PRESETS[(idx * 3) % len(QUESTION_IDEA_PRESETS) : (idx * 3) % len(QUESTION_IDEA_PRESETS) + 4]
                            if len(rel_suggestions) < 3:
                                rel_suggestions = QUESTION_IDEA_PRESETS[:4]
                            for chip_lbl, chip_val in rel_suggestions:
                                def pick_idea(val=chip_val, it=item):
                                    it["idea"] = val
                                    render_blueprint_rows()
                                ui.button(chip_lbl, on_click=pick_idea).props("unelevated size=xs no-caps").classes(
                                    "bg-white hover:bg-indigo-50 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded-md text-[11px]"
                                )

        with ui.row().classes("w-full items-center justify-between pt-2 border-t border-slate-200"):
            with ui.row().classes("gap-2"):
                ui.button(
                    "🪄 Tự điền Gợi ý mẫu chuẩn",
                    on_click=fill_sample_blueprint,
                    color="indigo-50",
                ).props("unelevated no-caps size=sm").classes("text-indigo-800 font-semibold px-3")
                ui.button(
                    "🗑️ Xóa trắng",
                    on_click=clear_blueprint,
                    color="slate-100",
                ).props("unelevated no-caps size=sm").classes("text-slate-600 px-3")

            with ui.row().classes("gap-2"):
                ui.button("💾 Lưu kịch bản", on_click=blueprint_dialog.close, color="slate-200").props(
                    "unelevated no-caps"
                ).classes("text-slate-800 font-semibold px-4")

                async def save_and_generate():
                    blueprint_dialog.close()
                    await on_generate_matrix()

                ui.button(
                    "🚀 Lưu & Tạo Đề Ngay theo Ý tưởng này",
                    on_click=save_and_generate,
                    color="primary",
                ).props("unelevated no-caps").classes("font-semibold px-4")

    def open_blueprint_modal():
        sync_blueprint_items()
        render_blueprint_rows()
        blueprint_dialog.open()

    # -----------------------------------------------------------------
    # HỘP THOẠI THÊM CÂU HỎI MỚI VÀO CUỐI ĐỀ (CÔ LẬP 1 CÂU MỚI + SYMPY RIÊNG)
    # -----------------------------------------------------------------
    add_q_dialog = ui.dialog()
    add_q_state = {
        "part": "PHẦN I (4 lựa chọn)",
        "level": "Vận dụng",
        "req": "Đồ thị hàm số bậc ba (nhận dạng cực trị và dấu hệ số), nghiệm đẹp",
    }
    with add_q_dialog, ui.card().classes("w-[620px] max-w-[95vw] p-6 rounded-2xl gap-3"):
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("➕ Thêm 1 câu hỏi mới vào cuối đề").classes(
                "text-lg font-bold text-slate-800"
            )
            ui.button(icon="close", on_click=add_q_dialog.close).props("flat round dense")

        with ui.row().classes("w-full gap-2"):
            ui.select(
                ["PHẦN I (4 lựa chọn)", "PHẦN II (Đúng/Sai a,b,c,d)", "PHẦN III (Trả lời ngắn)"],
                value=add_q_state["part"],
                label="Phần câu hỏi",
            ).bind_value(add_q_state, "part").props("outlined dense").classes("flex-1")

            ui.select(
                ["Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"],
                value=add_q_state["level"],
                label="Mức độ",
            ).bind_value(add_q_state, "level").props("outlined dense").classes("w-36")

        ui.label("⚡ Chọn nhanh dạng toán (1-Click điền ngay):").classes(
            "text-xs font-bold text-slate-500 uppercase tracking-wider -mb-1"
        )

        with ui.row().classes("w-full gap-1 flex-wrap"):
            for chip_lbl, chip_val in QUESTION_IDEA_PRESETS[:8]:
                def pick_add_idea(val=chip_val):
                    add_q_state["req"] = f"{val}, mức độ {add_q_state['level']}, nghiệm nguyên/phân số đẹp"
                ui.button(chip_lbl, on_click=pick_add_idea).props("unelevated size=xs no-caps").classes(
                    "bg-slate-100 hover:bg-indigo-50 text-slate-800 hover:text-indigo-900 border border-slate-200 px-2 py-1 rounded-lg text-xs"
                )

        ui.textarea(
            label="Yêu cầu câu hỏi:",
            placeholder="VD: Thêm 1 câu trắc nghiệm tìm số điểm cực trị của hàm số bậc 4 trùng phương...",
        ).bind_value(add_q_state, "req").classes("w-full")

        async def confirm_add_q():
            add_q_dialog.close()
            active_path = Path(state["active_file"])
            header_md, qs = parse_exam_markdown(
                active_path.read_text(encoding="utf-8") if active_path.exists() else ""
            )
            save_version_backup(active_path, "truoc_them_cau")
            temp_q_file = OUTPUT_DIR / "temp_single_q.md"
            temp_q_file.unlink(missing_ok=True)
            next_num = len(qs) + 1
            last_sec = qs[-1]["section"] if qs else ""

            prompt = (
                f"Hãy tạo DUY NHẤT 1 câu hỏi toán học mới theo yêu cầu: \"{add_q_state['req']}\".\n"
                f"QUY TRÌNH BẮT BUỘC:\n"
                f"1. Viết file `verify_single.py` bằng `sympy` để giải và kiểm chứng CHỈ RIÊNG câu hỏi mới này.\n"
                f"2. Chạy `verify_single.py` qua MCP tool `local-runner` (`executable: \"python\"`, `args: [\"verify_single.py\"]`, `cwd: \"D:\\\\MathAI\\\\de-toan-ai\"`).\n"
                f"3. Ghi câu hỏi mới kèm đáp án và lời giải chi tiết vào `{temp_q_file.as_posix()}` theo cấu trúc:\n"
                f"### Câu {next_num}.\n"
                f"<Đề bài và các phương án>\n\n"
                f"**Lời giải:**\n"
                f"- **Đáp án đúng:** <Đáp án>\n"
                f"- <Lời giải chi tiết từng bước>"
            )
            await execute_ai_task(
                prompt,
                active_path,
                "Đang tạo & kiểm định cho 1 câu hỏi mới...",
                use_continue=False,
                skip_backup=True,
            )
            if temp_q_file.exists():
                new_block = temp_q_file.read_text(encoding="utf-8").strip()
                if new_block:
                    qs.append(
                        {
                            "index": len(qs),
                            "section": last_sec,
                            "title": f"Câu {next_num}",
                            "stem": new_block,
                            "solution": "",
                            "full_block": new_block,
                        }
                    )
                    active_path.write_text(rebuild_exam_markdown(header_md, qs), encoding="utf-8")
                    state["open_solutions"].add(len(qs) - 1)
                    temp_q_file.unlink(missing_ok=True)
                    render_questions_workspace()

        with ui.row().classes("w-full justify-end gap-2"):
            ui.button("Hủy", on_click=add_q_dialog.close).props("flat no-caps")
            ui.button("✨ Tạo & Kiểm định câu mới", on_click=confirm_add_q, color="primary").props(
                "no-caps"
            )

    # -----------------------------------------------------------------
    # HỘP THOẠI XUẤT ĐỀ RA FILE WORD (.DOCX) CHUẨN BỘ GD&ĐT
    # -----------------------------------------------------------------
    export_word_dialog = ui.dialog()
    export_word_state = {
        "mode": "exam_only",  # exam_only | exam_and_solution | solution_only
        "school": "SỞ GIÁO DỤC VÀ ĐÀO TẠO",
        "title": "KỲ THI TỐT NGHIỆP TRUNG HỌC PHỔ THÔNG NĂM 2026",
        "code": "101",
    }

    with export_word_dialog, ui.card().classes("w-[640px] max-w-[95vw] p-6 rounded-2xl gap-3.5"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("description", size="24px").classes("text-blue-700")
                ui.label("Xuất Đề thi ra Microsoft Word (.docx)").classes("text-lg font-bold text-slate-800")
            ui.button(icon="close", on_click=export_word_dialog.close).props("flat round dense")

        ui.label(
            "Định dạng chuẩn văn bản thi của Bộ GD&ĐT (Times New Roman, lề 2cm, công thức Toán hiển thị chuẩn Native Word Equation)."
        ).classes("text-xs text-slate-500 -mt-1")

        ui.separator()

        ui.label("🎯 Chọn hình thức xuất file Word:").classes("text-xs font-bold text-slate-700 uppercase tracking-wider")
        ui.radio(
            {
                "exam_only": "📄 1. Chỉ Đề thi (Dành cho học sinh làm bài, có khung Họ tên/SBD, không có lời giải)",
                "exam_and_solution": "📑 2. Đề thi kèm Đáp án & Lời giải chi tiết (Dành cho giáo viên/tài liệu ôn tập)",
                "solution_only": "🔑 3. Riêng Đáp án & Hướng dẫn chấm (Bảng đáp án tổng hợp + Lời giải chi tiết)",
            },
            value="exam_only",
        ).bind_value(export_word_state, "mode").props("dense").classes("gap-2 text-sm text-slate-800")

        with ui.expansion("⚙️ Tùy chỉnh thông tin tiêu đề đề thi (Tên trường, mã đề)", icon="tune").classes(
            "w-full text-xs bg-slate-50 rounded-xl border border-slate-200"
        ):
            with ui.column().classes("w-full gap-2 p-2"):
                ui.input("Đơn vị / Sở / Trường").bind_value(export_word_state, "school").props("outlined dense").classes("w-full")
                ui.input("Tiêu đề kỳ thi").bind_value(export_word_state, "title").props("outlined dense").classes("w-full")
                ui.input("Mã đề thi (VD: 101, 102)").bind_value(export_word_state, "code").props("outlined dense").classes("w-36")

        def perform_word_export():
            active_p = Path(state["active_file"])
            if not active_p.exists():
                ui.notify("Không tìm thấy file đề hiện tại!", type="warning")
                return

            raw = active_p.read_text(encoding="utf-8")
            h_md, q_list = parse_exam_markdown(raw)
            if not q_list:
                ui.notify("Đề thi chưa có câu hỏi nào để xuất!", type="warning")
                return

            m = export_word_state["mode"]
            code = export_word_state["code"].strip() or "101"
            prefix_map = {
                "exam_only": f"De_thi_{code}",
                "exam_and_solution": f"De_va_Loi_giai_{code}",
                "solution_only": f"Dap_an_chi_tiet_{code}",
            }
            fname = f"{prefix_map.get(m, 'De_thi')}_{active_p.stem[:20]}.docx"
            temp_out = OUTPUT_DIR / fname

            try:
                export_exam_word(
                    header_md=h_md,
                    questions=q_list,
                    mode=m,
                    school_name=export_word_state["school"],
                    exam_title=export_word_state["title"],
                    exam_code=code,
                    output_path=temp_out,
                )
                ui.download(temp_out.read_bytes(), filename=fname)
                ui.notify(f"✓ Đã xuất file Word '{fname}' thành công!", type="positive")
                export_word_dialog.close()
            except Exception as e:
                ui.notify(f"Lỗi khi xuất Word: {e}", type="negative")

        with ui.row().classes("w-full items-center justify-between gap-2 pt-2 border-t border-slate-100 flex-wrap"):
            ui.button(
                "🔀 Đảo nhiều mã đề (101, 102...)",
                on_click=lambda: (export_word_dialog.close(), open_shuffle_modal()),
            ).props("flat no-caps color=indigo-700 text-xs").tooltip("Chuyển sang công cụ trộn và đảo nhiều mã đề kèm Bảng ma trận đáp án")
            with ui.row().classes("items-center gap-2"):
                ui.button("Hủy", on_click=export_word_dialog.close).props("flat no-caps")
                ui.button(
                    "🚀 Tải file Word về máy (.docx)",
                    on_click=perform_word_export,
                    color="blue-700",
                ).props("unelevated no-caps").classes("font-semibold px-4 rounded-xl")

    def open_word_export_modal(target_file: str = None):
        if target_file:
            state["active_file"] = target_file
        active_p = Path(state["active_file"])
        if active_p.exists():
            idx_d = _read_index_json()
            meta = idx_d.get(active_p.name, {})
            t = meta.get("title") or active_p.stem
            export_word_state["title"] = t
        export_word_dialog.open()

    # -----------------------------------------------------------------
    # HỘP THOẠI CẤU HÌNH TRỘN & ĐẢO NHIỀU MÃ ĐỀ (KÈM BẢNG MA TRẬN ĐÁP ÁN)
    # -----------------------------------------------------------------
    shuffle_dialog = ui.dialog()
    shuffle_state = {
        "preset": "4",
        "custom_codes": "101, 102, 103, 104",
        "shuffle_questions": True,
        "shuffle_mcq_options": True,
        "shuffle_tf_items": False,
        "mode": "exam_only",
        "school": "SỞ GIÁO DỤC VÀ ĐÀO TẠO",
        "title": "ĐỀ KIỂM TRA ĐỊNH KỲ NĂM HỌC 2025 - 2026",
    }

    with shuffle_dialog, ui.card().classes("w-[680px] max-w-[95vw] max-h-[90vh] overflow-y-auto p-6 rounded-3xl gap-4 bg-white shadow-2xl"):
        with ui.row().classes("w-full items-center justify-between"):
            with ui.row().classes("items-center gap-2"):
                ui.icon("shuffle", size="26px").classes("text-indigo-600")
                ui.label("Cấu hình Trộn & Đảo Đề Thi").classes("text-lg font-black text-slate-800")
            ui.button(icon="close", on_click=shuffle_dialog.close).props("flat round dense size=sm").classes("text-slate-400 hover:text-slate-600")

        ui.label(
            "Tự động tạo nhiều mã đề khác nhau, hoán vị câu hỏi theo từng Phần, đảo phương án A-B-C-D (tự cập nhật đáp án đúng), "
            "xuất từng mã đề ra file Word (.docx) và kèm 1 file Word Bảng ma trận soi đáp án tổng hợp các mã đề, đóng gói thành file ZIP."
        ).classes("text-xs text-slate-500 -mt-1 leading-relaxed")

        ui.separator()

        # 1. Chọn số lượng / danh sách mã đề
        ui.label("🎯 1. Danh sách Mã đề cần tạo:").classes("text-xs font-bold text-slate-700 uppercase tracking-wider")

        def update_shuffle_preset(e):
            val = e.value
            presets = {
                "2": "101, 102",
                "4": "101, 102, 103, 104",
                "6": "101, 102, 103, 104, 105, 106",
                "8": "101, 102, 103, 104, 105, 106, 107, 108",
            }
            if val in presets:
                shuffle_state["custom_codes"] = presets[val]
                shuffle_codes_input.value = presets[val]

        ui.radio(
            {
                "2": "2 mã (101, 102)",
                "4": "4 mã (101 - 104)",
                "6": "6 mã (101 - 106)",
                "8": "8 mã (101 - 108)",
                "custom": "Tùy chỉnh...",
            },
            value="4",
            on_change=update_shuffle_preset,
        ).props("dense inline").classes("text-xs text-slate-800 gap-3")

        shuffle_codes_input = ui.input(
            "Danh sách mã đề (ngăn cách bằng dấu phẩy)",
            value=shuffle_state["custom_codes"],
        ).bind_value(shuffle_state, "custom_codes").props("outlined dense").classes("w-full text-xs font-mono")

        # 2. Quy tắc đảo
        ui.label("⚙️ 2. Quy tắc hoán vị & xáo trộn:").classes("text-xs font-bold text-slate-700 uppercase tracking-wider mt-1")
        with ui.column().classes("w-full bg-slate-50 p-3 rounded-xl border border-slate-200 gap-2 text-xs"):
            ui.checkbox(
                "Hoán vị thứ tự câu hỏi trong từng Phần (giữ đúng cấu trúc ma trận Phần I, II, III, đánh số lại từ 1)",
                value=True,
            ).bind_value(shuffle_state, "shuffle_questions").props("dense")
            ui.checkbox(
                "Đảo ngẫu nhiên các phương án A, B, C, D (Phần I - tự động cập nhật đáp án đúng trong lời giải)",
                value=True,
            ).bind_value(shuffle_state, "shuffle_mcq_options").props("dense")
            ui.checkbox(
                "Đảo thứ tự các ý a), b), c), d) trong câu hỏi Đúng/Sai (Phần II - mặc định tắt để giữ thứ tự sư phạm)",
                value=False,
            ).bind_value(shuffle_state, "shuffle_tf_items").props("dense")

        # 3. Hình thức xuất Word
        ui.label("📑 3. Hình thức xuất Word từng mã đề:").classes("text-xs font-bold text-slate-700 uppercase tracking-wider mt-1")
        ui.radio(
            {
                "exam_only": "📄 Chỉ Đề thi từng mã đề (Dành cho học sinh làm bài, có khung Họ tên/SBD)",
                "exam_and_solution": "📑 Đề thi kèm Đáp án & Lời giải chi tiết theo từng mã đề",
            },
            value="exam_only",
        ).bind_value(shuffle_state, "mode").props("dense").classes("gap-2 text-xs text-slate-800")

        # 4. Tiêu đề trường / kỳ thi
        with ui.expansion("🏫 Tùy chỉnh thông tin tiêu đề đề thi", icon="tune").classes("w-full text-xs bg-slate-50 rounded-xl border border-slate-200"):
            with ui.column().classes("w-full gap-2 p-2"):
                ui.input("Đơn vị / Sở / Trường").bind_value(shuffle_state, "school").props("outlined dense").classes("w-full")
                ui.input("Tiêu đề kỳ thi").bind_value(shuffle_state, "title").props("outlined dense").classes("w-full")

        def perform_shuffle_export():
            active_p = Path(state["active_file"])
            if not active_p.exists():
                ui.notify("Không tìm thấy file đề hiện tại!", type="warning")
                return

            raw = active_p.read_text(encoding="utf-8")
            h_md, q_list = parse_exam_markdown(raw)
            if not q_list:
                ui.notify("Đề thi chưa có câu hỏi nào để đảo!", type="warning")
                return

            raw_codes = shuffle_state["custom_codes"]
            codes = [c.strip() for c in raw_codes.replace(";", ",").split(",") if c.strip()]
            if not codes:
                ui.notify("Vui lòng nhập ít nhất 1 mã đề!", type="warning")
                return

            ui.notify(f"⏳ Đang tiến hành tạo {len(codes)} mã đề và bảng ma trận đáp án...", type="info")

            try:
                res = generate_shuffled_package(
                    header_md=h_md,
                    questions=q_list,
                    exam_codes=codes,
                    school_name=shuffle_state["school"],
                    exam_title=shuffle_state["title"],
                    mode=shuffle_state["mode"],
                    shuffle_questions=shuffle_state["shuffle_questions"],
                    shuffle_mcq_options=shuffle_state["shuffle_mcq_options"],
                    shuffle_tf_items=shuffle_state["shuffle_tf_items"],
                    output_dir=OUTPUT_DIR,
                )

                zip_p = res["zip_path"]
                ui.download(zip_p.read_bytes(), filename=res["zip_filename"])
                ui.notify(
                    f"✓ Đã tạo thành công {len(codes)} mã đề ({', '.join(codes)}) và Bảng ma trận đáp án! Đang tải file ZIP...",
                    type="positive",
                    duration=6,
                )
                shuffle_dialog.close()
            except Exception as e:
                ui.notify(f"Lỗi khi đảo đề: {e}", type="negative")

        with ui.row().classes("w-full items-center justify-end gap-2 pt-2 border-t border-slate-100"):
            ui.button("Hủy", on_click=shuffle_dialog.close).props("flat no-caps")
            ui.button(
                "🚀 Bắt đầu Đảo đề & Tải trọn bộ ZIP (.zip)",
                on_click=perform_shuffle_export,
                color="indigo-700",
            ).props("unelevated no-caps").classes("font-semibold px-5 py-2 rounded-xl text-white shadow-md hover:bg-indigo-800")

    def open_shuffle_modal(target_file: str = None):
        if target_file:
            state["active_file"] = target_file
        active_p = Path(state["active_file"])
        if active_p.exists():
            idx_d = _read_index_json()
            meta = idx_d.get(active_p.name, {})
            t = meta.get("title") or active_p.stem
            shuffle_state["title"] = t
        shuffle_dialog.open()

    # -----------------------------------------------------------------
    # HỘP THOẠI ĐỔI TÊN & XÓA BỘ ĐỀ TRONG OUTPUT/
    # -----------------------------------------------------------------
    rename_dialog = ui.dialog()
    rename_state = {"filename": "", "title": ""}
    with rename_dialog, ui.card().classes("w-[440px] max-w-[92vw] p-5 rounded-2xl gap-3"):
        ui.label("✏️ Đổi tên Bộ đề").classes("text-base font-bold text-slate-800")
        ui.input("Tiêu đề bộ đề").bind_value(rename_state, "title").classes("w-full").props("outlined dense autofocus")

        def confirm_rename():
            fn = rename_state["filename"]
            new_t = rename_state["title"].strip()
            if fn and new_t:
                idx = _read_index_json()
                if fn in idx:
                    idx[fn]["title"] = new_t
                    _write_index_json(idx)
                    ui.notify("Đã cập nhật tên bộ đề!", type="positive")
                    render_File_selector()
                    render_questions_workspace()
            rename_dialog.close()

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Hủy", on_click=rename_dialog.close).props("flat no-caps")
            ui.button("Lưu thay đổi", on_click=confirm_rename, color="primary").props("unelevated no-caps")

    delete_dialog = ui.dialog()
    delete_state = {"filename": "", "path": ""}
    with delete_dialog, ui.card().classes("w-[420px] max-w-[92vw] p-5 rounded-2xl gap-3"):
        ui.label("🗑️ Xác nhận xóa Bộ đề").classes("text-base font-bold text-red-600")
        delete_lbl = ui.label("").classes("text-sm text-slate-700")

        def confirm_delete():
            p = Path(delete_state["path"])
            if p.exists():
                p.unlink(missing_ok=True)
            idx = _read_index_json()
            if delete_state["filename"] in idx:
                del idx[delete_state["filename"]]
                _write_index_json(idx)
            exams_remain = sync_and_list_exams()
            if exams_remain:
                state["active_file"] = exams_remain[0]["path"]
            else:
                state["active_file"] = str(OUTPUT_DIR / "de_ma_tran.md")
            state["editing_idx"] = None
            ui.notify("Đã xóa bộ đề!", type="info")
            delete_dialog.close()
            render_File_selector()
            render_questions_workspace()

        with ui.row().classes("w-full justify-end gap-2 mt-2"):
            ui.button("Hủy", on_click=delete_dialog.close).props("flat no-caps")
            ui.button("Xóa hẳn", on_click=confirm_delete, color="red").props("unelevated no-caps")

    def select_exam(path_str: str):
        state["active_file"] = path_str
        state["editing_idx"] = None
        render_File_selector()
        render_questions_workspace()

    def duplicate_exam(item: dict):
        src_p = Path(item["path"])
        if not src_p.exists():
            return
        new_title = (item.get("title") or item["filename"]) + " (Bản sao)"
        new_p, clean_t = create_unique_exam_file(new_title)
        shutil.copy2(src_p, new_p)
        register_exam_metadata(new_p, title=new_title, grade=item.get("grade", ""), topic=item.get("topic", ""))
        state["active_file"] = str(new_p)
        state["editing_idx"] = None
        ui.notify(f"Đã nhân bản bộ đề mới: {new_p.name}!", type="positive")
        render_File_selector()
        render_questions_workspace()

    def create_new_blank_exam():
        new_p, clean_t = create_unique_exam_file("Bộ đề mới THPT 2026")
        blank_content = (
            f"# {clean_t}\n"
            f"**Môn: Toán 12 — Chương trình THPT 2026**  \n"
            f"*Thời gian làm bài: 90 phút | Thang điểm: 10,00*\n\n"
            f"---\n\n"
            f"## PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn (0 câu)\n"
        )
        new_p.write_text(blank_content, encoding="utf-8")
        register_exam_metadata(new_p, title=clean_t)
        state["active_file"] = str(new_p)
        state["editing_idx"] = None
        ui.notify("Đã khởi tạo bộ đề mới! Bạn có thể thêm câu hỏi ngay.", type="positive")
        render_File_selector()
        render_questions_workspace()

    # -----------------------------------------------------------------
    # RENDER DANH SÁCH FILE TRONG OUTPUT/ (EXAM LIBRARY & MANAGER)
    # -----------------------------------------------------------------
    def render_File_selector():
        file_select_container.clear()
        exams = sync_and_list_exams()

        with file_select_container:
            with ui.row().classes("w-full items-center justify-between mb-2"):
                ui.label(f"Tổng cộng: {len(exams)} bộ đề").classes("text-xs font-semibold text-slate-500")
                ui.button("➕ Tạo đề mới", on_click=create_new_blank_exam, color="indigo-50").props(
                    "unelevated no-caps size=xs"
                ).classes("text-indigo-700 font-bold px-2 py-1 rounded-lg border border-indigo-200 hover:bg-indigo-100")

            if not exams:
                ui.label("Chưa có bộ đề nào trong thư mục output/").classes("text-xs text-slate-400 italic py-2")
                return

            with ui.column().classes("w-full gap-2 max-h-[460px] overflow-y-auto pr-1"):
                for ex in exams:
                    is_active = ex["path"] == state["active_file"]
                    card_style = (
                        "border-2 border-blue-600 bg-blue-50/70 shadow-sm"
                        if is_active
                        else "border border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/80"
                    )

                    with ui.card().classes(f"w-full p-2.5 rounded-xl {card_style} gap-1.5 transition-all"):
                        # Hàng tiêu đề & Badge đang mở
                        with ui.row().classes("w-full items-center justify-between no-wrap"):
                            title_row = ui.row().classes("items-center gap-1.5 min-w-0 cursor-pointer flex-1")
                            title_row.on("click", lambda _, p=ex["path"]: select_exam(p))
                            with title_row:
                                ui.icon("description", size="18px").classes(
                                    "text-blue-600 flex-shrink-0" if is_active else "text-slate-400 flex-shrink-0"
                                )
                                title_txt = ex.get("title") or ex["filename"]
                                ui.label(title_txt).classes(
                                    f"text-xs truncate {'font-bold text-blue-900' if is_active else 'font-semibold text-slate-700'}"
                                ).tooltip(title_txt)

                            if is_active:
                                ui.badge("Đang mở", color="blue-600").classes("text-[10px] px-1.5 py-0.5 rounded-md flex-shrink-0")

                        # Dòng metadata: Số câu, thời gian, tên file
                        with ui.row().classes("w-full items-center justify-between text-[11px] text-slate-500 px-0.5"):
                            with ui.row().classes("items-center gap-1"):
                                ui.badge(f"{ex.get('question_count', 0)} câu", color="slate-200").classes(
                                    "text-slate-700 text-[10px] px-1.5 py-0 rounded font-medium"
                                )
                                ui.label(ex.get("updated_at", "")).classes("text-[10px] text-slate-400")
                            ui.label(ex["filename"]).classes("text-[9px] font-mono text-slate-400 truncate max-w-[120px]")

                        # Hàng nút thao tác nhanh
                        with ui.row().classes("w-full items-center justify-end gap-1 pt-1 border-t border-slate-100"):
                            def open_rename(item=ex):
                                rename_state["filename"] = item["filename"]
                                rename_state["title"] = item.get("title") or item["filename"]
                                rename_dialog.open()

                            def open_delete(item=ex):
                                delete_state["filename"] = item["filename"]
                                delete_state["path"] = item["path"]
                                delete_lbl.set_text(
                                    f"Bạn có chắc muốn xóa '{item.get('title') or item['filename']}' ({item['filename']})?"
                                )
                                delete_dialog.open()

                            ui.button(icon="edit", on_click=open_rename).props(
                                "flat round dense size=xs color=slate-600"
                            ).tooltip("Đổi tên bộ đề")
                            ui.button(icon="content_copy", on_click=lambda item=ex: duplicate_exam(item)).props(
                                "flat round dense size=xs color=indigo-600"
                            ).tooltip("Nhân bản bộ đề này")
                            ui.button(
                                icon="download",
                                on_click=lambda item=ex: ui.download(
                                    Path(item["path"]).read_bytes(), filename=item["filename"]
                                ),
                            ).props("flat round dense size=xs color=emerald-600").tooltip("Tải file .md")
                            ui.button(
                                icon="article",
                                on_click=lambda item=ex: open_word_export_modal(item["path"]),
                            ).props("flat round dense size=xs color=blue-700").tooltip("Xuất ra file Word (.docx)")
                            ui.button(
                                icon="shuffle",
                                on_click=lambda item=ex: open_shuffle_modal(item["path"]),
                            ).props("flat round dense size=xs color=indigo-700").tooltip("Trộn & Đảo nhiều mã đề (.zip)")
                            ui.button(icon="delete", on_click=open_delete).props(
                                "flat round dense size=xs color=red-500"
                            ).tooltip("Xóa bộ đề")

    # -----------------------------------------------------------------
    # RENDER DANH SÁCH THẺ CÂU HỎI TƯƠNG TÁC (MAIN WORKSPACE)
    # -----------------------------------------------------------------
    def render_questions_workspace():
        right_column.clear()
        active_path = Path(state["active_file"])

        with right_column:
            if not active_path.exists():
                with ui.card().classes(
                    "w-full p-10 rounded-2xl border border-dashed border-slate-300 bg-white items-center text-center gap-2"
                ):
                    ui.icon("quiz", size="48px").classes("text-slate-300")
                    ui.label("Chưa có đề toán nào trong file đang chọn").classes(
                        "text-lg font-bold text-slate-700"
                    )
                    ui.label(
                        "Hãy chọn thông số ở cột bên trái và bấm '🚀 Tạo Đề Theo Ma Trận Này & Kiểm Định'."
                    ).classes("text-sm text-slate-500")
                return

            raw_md = active_path.read_text(encoding="utf-8")
            header_md, questions = parse_exam_markdown(raw_md)
            backups = list_backups(active_path)
            active_meta = _read_index_json().get(active_path.name, {})
            current_exam_title = active_meta.get("title") or active_path.stem

            # Thanh công cụ tổng của Đề toán
            with ui.card().classes(
                "w-full p-4 rounded-2xl shadow-sm border border-slate-200 bg-white"
            ):
                with ui.row().classes("w-full items-center justify-between flex-wrap gap-2"):
                    with ui.column().classes("gap-0.5"):
                        with ui.row().classes("items-center gap-2"):
                            ui.label(f"📋 {current_exam_title}").classes(
                                "text-lg font-bold text-slate-800"
                            )
                            ui.badge(f"{len(questions)} câu", color="indigo-100").classes(
                                "text-indigo-800 font-bold text-xs px-2 py-0.5 rounded-full"
                            )
                        ui.label(
                            f"File: output/{active_path.name} • Thao tác: Đổi số 1-Click, Bảo AI sửa riêng, Sửa LaTeX, Xem lời giải"
                        ).classes("text-xs text-slate-500")

                    with ui.row().classes("items-center gap-2"):
                        ui.button(
                            "➕ Thêm câu mới",
                            on_click=add_q_dialog.open,
                            color="primary",
                        ).props("unelevated no-caps size=sm").classes("px-3 rounded-lg font-semibold")

                        def toggle_all_solutions():
                            if len(state["open_solutions"]) == len(questions):
                                state["open_solutions"].clear()
                            else:
                                state["open_solutions"] = set(range(len(questions)))
                            render_questions_workspace()

                        ui.button(
                            "👁️ Ẩn/Hiện toàn bộ lời giải",
                            on_click=toggle_all_solutions,
                            color="slate-100",
                        ).props("unelevated no-caps size=sm").classes("text-slate-700 px-3 rounded-lg")

                        def undo_last_change():
                            bks = list_backups(active_path)
                            if not bks:
                                return
                            active_path.write_text(
                                bks[0].read_text(encoding="utf-8"), encoding="utf-8"
                            )
                            bks[0].unlink()
                            ui.notify("↩️ Đã hoàn tác về phiên bản trước đó!", type="info")
                            render_questions_workspace()

                        ui.button(
                            f"↩️ Hoàn tác ({len(backups)})",
                            on_click=undo_last_change,
                        ).props(
                            f"outline no-caps size=sm {'disable' if not backups else ''}"
                        ).classes("px-3 rounded-lg")

                        ui.button(
                            "📥 Tải file Đề (.md)",
                            on_click=lambda: ui.download(
                                active_path.read_bytes(), filename=active_path.name
                            ),
                            color="emerald-600",
                        ).props("unelevated no-caps size=sm").classes(
                            "text-white px-3 rounded-lg font-semibold"
                        )

                        ui.button(
                            "📝 Xuất File Word (.docx)",
                            on_click=lambda: open_word_export_modal(),
                            color="blue-700",
                        ).props("unelevated no-caps size=sm").classes(
                            "text-white px-3.5 rounded-lg font-semibold shadow-xs hover:bg-blue-800"
                        ).tooltip("Xuất đề thi ra Word: Chỉ đề thi, Đề kèm đáp án, hoặc Riêng đáp án")

                        ui.button(
                            "🔀 Cấu hình Đảo đề",
                            on_click=lambda: open_shuffle_modal(),
                            color="indigo-700",
                        ).props("unelevated no-caps size=sm").classes(
                            "text-white px-3.5 rounded-lg font-semibold shadow-xs hover:bg-indigo-800"
                        ).tooltip("Trộn và đảo nhiều mã đề (101, 102...) kèm Bảng ma trận soi đáp án & nén ZIP")

            # Thanh Lọc câu hỏi nhanh (Filter Bar 1-Click)
            with ui.row().classes("w-full items-center justify-between bg-white px-4 py-2 rounded-xl border border-slate-200 mt-2 flex-wrap gap-2"):
                with ui.row().classes("items-center gap-1.5"):
                    ui.icon("filter_list", size="18px").classes("text-slate-500")
                    ui.label("Lọc phần thi:").classes("text-xs font-bold text-slate-600 mr-1")

                    filters = [
                        ("all", f"Tất cả ({len(questions)})"),
                        ("p1", "Phần I: 4 Lựa chọn"),
                        ("p2", "Phần II: Đúng/Sai"),
                        ("p3", "Phần III: Trả lời ngắn"),
                    ]
                    for f_key, f_lbl in filters:
                        is_act = state.get("filter_part", "all") == f_key
                        def set_f(k=f_key):
                            state["filter_part"] = k
                            render_questions_workspace()
                        btn_cls = "bg-blue-700 text-white font-bold shadow-xs" if is_act else "bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium"
                        ui.button(f_lbl, on_click=set_f).props("unelevated size=xs no-caps").classes(f"{btn_cls} px-2.5 py-1 rounded-lg text-xs")

            # Tiêu đề Đề thi (nếu có)
            if header_md:
                with ui.card().classes(
                    "w-full px-5 py-3.5 rounded-2xl border border-slate-200 bg-white shadow-xs"
                ):
                    ui.html(md_to_math_html(header_md), sanitize=False)

            # Hiển thị từng Câu hỏi dưới dạng Card tương tác độc lập
            current_sec_banner = None
            curr_filter = state.get("filter_part", "all")
            for idx, q in enumerate(questions):
                sec_name = q.get("section", "")
                
                # Áp dụng bộ lọc Phần I, II, III
                if curr_filter == "p1" and "PHẦN I" not in sec_name.upper():
                    continue
                if curr_filter == "p2" and "PHẦN II" not in sec_name.upper():
                    continue
                if curr_filter == "p3" and "PHẦN III" not in sec_name.upper():
                    continue

                if sec_name and sec_name != current_sec_banner:
                    current_sec_banner = sec_name
                    with ui.row().classes(
                        "w-full items-center gap-2 mt-2 px-3 py-1.5 bg-indigo-50 border-l-4 border-indigo-600 rounded-r-lg"
                    ):
                        ui.icon("folder_open", size="18px").classes("text-indigo-700")
                        ui.label(sec_name).classes("text-sm font-bold text-indigo-900")

                is_editing = state["editing_idx"] == idx
                is_sol_open = idx in state["open_solutions"]

                card_accent = (
                    "border-l-4 border-l-blue-600"
                    if "PHẦN I" in sec_name.upper()
                    else ("border-l-4 border-l-emerald-600" if "PHẦN II" in sec_name.upper() else "border-l-4 border-l-amber-500")
                )

                with ui.card().classes(
                    f"w-full p-5 rounded-2xl shadow-xs hover:shadow-md transition-shadow border border-slate-200 {card_accent} bg-white gap-3"
                ):
                    # Hàng tiêu đề của Thẻ câu hỏi + Các nút chức năng trực tiếp
                    with ui.row().classes(
                        "w-full items-center justify-between pb-2 border-b border-slate-100 flex-wrap gap-2"
                    ):
                        with ui.row().classes("items-center gap-2"):
                            ui.badge(f"{q['title']}", color="blue-700").classes(
                                "text-xs font-bold px-3 py-1 rounded-full"
                            )
                            ui.badge("✓ Đã kiểm định", color="emerald-100").classes(
                                "text-emerald-800 text-[11px] font-semibold px-2.5 py-0.5 rounded-full"
                            )

                        # Cụm nút hành động gắn liền trên từng câu hỏi
                        with ui.row().classes("items-center gap-1.5"):
                            # 1. Nút 1-Click Đổi số mới
                            async def quick_regen(i=idx):
                                ai_fix_state["q_idx"] = i
                                await trigger_ai_single_question(
                                    "Đổi bộ số liệu/hàm số khác sao cho nghiệm đẹp, giữ nguyên dạng toán, tính lại đáp án mới chính xác và viết lại lời giải chi tiết mới"
                                )

                            ui.button(
                                "🎲 Đổi số mới",
                                on_click=quick_regen,
                                color="indigo-50",
                            ).props("unelevated no-caps size=sm").classes(
                                "text-indigo-800 hover:bg-indigo-100 font-semibold px-2.5 rounded-lg"
                            ).tooltip("Bảo AI tự động thay bộ số liệu khác có nghiệm đẹp cho riêng câu này")

                            # 2. Nút Mở bảng AI Sửa riêng câu này
                            ui.button(
                                "🤖 AI Sửa câu này",
                                on_click=lambda i=idx, qo=q: open_ai_fix_modal(i, qo),
                                color="blue-600",
                            ).props("unelevated no-caps size=sm").classes(
                                "text-white font-semibold px-3 rounded-lg"
                            ).tooltip("Chọn mức độ khó hoặc nhập yêu cầu để AI sửa riêng câu này")

                            # 3. Nút Sửa tay LaTeX trực tiếp ngay trên thẻ
                            def toggle_edit(i=idx):
                                state["editing_idx"] = None if state["editing_idx"] == i else i
                                render_questions_workspace()

                            ui.button(
                                "✖️ Đóng sửa" if is_editing else "✏️ Sửa tay",
                                on_click=toggle_edit,
                                color="amber-100" if is_editing else "slate-100",
                            ).props("unelevated no-caps size=sm").classes(
                                "text-slate-700 font-medium px-2.5 rounded-lg"
                            )

                            # 4. Nút Xem/Ẩn Đáp án & Lời giải ngay trên thẻ
                            if q["solution"]:
                                def toggle_sol(i=idx):
                                    if i in state["open_solutions"]:
                                        state["open_solutions"].remove(i)
                                    else:
                                        state["open_solutions"].add(i)
                                    render_questions_workspace()

                                ui.button(
                                    "📘 Ẩn lời giải" if is_sol_open else "📘 Xem lời giải",
                                    on_click=toggle_sol,
                                    color="emerald-50" if is_sol_open else "slate-100",
                                ).props("unelevated no-caps size=sm").classes(
                                    f"{'text-emerald-800 font-semibold' if is_sol_open else 'text-slate-700'} px-2.5 rounded-lg"
                                )

                            # 5. Di chuyển lên / xuống & Xóa câu
                            def move_q(i=idx, delta=-1):
                                j = i + delta
                                if 0 <= j < len(questions):
                                    save_version_backup(active_path, "doi_vi_tri")
                                    questions[i], questions[j] = questions[j], questions[i]
                                    active_path.write_text(
                                        rebuild_exam_markdown(header_md, questions),
                                        encoding="utf-8",
                                    )
                                    render_questions_workspace()

                            if idx > 0:
                                ui.button(icon="arrow_upward", on_click=lambda i=idx: move_q(i, -1)).props(
                                    "flat round dense size=sm"
                                ).tooltip("Đẩy câu này lên trên")
                            if idx < len(questions) - 1:
                                ui.button(icon="arrow_downward", on_click=lambda i=idx: move_q(i, 1)).props(
                                    "flat round dense size=sm"
                                ).tooltip("Đẩy câu này xuống dưới")

                            def delete_q(i=idx):
                                save_version_backup(active_path, f"xoa_cau_{i+1}")
                                new_qs = [ item for k, item in enumerate(questions) if k != i ]
                                active_path.write_text(
                                    rebuild_exam_markdown(header_md, new_qs),
                                    encoding="utf-8",
                                )
                                ui.notify(f"🗑️ Đã xóa Câu {i + 1} (Có thể bấm Hoàn tác)", type="warning")
                                render_questions_workspace()

                            ui.button(icon="delete_outline", on_click=delete_q, color="red-400").props(
                                "flat round dense size=sm"
                            ).tooltip("Xóa câu hỏi này")

                    # Thanh nhập Ý tưởng riêng gắn trực tiếp trên từng thẻ câu hỏi (Inline Idea Bar)
                    if idx not in state["card_ideas"]:
                        state["card_ideas"][idx] = {"level": "Giữ nguyên", "idea": ""}
                    card_idea_ref = state["card_ideas"][idx]

                    with ui.row().classes(
                        "w-full items-center gap-2 bg-indigo-50/60 px-3 py-1.5 rounded-xl border border-indigo-100 no-wrap"
                    ):
                        ui.icon("lightbulb", size="18px").classes("text-amber-500 shrink-0")
                        ui.select(
                            ["Giữ nguyên", "Nhận biết", "Thông hiểu", "Vận dụng", "Vận dụng cao"],
                            value=card_idea_ref["level"],
                            label="Mức độ",
                        ).bind_value(card_idea_ref, "level").props("dense borderless").classes(
                            "w-28 text-xs shrink-0"
                        )

                        async def run_inline_idea(i=idx):
                            ref = state["card_ideas"].get(i, {})
                            idea_str = ref.get("idea", "").strip()
                            lvl_str = ref.get("level", "Giữ nguyên")
                            if not idea_str and lvl_str == "Giữ nguyên":
                                with right_column:
                                    ui.notify(
                                        "Hãy nhập ý tưởng hoặc chọn mức độ mới cho câu này!",
                                        type="warning",
                                    )
                                return
                            full_req = (
                                f"[Mức độ: {lvl_str}] {idea_str}"
                                if lvl_str != "Giữ nguyên"
                                else idea_str
                            )
                            ai_fix_state["q_idx"] = i
                            await trigger_ai_single_question(full_req)

                        idea_inp = (
                            ui.input(
                                placeholder=f"💡 Nhập ý tưởng riêng cho {q['title']} (VD: Đổi sang hàm phân thức tìm GTLN trên [1; 3], nghiệm nguyên)...",
                                value=card_idea_ref["idea"],
                            )
                            .bind_value(card_idea_ref, "idea")
                            .props("dense borderless clearable")
                            .classes("flex-1 text-xs")
                        )
                        idea_inp.on("keydown.enter", run_inline_idea)

                        ui.button(
                            "⚡ AI Làm câu này",
                            on_click=run_inline_idea,
                            color="indigo-600",
                        ).props("unelevated no-caps size=sm").classes(
                            "text-white font-semibold px-3 rounded-lg shrink-0"
                        ).tooltip("Yêu cầu hệ thống làm lại riêng câu này theo đúng ý tưởng vừa nhập và kiểm định lại")

                    # Nội dung Đề bài hoặc Khung sửa tay Live LaTeX
                    if is_editing:
                        with ui.row().classes("w-full gap-4 items-start no-wrap mt-1"):
                            ed_state = {"text": q["full_block"]}
                            with ui.column().classes("w-1/2 gap-2"):
                                ui.label("Mã nguồn Markdown / LaTeX của câu này:").classes(
                                    "text-xs font-bold text-slate-500"
                                )
                                live_preview_html = ui.html(md_to_math_html(q["full_block"]), sanitize=False)

                                def on_text_change(e):
                                    ed_state["text"] = e.value
                                    live_preview_html.set_content(md_to_math_html(e.value))
                                    trigger_mathjax()

                                ui.textarea(
                                    value=q["full_block"],
                                    on_change=on_text_change,
                                    pad_x=0,
                                    pad_y=0,
                                ).props("outlined autogrow").classes("w-full font-mono text-sm")

                                def save_manual_edit(i=idx, st_ref=ed_state):
                                    save_version_backup(active_path, f"sua_tay_cau_{i+1}")
                                    questions[i]["full_block"] = st_ref["text"].strip()
                                    active_path.write_text(
                                        rebuild_exam_markdown(header_md, questions),
                                        encoding="utf-8",
                                    )
                                    state["editing_idx"] = None
                                    ui.notify(f"✅ Đã lưu thay đổi cho Câu {i + 1}!", type="positive")
                                    render_questions_workspace()

                                with ui.row().classes(" gap-2"):
                                    ui.button(
                                        "💾 Lưu thay đổi câu này",
                                        on_click=save_manual_edit,
                                        color="primary",
                                    ).props("unelevated no-caps size=sm").classes("px-4")
                                    ui.button(
                                        "Hủy",
                                        on_click=lambda: (
                                            state.update({"editing_idx": None}),
                                            render_questions_workspace(),
                                        ),
                                    ).props("flat no-caps size=sm")

                            with ui.column().classes(
                                "w-1/2 p-4 rounded-xl bg-slate-50 border border-slate-200"
                            ):
                                ui.label("👁️ Xem trước công thức Toán (Live Preview):").classes(
                                    "text-xs font-bold text-slate-500 mb-1"
                                )
                                # Đặt live_preview_html vào cột phải
                                live_preview_html.move(target_container=ui.context.slot.parent)
                    else:
                        # Hiển thị Đề bài + Các phương án lựa chọn
                        ui.html(md_to_math_html(q["stem"]), sanitize=False).classes("w-full px-1")

                        # Hiển thị Lời giải chi tiết khi bật
                        if q["solution"] and is_sol_open:
                            with ui.column().classes(
                                "w-full mt-2 p-4 rounded-xl bg-emerald-50/70 border border-emerald-200 gap-1"
                            ):
                                with ui.row().classes("items-center gap-1.5 mb-1"):
                                    ui.icon("verified", size="18px").classes("text-emerald-700")
                                    ui.label("Đáp án & Lời giải chi tiết (Đã kiểm định)").classes(
                                        "text-xs font-bold text-emerald-900 uppercase tracking-wider"
                                    )
                                ui.html(md_to_math_html(q["solution"], is_solution=True), sanitize=False).classes("w-full")

            trigger_mathjax()

    render_File_selector()
    render_questions_workspace()


if __name__ in {"__main__", "__mp_main__"}:
    import socket

    def is_port_in_use(host: str, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return False
            except OSError:
                return True

    server_host = os.environ.get("HOST", "0.0.0.0")
    default_port = int(os.environ.get("PORT", "8080"))
    server_port = default_port

    # Tự động tìm port khả dụng nếu port mặc định đang bị chiếm dụng
    while is_port_in_use(server_host, server_port) and server_port < default_port + 20:
        print(f"[THONG BAO] Port {server_port} dang ban, tu dong chuyen sang port {server_port + 1}...")
        server_port += 1

    show_browser = os.environ.get("SHOW_BROWSER", "true").lower() in ("true", "1", "yes")

    ui.run(
        title="Math Studio - Hệ Thống Biên Soạn & Thẩm Định Đề Toán",
        host=server_host,
        port=server_port,
        reload=False,
        show=show_browser,
    )
