#!/usr/bin/env python3
"""把 lf-mir200-knowledge 连同必需的说明书知识库安装到本机技能目录。

说明书（knowledge_base/）是技能的必要组成，不能只复制 SKILL.md 外壳。
本脚本先校验源目录完整，再整体拷贝到目标位置。
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path


SKILL_NAME = "lf-mir200-knowledge"
REQUIRED_SKILL_FILES = (Path("SKILL.md"),)
REQUIRED_KNOWLEDGE_FILES = (
    Path("index.md"),
    Path("manifest.json"),
)

# 两个客户端的用户级技能目录。ZCode 优先，Codex 兼容。
DEFAULT_DESTS = {
    "zcode": Path.home() / ".zcode" / "skills" / SKILL_NAME,
    "codex": Path.home() / ".codex" / "skills" / SKILL_NAME,
}


class InstallError(RuntimeError):
    """源目录不是完整的可安装包时抛出。"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="安装 lf-mir200-knowledge 及其必需的 knowledge_base。"
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parents[1] / SKILL_NAME,
        help="包含 SKILL.md 与 knowledge_base/ 的技能目录。",
    )
    parser.add_argument(
        "--target",
        choices=sorted(DEFAULT_DESTS),
        default="zcode",
        help="安装到哪个客户端的用户技能目录（默认 zcode）。",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="显式指定目标目录，覆盖 --target。",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="校验通过后替换已存在的目标目录。",
    )
    return parser.parse_args()


def require_directory(path: Path, label: str) -> None:
    if not path.is_dir():
        raise InstallError(f"缺少{label}目录：{path}")


def require_files(root: Path, files: tuple[Path, ...], label: str) -> None:
    missing = [str(path) for path in files if not (root / path).is_file()]
    if missing:
        raise InstallError(f"{label}缺少必需文件：{', '.join(missing)}")


def validate_source(source: Path) -> Path:
    source = source.resolve()
    require_directory(source, "技能")
    require_files(source, REQUIRED_SKILL_FILES, "技能")
    knowledge = source / "knowledge_base"
    require_directory(knowledge, "knowledge_base")
    require_files(knowledge, REQUIRED_KNOWLEDGE_FILES, "knowledge_base")

    manifest = json.loads((knowledge / "manifest.json").read_text(encoding="utf-8"))
    chapter_count = manifest.get("chapter_count")
    if not isinstance(chapter_count, int) or chapter_count <= 0:
        raise InstallError("knowledge_base/manifest.json 没有正的 chapter_count")
    chapters = knowledge / "chapters"
    if not chapters.is_dir() or not any(chapters.rglob("*.md")):
        raise InstallError("knowledge_base/chapters 下没有任何 Markdown 章节")
    return source


def install(source: Path, dest: Path, force: bool = False) -> dict[str, object]:
    source = validate_source(source)
    dest = dest.resolve()
    if dest.exists() and not force:
        raise InstallError(f"目标已存在：{dest}；如需替换请加 --force")

    dest.parent.mkdir(parents=True, exist_ok=True)
    # 先拷到同盘临时目录再原子替换，避免拷到一半失败留下半个技能。
    staging_parent = Path(tempfile.mkdtemp(prefix="lf-mir200-skill-", dir=dest.parent))
    staging = staging_parent / dest.name
    try:
        # 生成的索引与缓存可以重建，不随安装拷贝。
        shutil.copytree(
            source,
            staging,
            ignore=shutil.ignore_patterns(".lfmir-kb", ".codex-kb", "__pycache__", "*.pyc"),
        )
        if dest.exists():
            shutil.rmtree(dest)
        staging.replace(dest)
    finally:
        shutil.rmtree(staging_parent, ignore_errors=True)

    chapter_count = len(list((dest / "knowledge_base" / "chapters").rglob("*.md")))
    asset_count = len([p for p in (dest / "knowledge_base" / "assets").rglob("*") if p.is_file()])
    return {
        "destination": str(dest),
        "skill": True,
        "knowledge_base": True,
        "chapter_files": chapter_count,
        "asset_files": asset_count,
    }


def emit(text: str) -> None:
    """按 UTF-8 直接写 stdout，避免非 UTF-8 locale 下打印中文报编码错。"""
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write((text + "\n").encode("utf-8", errors="replace"))
        buffer.flush()
    else:
        sys.stdout.write(text + "\n")


def main() -> int:
    args = parse_args()
    dest = args.dest if args.dest is not None else DEFAULT_DESTS[args.target]
    try:
        result = install(args.source, dest, args.force)
    except (InstallError, OSError, json.JSONDecodeError) as exc:
        emit(f"错误：{exc}")
        return 1
    emit(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
