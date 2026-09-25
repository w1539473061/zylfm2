#!/usr/bin/env python3
"""守卫：references 下两个生成文件必须等于「无样本」状态下 update 的产物。

为什么需要这道检查：`mir200-thinking.md` 与 `mir200-training.md` 由 `lf_kb.py`
从 `样本Mir200` 重新生成，而 `样本Mir200` 是使用者本地的私有服务端目录。
使用者只要把自己的服务端接进来跑一次 `update`，自己服务端的脚本路径就会被写进
这两个**被 git 追踪**的文件——样本目录本身有 `.gitignore` 挡着，这两个文件没有。

这道检查在一份干净副本上（强制排除 `样本Mir200`）重新生成，再与仓库里的版本比对，
任何私有服务端痕迹或手工改动都会让它失败。
"""

from __future__ import annotations

import argparse
import difflib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SKILL_NAME = "lf-mir200-knowledge"
GENERATED = (
    Path("references") / "mir200-thinking.md",
    Path("references") / "mir200-training.md",
)
# 干净副本必须排除样本目录与生成索引，否则「重新生成」就不是干净状态。
COPY_IGNORE = shutil.ignore_patterns(    "样本Mir200", "样本2Mir200", ".lfmir-kb", ".codex-kb", "__pycache__", "*.pyc", ".git"
)
# 生成物里出现这些片段，说明它是在接入私有样本的状态下生成的。
SAMPLE_MARKERS = ("样本Mir200/", "样本Mir200\\", "样本2Mir200/", "样本2Mir200\\")


def emit(text: str = "") -> None:
    """按 UTF-8 直接写 stdout。

    CI（英文 locale 的 Windows runner）里 stdout 编码可能不是 UTF-8，
    直接 print 中文会抛 UnicodeEncodeError 并让检查以非零码退出，
    于是「检查通过」被误报成失败。这里绕开文本层编码，固定写 UTF-8 字节。
    """
    data = (text + "\n").encode("utf-8", errors="replace")
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write(data)
        buffer.flush()
    else:
        sys.stdout.write(data.decode("utf-8", errors="replace"))


def normalize(text: str) -> str:
    """统一换行，避免 Windows 的 CRLF 与 Linux 的 LF 造成假失败。"""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="校验生成文件未被私有样本污染。")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="仓库根目录（含 lf-mir200-knowledge/）。",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    skill = root / SKILL_NAME
    if not (skill / "scripts" / "lf_kb.py").is_file():
        emit(f"错误：找不到技能脚本 {skill / 'scripts' / 'lf_kb.py'}")
        return 2

    problems: list[str] = []

    # 先做定向标记扫描，这样报错信息能直接点出「你把私有服务端带进来了」，
    # 而不是让人对着一堆 diff 猜原因。
    for rel in GENERATED:
        committed = skill / rel
        if not committed.is_file():
            problems.append(f"{rel.as_posix()} 不存在")
            continue
        text = committed.read_text(encoding="utf-8", errors="replace")
        for marker in SAMPLE_MARKERS:
            if marker in text:
                for i, line in enumerate(text.splitlines(), 1):
                    if marker in line:
                        problems.append(
                            f"{rel.as_posix()}:{i} 含私有样本路径（{marker}）：{line.strip()[:110]}"
                        )

    # 再在干净副本上重新生成，与仓库版本比对，抓「手工改动」与「其它漂移」。
    with tempfile.TemporaryDirectory(prefix="lf-guard-") as tmp:
        copy = Path(tmp) / SKILL_NAME
        shutil.copytree(skill, copy, ignore=COPY_IGNORE)
        result = subprocess.run(
            [sys.executable, str(copy / "scripts" / "lf_kb.py"),
             "--root", str(copy), "update"],
            cwd=copy, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
        )
        if result.returncode != 0:
            emit("错误：在干净副本上重建索引失败。")
            emit(result.stdout.strip()[-1500:])
            emit(result.stderr.strip()[-1500:])
            return 2

        for rel in GENERATED:
            committed = skill / rel
            regenerated = copy / rel
            if not regenerated.is_file() or not committed.is_file():
                continue
            expected = normalize(regenerated.read_text(encoding="utf-8", errors="replace"))
            actual = normalize(committed.read_text(encoding="utf-8", errors="replace"))
            if expected == actual:
                continue
            problems.append(f"{rel.as_posix()} 与无样本状态下重新生成的结果不一致：")
            diff = difflib.unified_diff(
                actual.splitlines(), expected.splitlines(),
                fromfile="仓库版本", tofile="重新生成（无样本）", lineterm="", n=1,
            )
            for line in list(diff)[:24]:
                problems.append("    " + line)

    if problems:
        emit("生成文件守卫未通过：\n")
        for item in problems:
            emit(item)
        emit(
            "\n这两个文件由 `lf_kb.py update` 生成，不要手工编辑。\n"
            "如果你接入过自己的服务端，请断开 `样本Mir200` 后重跑：\n"
            f"  python {SKILL_NAME}/scripts/lf_kb.py --root {SKILL_NAME} update\n"
            "提交前请确认 `git diff` 里不含自己服务端的任何路径。"
        )
        return 1

    emit(f"生成文件守卫通过：{len(GENERATED)} 个生成文件均为无样本状态下的产物。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
