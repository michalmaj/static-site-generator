# # src/page.py
# from __future__ import annotations
# import os
# import re
# from pathlib import Path
# from markdown_to_html import markdown_to_html_node


# _H1_RE = re.compile(r"^\s*#(?!#)\s*(.+?)\s*$")  # tylko pojedynczy '#', z obustronnym trimem


# def extract_title(markdown: str) -> str:
#     """
#     Zwraca tytuł strony (pierwszy nagłówek H1).
#     Jeśli brak H1, rzuca ValueError.
#     Przykład:
#         "# Hello" -> "Hello"
#     """
#     if markdown is None:
#         raise ValueError("markdown cannot be None")

#     # Normalizacja końców linii
#     text = markdown.replace("\r\n", "\n").replace("\r", "\n")

#     for line in text.split("\n"):
#         m = _H1_RE.match(line)
#         if m:
#             return m.group(1).strip()

#     raise ValueError("No H1 ('# ') header found in markdown")


# def generate_page(from_path: str | os.PathLike,
#                   template_path: str | os.PathLike,
#                   dest_path: str | os.PathLike) -> None:
#     """
#     Generuje pojedynczą stronę HTML na bazie markdownu i szablonu.

#     Kroki:
#       - czyta markdown (from_path)
#       - renderuje do HTML string (markdown_to_html_node(...).to_html())
#       - wyciąga tytuł extract_title(...)
#       - wczytuje template (template_path)
#       - podstawia {{ Title }} oraz {{ Content }}
#       - zapisuje do dest_path, tworząc katalogi
#     """
#     from_path = Path(from_path)
#     template_path = Path(template_path)
#     dest_path = Path(dest_path)

#     print(f"[generate] {from_path} -> {dest_path} (template: {template_path})")

#     md = from_path.read_text(encoding="utf-8")
#     template = template_path.read_text(encoding="utf-8")

#     root_node = markdown_to_html_node(md)
#     html_inner = root_node.to_html()

#     title = extract_title(md)

#     page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_inner)

#     dest_path.parent.mkdir(parents=True, exist_ok=True)
#     dest_path.write_text(page, encoding="utf-8")
#     print(f"[generate] wrote: {dest_path}")

# def generate_pages_recursive(dir_path_content, template_path, dest_dir_path) -> None:
#     """
#     Mapowanie:
#       content/index.md           -> public/index.html
#       content/x.md               -> public/x/index.html
#       content/blog/y.md          -> public/blog/y/index.html
#       content/blog/y/index.md    -> public/blog/y/index.html  (też działa)
#     """
#     content_root = Path(dir_path_content)
#     dest_root = Path(dest_dir_path)
#     template_path = Path(template_path)

#     if not content_root.exists():
#         raise FileNotFoundError(f"Content directory not found: {content_root}")

#     for root, _dirs, files in os.walk(content_root):
#         root_path = Path(root)
#         for fname in files:
#             if not fname.lower().endswith(".md"):
#                 continue

#             src_md = root_path / fname
#             rel = src_md.relative_to(content_root)  # np. blog/glorfindel/index.md

#             # Dwa warianty wejścia:
#             # 1) .../index.md
#             # 2) .../<name>.md
#             if rel.stem == "index":
#                 # .../index.md -> .../index.html (zachowaj drzewo)
#                 dest_html = dest_root / rel.with_suffix(".html")
#             else:
#                 # .../<name>.md -> .../<name>/index.html
#                 dest_html = dest_root / rel.parent / rel.stem / "index.html"

#             print(f"[generate] {src_md} -> {dest_html}")
#             dest_html.parent.mkdir(parents=True, exist_ok=True)
#             generate_page(src_md, template_path, dest_html)

# src/page.py
from __future__ import annotations
import os
import re
from pathlib import Path
from markdown_to_html import markdown_to_html_node

_H1_RE = re.compile(r"^\s*#(?!#)\s*(.+?)\s*$")  # tylko pojedynczy '#'

def extract_title(markdown: str) -> str:
    if markdown is None:
        raise ValueError("markdown cannot be None")
    text = markdown.replace("\r\n", "\n").replace("\r", "\n")
    for line in text.split("\n"):
        m = _H1_RE.match(line)
        if m:
            return m.group(1).strip()
    raise ValueError("No H1 ('# ') header found in markdown")

def _normalize_basepath(bp: str | None) -> str:
    bp = (bp or "/").strip()
    if not bp:
        bp = "/"
    if not bp.startswith("/"):
        bp = "/" + bp
    if not bp.endswith("/"):
        bp = bp + "/"
    return bp

def generate_page(from_path: str | os.PathLike,
                  template_path: str | os.PathLike,
                  dest_path: str | os.PathLike,
                  basepath: str = "/") -> None:
    """
    Generuje stronę HTML i podmienia ścieżki absolutne na z basepath:
      href="/..." -> href="{basepath}..."
      src="/..."  -> src="{basepath}..."
    """
    from_path = Path(from_path)
    template_path = Path(template_path)
    dest_path = Path(dest_path)
    basepath = _normalize_basepath(basepath)

    print(f"[generate] {from_path} -> {dest_path} (template: {template_path}, basepath: {basepath})")

    md = from_path.read_text(encoding="utf-8")
    template = template_path.read_text(encoding="utf-8")

    root_node = markdown_to_html_node(md)
    html_inner = root_node.to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_inner)

    # Podmiana ścieżek absolutnych (tylko gdy zaczynają się od "/")
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/',  f'src="{basepath}')

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(page, encoding="utf-8")
    print(f"[generate] wrote: {dest_path}")

def generate_pages_recursive(dir_path_content: str | os.PathLike,
                             template_path: str | os.PathLike,
                             dest_dir_path: str | os.PathLike,
                             basepath: str = "/") -> None:
    """
    Mapowanie:
      content/index.md        -> docs/index.html
      content/x.md            -> docs/x/index.html
      content/blog/y.md       -> docs/blog/y/index.html
      content/blog/y/index.md -> docs/blog/y/index.html
    """
    content_root = Path(dir_path_content)
    dest_root = Path(dest_dir_path)
    template_path = Path(template_path)
    basepath = _normalize_basepath(basepath)

    if not content_root.exists():
        raise FileNotFoundError(f"Content directory not found: {content_root}")

    for root, _dirs, files in os.walk(content_root):
        root_path = Path(root)
        for fname in files:
            if not fname.lower().endswith(".md"):
                continue
            src_md = root_path / fname
            rel = src_md.relative_to(content_root)

            if rel.stem == "index":
                dest_html = dest_root / rel.with_suffix(".html")
            else:
                dest_html = dest_root / rel.parent / rel.stem / "index.html"

            print(f"[generate] {src_md} -> {dest_html} (basepath: {basepath})")
            dest_html.parent.mkdir(parents=True, exist_ok=True)
            generate_page(src_md, template_path, dest_html, basepath=basepath)