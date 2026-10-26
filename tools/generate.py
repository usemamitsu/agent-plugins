#!/usr/bin/env python3
"""Generate ready-to-install client packages from skills/ and src/shared/."""
from pathlib import Path
import json
import shutil
import argparse
import re
import zipfile
import hashlib

ROOT = Path(__file__).resolve().parents[1]
VERSION = json.loads((ROOT / "package.json").read_text())["version"]
SKILLS = ROOT / "skills"
REFS = ROOT / "src/shared/references"
AP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/"


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def skills_into(destination, grok=False):
    for source in sorted(SKILLS.iterdir()):
        if grok and source.name == "x-post-extraction":
            continue
        target = destination / source.name
        shutil.copytree(source, target)
        shutil.rmtree(target / "references", ignore_errors=True)
        shutil.copytree(REFS, target / "references")
        if grok and source.name == "mamitsu":
            path = target / "SKILL.md"
            text = path.read_text()
            text = text.replace("YouTube, Instagram, TikTok, and X posts",
                                "YouTube, Instagram, and TikTok posts")
            text = text.replace(
                "; `x-post-extraction` for post text and attachments", "")
            # Put the routing boundary before the call workflow, not after it.
            text = text.replace("# Turn a post into useful information\n",
                "# Turn a post into useful information\n\n"
                "For ordinary X/Twitter requests, use Grok Bot's native X access; "
                "do not route them to mamitsu by default. Use mamitsu for X when "
                "the user explicitly requests it. This boundary applies only to "
                "Grok Bot, not other clients running a Grok model. The mamitsu "
                "API and its application-integration skill still support X.\n"
            )
            path.write_text(text)


def downloads_into(out, grok):
    """Stable ZIP metadata makes byte-for-byte drift checks meaningful."""
    for skill in sorted(SKILLS.iterdir()):
        target = out / "downloads/chatgpt" / f"{skill.name}.zip"
        target.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_STORED) as archive:
            entries = {"SKILL.md": (skill / "SKILL.md").read_bytes()}
            entries.update({
                f"references/{ref.name}": ref.read_bytes()
                for ref in sorted(REFS.iterdir())
            })
            for relative, data in sorted(entries.items()):
                info = zipfile.ZipInfo(f"{skill.name}/{relative}", (2026, 1, 1, 0, 0, 0))
                # Stored entries avoid compression-library version drift in CI.
                info.compress_type = zipfile.ZIP_STORED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
    for skill in sorted((grok / "skills").iterdir()):
        text = (skill / "SKILL.md").read_text()
        # Grok's documented written-instruction route is not a ZIP importer.
        # Inline references so a saved skill needs no local filesystem.
        for ref in sorted(REFS.iterdir()):
            anchor = ref.stem
            text = re.sub(r"\]\(references/" + re.escape(ref.name) + r"\)",
                          f"](#{anchor})", text)
            text += f'\n\n<a id="{anchor}"></a>\n\n' + ref.read_text()
        path = out / "downloads/grok-bot" / f"{skill.name}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    files = []
    for path in sorted((out / "downloads").rglob("*")):
        if path.is_file():
            relative = path.relative_to(out.parent).as_posix()
            files.append({
                "skill": path.stem,
                "client": path.parent.name,
                "path": relative,
                "url": "https://raw.githubusercontent.com/usemamitsu/agent-plugins/main/" + relative,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            })
    write_json(out / "downloads/index.json", {"version": VERSION, "files": files})


def portable(name, dest, grok=False):
    dest.mkdir(parents=True)
    write_json(dest / "plugin.json", {
        "$schema": AP_SCHEMA + "plugin.schema.json",
        "name": name,
        "version": VERSION,
        "description": "Extract structured data from public social posts with mamitsu.",
        "author": {"name": "mamitsu", "url": "https://usemamitsu.com"},
        "homepage": "https://usemamitsu.com",
        "repository": "https://github.com/usemamitsu/agent-plugins",
    })
    write_json(dest / "mcp.json", {
        "$schema": AP_SCHEMA + "mcp.schema.json",
        "mcpServers": {"mamitsu": {"type": "streamable-http", "url": "https://usemamitsu.com/mcp"}}
    })
    skills_into(dest / "skills", grok)


