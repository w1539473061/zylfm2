"""生成文件守卫的回归测试。

守卫本身是防止「贡献者把自己的私有服务端路径写进被追踪文件」的唯一防线，
所以它自己的行为也要有测试兜住：既要能放行干净状态，也要能拦住污染。

这里用一个最小假技能树（带 stub 版 lf_kb.py）来测守卫的判定逻辑，
不依赖真实的 849 章说明书，所以跑得很快。
"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
GUARD = REPO_ROOT / "scripts" / "check_generated.py"

THINKING_BODY = "# Mir200 Script Thinking\n\n## Principles\n\n- 先找入口。\n"
TRAINING_BODY = "# Mir200 Training Course\n\n## Lessons\n\n- lesson-01\n"

# 假 lf_kb.py：只做「生成两个文件」这一件事，行为确定，方便断言。
STUB_LF_KB = '''\
import sys
from pathlib import Path

args = sys.argv[1:]
root = Path(args[args.index("--root") + 1])
refs = root / "references"
refs.mkdir(parents=True, exist_ok=True)
(refs / "mir200-thinking.md").write_text({thinking!r}, encoding="utf-8")
(refs / "mir200-training.md").write_text({training!r}, encoding="utf-8")
print("{{}}")
'''.format(thinking=THINKING_BODY, training=TRAINING_BODY)


def build_fake_skill(root: Path) -> Path:
    """造一棵最小技能树，已处于「干净」状态（生成物与 stub 产物一致）。"""
    skill = root / "lf-mir200-knowledge"
    (skill / "scripts").mkdir(parents=True)
    (skill / "scripts" / "lf_kb.py").write_text(STUB_LF_KB, encoding="utf-8")
    refs = skill / "references"
    refs.mkdir(parents=True)
    (refs / "mir200-thinking.md").write_text(THINKING_BODY, encoding="utf-8")
    (refs / "mir200-training.md").write_text(TRAINING_BODY, encoding="utf-8")
    return skill


def run_guard(root: Path) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(GUARD), "--root", str(root)],
        capture_output=True,
    )
    return result.returncode, result.stdout.decode("utf-8", errors="replace")


class CheckGeneratedTests(unittest.TestCase):
    def test_passes_when_generated_files_match_clean_regeneration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_fake_skill(root)

            code, output = run_guard(root)

        self.assertEqual(code, 0, output)
        self.assertIn("守卫通过", output)

    def test_blocks_private_sample_paths(self):
        """贡献者接入自己的服务端后跑 update，路径会被写进生成物——必须拦住。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = build_fake_skill(root)
            thinking = skill / "references" / "mir200-thinking.md"
            thinking.write_text(
                THINKING_BODY
                + "- Example: `样本Mir200/Envir/QuestDiary/某人的私服/绝密脚本.txt`\n",
                encoding="utf-8",
            )

            code, output = run_guard(root)

        self.assertEqual(code, 1)
        self.assertIn("含私有样本路径", output)
        self.assertIn("绝密脚本.txt", output)

    def test_blocks_manual_edits_even_without_sample_paths(self):
        """手工改生成物也要拦——否则下次 update 会把改动冲掉，白费功夫。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = build_fake_skill(root)
            thinking = skill / "references" / "mir200-thinking.md"
            thinking.write_text(
                THINKING_BODY.replace("先找入口。", "我手改的规则。"), encoding="utf-8"
            )

            code, output = run_guard(root)

        self.assertEqual(code, 1)
        self.assertIn("不一致", output)
        self.assertIn("我手改的规则", output)

    def test_blocks_missing_generated_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = build_fake_skill(root)
            (skill / "references" / "mir200-training.md").unlink()

            code, output = run_guard(root)

        self.assertEqual(code, 1)
        self.assertIn("不存在", output)

    def test_reports_error_when_skill_script_is_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            code, output = run_guard(root)

        self.assertEqual(code, 2)
        self.assertIn("找不到技能脚本", output)

    def test_tolerates_crlf_difference(self):
        """Windows 检出可能带来 CRLF；行尾差异不该被当成污染。"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = build_fake_skill(root)
            thinking = skill / "references" / "mir200-thinking.md"
            thinking.write_bytes(THINKING_BODY.replace("\n", "\r\n").encode("utf-8"))

            code, output = run_guard(root)

        self.assertEqual(code, 0, output)


if __name__ == "__main__":
    unittest.main()
