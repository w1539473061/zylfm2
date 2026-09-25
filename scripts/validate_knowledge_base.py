from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*]\(([^)]+)\)|!\[[^\]]*]\(([^)]+)\)")

# 说明书里的 .rar 是随 CHM 分发的脚本附件。本仓库按 .gitignore 有意不收录
# 归档与二进制，所以这类链接指向的文件预期不存在，不算校验失败；
# 把它们单独统计，免得仓库自带的校验工具长期报假错。
ARCHIVE_SUFFIXES = (".rar", ".zip", ".7z")


def iter_markdown_links(path: Path):
    text = path.read_text(encoding="utf-8")
    for match in LINK_PATTERN.finditer(text):
        target = match.group(1) or match.group(2)
        target = target.strip().strip("<>")
        if not target or target.startswith("#"):
            continue
        split = urlsplit(target)
        if split.scheme or split.netloc:
            continue
        yield unquote(split.path)


def validate(root: Path) -> dict[str, object]:
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
    markdown_files = sorted(root.rglob("*.md"))
    chapter_files = sorted((root / "chapters").rglob("*.md")) if (root / "chapters").exists() else []
    asset_files = [p for p in (root / "assets").rglob("*") if p.is_file()] if (root / "assets").exists() else []

    missing_links = []
    missing_archives = []
    for md in markdown_files:
        for link in iter_markdown_links(md):
            target = (md.parent / link).resolve()
            if target.exists():
                continue
            entry = {
                "file": md.relative_to(root).as_posix(),
                "target": link,
            }
            if link.lower().endswith(ARCHIVE_SUFFIXES):
                missing_archives.append(entry)
            else:
                missing_links.append(entry)

    mojibake_markers = ["����", "锟斤拷"]
    mojibake_files = []
    for md in markdown_files:
        text = md.read_text(encoding="utf-8", errors="replace")
        if any(marker in text for marker in mojibake_markers):
            mojibake_files.append(md.relative_to(root).as_posix())

    return {
        "index_exists": (root / "index.md").exists(),
        "manifest_exists": manifest_path.exists(),
        "chapter_files": len(chapter_files),
        "asset_files": len(asset_files),
        "manifest_chapter_count": manifest.get("chapter_count"),
        "manifest_asset_count": manifest.get("asset_count"),
        "missing_link_count": len(missing_links),
        "missing_links_sample": missing_links[:20],
        "missing_archive_link_count": len(missing_archives),
        "missing_archive_links_sample": missing_archives[:20],
        "mojibake_file_count": len(mojibake_files),
        "mojibake_files_sample": mojibake_files[:20],
    }


def emit_json(data: object) -> None:
    """按 UTF-8 直接写 stdout。

    报告里含中文文件名，而 CI（英文 locale 的 Windows runner）的 stdout
    编码可能不是 UTF-8；直接 print 会抛 UnicodeEncodeError 并以非零码退出，
    把「校验通过」误报成失败。这里绕开文本层编码，固定写 UTF-8 字节。
    """
    text = json.dumps(data, ensure_ascii=False, indent=2)
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write((text + "\n").encode("utf-8", errors="replace"))
        buffer.flush()
    else:
        sys.stdout.write(text + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="静态校验转换后的 Markdown 知识库。")
    parser.add_argument("--root", default="lf-mir200-knowledge/knowledge_base")
    args = parser.parse_args()
    report = validate(Path(args.root))
    emit_json(report)
    if report["missing_link_count"] or not report["index_exists"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