def generate(output_root=ROOT):
    output_root = Path(output_root).resolve()
    out = output_root / "dist"
    if out.exists():
        shutil.rmtree(out)
    write_json(output_root / "plugin.json", {
        "$schema": AP_SCHEMA + "plugin.schema.json",
        "name": "mamitsu",
        "version": VERSION,
        "description": "Extract structured data from public social posts with mamitsu.",
        "author": {"name": "mamitsu", "url": "https://usemamitsu.com"},
        "homepage": "https://usemamitsu.com",
        "repository": "https://github.com/usemamitsu/agent-plugins",
    })
    write_json(output_root / "mcp.json", {
        "$schema": AP_SCHEMA + "mcp.schema.json",
        "mcpServers": {"mamitsu": {"type": "streamable-http", "url": "https://usemamitsu.com/mcp"}}
    })
    portable("mamitsu", out / "portable/mamitsu")
    portable("mamitsu", out / "grok-bot/mamitsu", grok=True)

    claude = out / "claude/mamitsu"
    (claude / ".claude-plugin").mkdir(parents=True)
    write_json(claude / ".claude-plugin/plugin.json", {
        "name": "mamitsu", "version": VERSION,
        "description": "Extract structured data from public social posts with mamitsu.",
        "author": {"name": "mamitsu", "url": "https://usemamitsu.com"},
        "homepage": "https://usemamitsu.com",
        "repository": "https://github.com/usemamitsu/agent-plugins",
        "skills": "./skills"
    })
    write_json(claude / ".mcp.json", {
        "mcpServers": {"mamitsu": {"type": "http", "url": "https://usemamitsu.com/mcp"}}
    })
    skills_into(claude / "skills")
    write_json(output_root / ".claude-plugin/marketplace.json", {
        "name": "mamitsu", "description": "Skills and OAuth MCP for extracting public social posts.", "owner": {"name": "mamitsu"},
        "plugins": [{"name": "mamitsu", "source": "./dist/claude/mamitsu",
                     "description": "Extract structured data from public social posts."}]
    })

    write_json(output_root / ".agents/plugins/marketplace.json", {
        "name": "mamitsu",
        "interface": {"displayName": "mamitsu"},
        "plugins": [{"name": "mamitsu", "source": {"source": "local", "path": "./"},
                     "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                     "category": "Productivity"}]
    })
    write_json(output_root / ".cursor-plugin/marketplace.json", {
        "name": "mamitsu", "owner": {"name": "mamitsu"},
        "plugins": [{"name": "mamitsu", "source": ".",
                     "description": "Extract structured data from public social posts.",
                     "version": VERSION}]
    })

    pi = out / "pi/mamitsu"
    (pi / "extensions").mkdir(parents=True)
    (pi / "package.json").write_text(json.dumps({
        "name": "@usemamitsu/pi-mamitsu",
        "version": VERSION,
        "private": True,
        "description": "mamitsu MCP and skills for Pi",
        "peerDependencies": {"@earendil-works/pi-coding-agent": "*"},
        "peerDependenciesMeta": {"@earendil-works/pi-coding-agent": {"optional": True}},
        "pi": {"extensions": ["./extensions/mamitsu.ts"], "skills": ["./skills"]}
    }, indent=2) + "\n")
    (pi / "extensions/mamitsu.ts").write_text(
        'import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";\n\n'
        'export default function (pi: ExtensionAPI) {\n'
        '  pi.registerMcpServer("mamitsu", {\n'
        '    url: "https://usemamitsu.com/mcp",\n'
        '    description: "Extract structured data from public social posts.",\n'
        '  });\n'
        '}\n'
    )
    skills_into(pi / "skills")
    downloads_into(out, out / "grok-bot/mamitsu")

    # Canonical, independently installable skills carry generated references too.
    # Never mutate canonical source while rendering a temporary drift-check tree.
    if output_root == ROOT:
        for skill in SKILLS.iterdir():
            shutil.copytree(REFS, skill / "references", dirs_exist_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT,
        help="write generated artifacts under this root (source remains the repository)",
    )
    generate(parser.parse_args().output_root)
