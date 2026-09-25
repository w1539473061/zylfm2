import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from install_skill import InstallError, install, validate_source


class InstallSkillTests(unittest.TestCase):
    def make_source(self, root: Path, include_knowledge: bool = True) -> Path:
        skill = root / "lf-mir200-knowledge"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: lf-mir200-knowledge\n---\n", encoding="utf-8")
        if include_knowledge:
            knowledge = skill / "knowledge_base"
            (knowledge / "chapters").mkdir(parents=True)
            (knowledge / "assets").mkdir()
            (knowledge / "index.md").write_text("# index\n", encoding="utf-8")
            (knowledge / "manifest.json").write_text(
                json.dumps({"chapter_count": 1}), encoding="utf-8"
            )
            (knowledge / "chapters" / "001-test.md").write_text("# test\n", encoding="utf-8")
        return skill

    def test_install_copies_skill_and_packaged_knowledge_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_source(root / "source")
            dest = root / "installed"

            result = install(source, dest)

            self.assertTrue(result["skill"])
            self.assertTrue(result["knowledge_base"])
            self.assertTrue((dest / "SKILL.md").is_file())
            self.assertTrue((dest / "knowledge_base" / "index.md").is_file())
            self.assertTrue((dest / "knowledge_base" / "chapters" / "001-test.md").is_file())

    def test_install_skips_generated_indexes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_source(root / "source")
            (source / ".lfmir-kb" / "indexes").mkdir(parents=True)
            (source / ".lfmir-kb" / "indexes" / "docs.json").write_text("[]", encoding="utf-8")
            dest = root / "installed"

            install(source, dest)

            self.assertFalse((dest / ".lfmir-kb").exists())

    def test_install_rejects_skill_without_companion_knowledge_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_source(Path(tmp) / "source", include_knowledge=False)

            with self.assertRaises(InstallError):
                validate_source(source)

    def test_install_rejects_empty_chapter_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_source(root / "source")
            for chapter in (source / "knowledge_base" / "chapters").glob("*.md"):
                chapter.unlink()

            with self.assertRaises(InstallError):
                validate_source(source)

    def test_install_does_not_overwrite_without_force(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_source(root / "source")
            dest = root / "installed"
            dest.mkdir()

            with self.assertRaises(InstallError):
                install(source, dest)

    def test_install_force_replaces_existing_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = self.make_source(root / "source")
            dest = root / "installed"
            dest.mkdir()
            (dest / "stale.txt").write_text("old", encoding="utf-8")

            install(source, dest, force=True)

            self.assertFalse((dest / "stale.txt").exists())
            self.assertTrue((dest / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
