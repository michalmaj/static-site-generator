# # src/main.py
# import os
# import shutil
# from pathlib import Path
# from page import generate_pages_recursive  # <-- ważne: rekurencja!

# def _project_root() -> Path:
#     return Path(__file__).resolve().parent.parent

# def _abs(rel: str) -> Path:
#     return _project_root() / rel

# def clean_dir(dst: Path) -> None:
#     if dst.exists():
#         print(f"[clean] removing: {dst}")
#         shutil.rmtree(dst)
#     print(f"[clean] mkdir: {dst}")
#     dst.mkdir(parents=True, exist_ok=True)

# def copy_recursive(src: Path, dst: Path) -> None:
#     if not src.exists():
#         print(f"[warn] static not found: {src}")
#         return
#     for name in os.listdir(src):
#         s = src / name
#         d = dst / name
#         if s.is_dir():
#             print(f"[dir ] {d}")
#             d.mkdir(parents=True, exist_ok=True)
#             copy_recursive(s, d)
#         else:
#             print(f"[copy] {s} -> {d}")
#             shutil.copy(s, d)

# def build():
#     root = _project_root()
#     static_dir = root / "static"
#     public_dir = root / "public"
#     content_dir = root / "content"
#     template_path = root / "template.html"

#     # 1) wyczyść public/
#     clean_dir(public_dir)

#     # 2) skopiuj static/
#     copy_recursive(static_dir, public_dir)

#     # 3) wygeneruj WSZYSTKIE strony z content/ -> public/
#     print(f"[pages] generating from {content_dir} -> {public_dir} using {template_path}")
#     generate_pages_recursive(content_dir, template_path, public_dir)
#     print("[done] site built.")

# def main():
#     build()

# if __name__ == "__main__":
#     main()

# src/main.py
import os
import sys
import shutil
from pathlib import Path
from page import generate_pages_recursive

def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent

def _abs(rel: str) -> Path:
    return _project_root() / rel

def clean_dir(dst: Path) -> None:
    if dst.exists():
        print(f"[clean] removing: {dst}")
        shutil.rmtree(dst)
    print(f"[clean] mkdir: {dst}")
    dst.mkdir(parents=True, exist_ok=True)

def copy_recursive(src: Path, dst: Path) -> None:
    if not src.exists():
        print(f"[warn] static not found: {src}")
        return
    for name in os.listdir(src):
        s = src / name
        d = dst / name
        if s.is_dir():
            print(f"[dir ] {d}")
            d.mkdir(parents=True, exist_ok=True)
            copy_recursive(s, d)
        else:
            print(f"[copy] {s} -> {d}")
            shutil.copy(s, d)

def build(basepath: str = "/"):
    root = _project_root()
    static_dir = root / "static"
    docs_dir   = root / "docs"       # <-- build do docs/
    content_dir = root / "content"
    template_path = root / "template.html"

    # 1) wyczyść docs/
    clean_dir(docs_dir)

    # 2) skopiuj static/ -> docs/
    copy_recursive(static_dir, docs_dir)

    # 3) wygeneruj wszystkie strony z content/ -> docs/
    print(f"[pages] generating from {content_dir} -> {docs_dir} using {template_path} (basepath={basepath})")
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath=basepath)
    print("[done] site built.")

def main():
    # basepath z argv (opcjonalny), domyślnie "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    build(basepath)

if __name__ == "__main__":
    main()