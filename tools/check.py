#!/usr/bin/env python3
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFS = ROOT / "src/shared/references"
SKILL_NAMES = {
    "mamitsu", "mamitsu-app-integration", "youtube-extraction",
    "instagram-extraction", "tiktok-extraction", "x-post-extraction"
}
ROOT_ARTIFACTS = [
    ".agents/plugins/marketplace.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/marketplace.json",
    "plugin.json",
    "mcp.json",
]


def files_under(directory):
    return {
        path.relative_to(directory): path.read_bytes()
        for path in directory.rglob("*") if path.is_file()
    }


def main():
    with tempfile.TemporaryDirectory() as temporary:
        generated = Path(temporary) / "generated"
        subprocess.run(
            ["python3", "tools/generate.py", "--output-root", str(generated)],
            cwd=ROOT,
            check=True,
        )

        expected_root = set(ROOT_ARTIFACTS)
        actual_root = {name for name in ROOT_ARTIFACTS if (ROOT / name).is_file()}
        assert actual_root == expected_root, f"Missing root generated files: {expected_root - actual_root}"
        for name in ROOT_ARTIFACTS:
            assert (ROOT / name).read_bytes() == (generated / name).read_bytes(), f"Generated drift: {name}"

        expected_dist = files_under(generated / "dist")
        actual_dist = files_under(ROOT / "dist")
        assert actual_dist.keys() == expected_dist.keys(), (
            f"dist file-set drift: missing={expected_dist.keys() - actual_dist.keys()}, "
            f"extra={actual_dist.keys() - expected_dist.keys()}"
        )
        for relative, expected in expected_dist.items():
            assert actual_dist[relative] == expected, f"Generated drift: dist/{relative}"

        for skill in (ROOT / "skills").iterdir():
            assert (skill / "references/extraction-contract.md").read_bytes() == (
                REFS / "extraction-contract.md"
            ).read_bytes(), f"stale canonical reference: {skill.name}/extraction-contract.md"
            assert (skill / "references/source-evidence.md").read_bytes() == (
                REFS / "source-evidence.md"
            ).read_bytes(), f"stale canonical reference: {skill.name}/source-evidence.md"

        for path in list((ROOT / "dist").rglob("*.json")) + [
            ROOT / name for name in ROOT_ARTIFACTS
        ] + [ROOT / "docs/client-installs.json"]:
            json.loads(path.read_text())

        for pkg in [ROOT / "dist/portable/mamitsu", ROOT / "dist/grok-bot/mamitsu"]:
            manifest = json.loads((pkg / "plugin.json").read_text())
            assert manifest["name"] == "mamitsu"
            assert json.loads((pkg / "mcp.json").read_text())["mcpServers"]["mamitsu"]["url"] == "https://usemamitsu.com/mcp"
            found = {path.name for path in (pkg / "skills").iterdir()}
            expected = SKILL_NAMES - ({"x-post-extraction"} if "grok-bot" in str(pkg) else set())
            assert found == expected, (pkg, found)
            for skill in (pkg / "skills").iterdir():
                text = (skill / "SKILL.md").read_text()
                assert (skill / "references/extraction-contract.md").is_file()
                assert (skill / "references/source-evidence.md").is_file()
                assert text.startswith("---\n") and "\nname: " in text and "\ndescription: " in text

        grok = (ROOT / "dist/grok-bot/mamitsu/skills/mamitsu/SKILL.md").read_text().lower()
        assert "grok bot's native x access" in grok and "do not route them to mamitsu by default" in grok
        assert "x.com/" not in grok and "x-post-extraction" not in grok
        assert "x-post-extraction" not in {path.name for path in (ROOT / "dist/grok-bot/mamitsu/skills").iterdir()}
        common_x = (ROOT / "skills/x-post-extraction/SKILL.md").read_text().lower()
        assert "post author's claim" in common_x
        assert "native x access" not in common_x and "grok bot" not in common_x

        for pkg in [ROOT / "dist/claude/mamitsu", ROOT / "dist/portable/mamitsu", ROOT / "dist/pi/mamitsu"]:
            names = {path.name for path in (pkg / "skills").iterdir()}
            assert names == SKILL_NAMES, (pkg, names)
            assert (pkg / "skills/x-post-extraction/SKILL.md").is_file()
        pi = ROOT / "dist/pi/mamitsu"
        assert "registerMcpServer" in (pi / "extensions/mamitsu.ts").read_text()
        assert json.loads((pi / "package.json").read_text())["private"] is True

        claude_source = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())["plugins"][0]["source"]
        assert (ROOT / claude_source).is_dir(), f"Claude marketplace target missing: {claude_source}"
        cursor_source = json.loads((ROOT / ".cursor-plugin/marketplace.json").read_text())["plugins"][0]["source"]
        assert (ROOT / cursor_source).is_dir(), f"Cursor marketplace target missing: {cursor_source}"
        pi_manifest = json.loads((ROOT / "package.json").read_text())["pi"]
        assert all((ROOT / path.removeprefix("./")).exists() for path in pi_manifest["extensions"] + pi_manifest["skills"])
        cases = json.loads((ROOT / "evals/activation-cases.json").read_text())
        assert len(cases) >= 8
        assert all("expected" in case and "excluded" in case for case in cases)

    print("Committed generated file sets/bytes, references, manifests, package boundaries, and activation fixtures passed.")


if __name__ == "__main__":
    main()
