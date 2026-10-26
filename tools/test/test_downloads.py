"""Release artifacts are deterministic and preserve standalone/Grok boundaries."""
import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("generate", ROOT / "tools/generate.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
NAMES = {path.name for path in (ROOT / "skills").iterdir()}


class DownloadTests(unittest.TestCase):
    def test_upload_archives_are_complete_and_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            generator.generate(out)
            downloads = out / "dist/downloads"
            self.assertEqual(
                {path.stem for path in (downloads / "chatgpt").glob("*.zip")},
                NAMES,
            )
            before = {}
            for name in NAMES:
                path = downloads / "chatgpt" / f"{name}.zip"
                before[name] = path.read_bytes()
                with zipfile.ZipFile(path) as archive:
                    self.assertIn(f"{name}/SKILL.md", archive.namelist())
                    for ref in ("extraction-contract.md", "source-evidence.md"):
                        self.assertIn(f"{name}/references/{ref}", archive.namelist())
                    self.assertFalse(any(".." in item for item in archive.namelist()))
            generator.generate(out)
            self.assertEqual(before, {
                name: (downloads / "chatgpt" / f"{name}.zip").read_bytes()
                for name in NAMES
            })

    def test_grok_written_skill_downloads_omit_x_and_inline_references(self):
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            generator.generate(out)
            downloads = out / "dist/downloads/grok-bot"
            self.assertEqual({p.stem for p in downloads.glob("*.md")},
                             NAMES - {"x-post-extraction"})
            for path in downloads.glob("*.md"):
                text = path.read_text()
                self.assertNotIn("](references/", text)
                self.assertIn("# mamitsu extraction contract", text)
                self.assertIn("# Working from social-post evidence", text)
            general = (downloads / "mamitsu.md").read_text()
            self.assertNotIn("`x-post-extraction`", general)
            self.assertNotIn("https://x.com/", general)
            self.assertIn("Grok Bot's native X access", general)
            integration = (downloads / "mamitsu-app-integration.md").read_text()
            self.assertIn("X/Twitter", integration)


if __name__ == "__main__":
    unittest.main()
