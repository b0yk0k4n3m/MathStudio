# -*- coding: utf-8 -*-
"""
Script tự động tạo biểu tượng (Shortcut) Math Studio ra màn hình Desktop của Windows
Kèm icon toán học chuyên nghiệp và bộ khởi động ẩn cửa sổ dòng lệnh (Silent Launcher)
"""

import os
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def ensure_ico(ico_path: Path):
    if ico_path.exists():
        return
    try:
        from PIL import Image, ImageDraw
        sizes = [16, 32, 48, 64, 128, 256]
        images = []
        for s in sizes:
            img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            r = int(s * 0.22)
            bg_color = (37, 99, 235, 255) # Royal Blue
            draw.rounded_rectangle([0, 0, s - 1, s - 1], radius=r, fill=bg_color)
            border_color = (96, 165, 250, 255)
            draw.rounded_rectangle([1, 1, s - 2, s - 2], radius=r, outline=border_color, width=max(1, s // 40))
            pad = s * 0.22
            w = s - 2 * pad
            x0, y0 = pad, pad
            x1, y1 = s - pad, s - pad
            xm, ym = pad + w * 0.45, s / 2
            lw = max(2, int(s * 0.09))
            draw.line([(x1, y0), (x0, y0), (xm, ym), (x0, y1), (x1, y1)], fill=(255, 255, 255, 255), width=lw, joint="curve")
            accent_r = max(1, int(s * 0.05))
            draw.ellipse([x1 - accent_r * 2, ym - accent_r, x1, ym + accent_r], fill=(250, 204, 21, 255))
            images.append(img)
        images[-1].save(str(ico_path), format="ICO", sizes=[(s, s) for s in sizes])
        print(f"✓ Đã tạo icon {ico_path.name}")
    except Exception as e:
        print(f"Cảnh báo khi tạo icon: {e}")

def create_desktop_shortcut():
    proj_dir = Path(__file__).parent.resolve()
    ico_path = proj_dir / "math_studio.ico"
    ensure_ico(ico_path)

    vbs_path = proj_dir / "run_desktop.vbs"
    # Tạo launcher chạy ẩn cửa sổ CMD để trông như ứng dụng Desktop thật
    vbs_content = (
        'Set WshShell = CreateObject("WScript.Shell")\n'
        'Set fso = CreateObject("Scripting.FileSystemObject")\n'
        'strDir = fso.GetParentFolderName(WScript.ScriptFullName)\n'
        'WshShell.CurrentDirectory = strDir\n'
        'WshShell.Run "cmd /c run_app.bat", 0, False\n'
    )
    vbs_path.write_text(vbs_content, encoding="utf-8")

    desktop_dir = Path(os.environ.get("USERPROFILE", "")) / "Desktop"
    if not desktop_dir.exists():
        # Fallback to OneDrive Desktop if synced
        onedrive_desktop = Path(os.environ.get("USERPROFILE", "")) / "OneDrive" / "Desktop"
        if onedrive_desktop.exists():
            desktop_dir = onedrive_desktop

    if not desktop_dir.exists():
        print("Không tìm thấy thư mục Desktop trên hệ thống!")
        return False

    lnk_path = desktop_dir / "Math Studio.lnk"

    # Thử tạo qua COM win32com nếu có
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(str(lnk_path))
        shortcut.TargetPath = str(vbs_path)
        shortcut.WorkingDirectory = str(proj_dir)
        if ico_path.exists():
            shortcut.IconLocation = f"{str(ico_path)}, 0"
        shortcut.Description = "Math Studio - Hệ Thống Biên Soạn & Thẩm Định Đề Thi Toán THPT"
        shortcut.Save()
        print(f"✓ ĐÃ TẠO ICON THÀNH CÔNG TRÊN DESKTOP: {lnk_path}")
        return True
    except Exception as e:
        pass

    # Fallback: Tạo qua file VBS tạm bằng cscript
    try:
        temp_vbs = proj_dir / "_temp_create_lnk.vbs"
        script_txt = (
            f'Set WshShell = CreateObject("WScript.Shell")\n'
            f'Set oLink = WshShell.CreateShortcut("{str(lnk_path)}")\n'
            f'oLink.TargetPath = "{str(vbs_path)}"\n'
            f'oLink.WorkingDirectory = "{str(proj_dir)}"\n'
            f'oLink.IconLocation = "{str(ico_path)}, 0"\n'
            f'oLink.Description = "Math Studio - He Thong Bien Soan & Tham Dinh De Thi Toan THPT"\n'
            f'oLink.Save\n'
        )
        temp_vbs.write_text(script_txt, encoding="utf-8")
        os.system(f'cscript //nologo "{str(temp_vbs)}"')
        if temp_vbs.exists():
            temp_vbs.unlink()
        print(f"✓ ĐÃ TẠO ICON THÀNH CÔNG TRÊN DESKTOP: {lnk_path}")
        return True
    except Exception as err:
        print(f"Lỗi khi tạo shortcut: {err}")
        return False

if __name__ == "__main__":
    create_desktop_shortcut()
