import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class ContractTests(unittest.TestCase):
    def test_release_identity_matches_across_client_outputs(self):
        version = json.loads((ROOT / "package.json").read_text())["version"]
        contract = json.loads((ROOT / "docs/client-installs.json").read_text())
        self.assertEqual(contract["releaseVersion"], version)
        for relative in ("plugin.json", "dist/portable/mamitsu/plugin.json",
                         "dist/grok-bot/mamitsu/plugin.json",
                         "dist/claude/mamitsu/.claude-plugin/plugin.json"):
            manifest = json.loads((ROOT / relative).read_text())
            self.assertEqual(manifest["name"], "mamitsu")
            self.assertEqual(manifest["version"], version)
        self.assertEqual(json.loads((ROOT / "dist/pi/mamitsu/package.json").read_text())["version"],
                         version)

    def test_every_independent_skill_has_both_reference_files(self):
        skills = ROOT / "skills"
        for skill in skills.iterdir():
            with self.subTest(skill=skill.name):
                self.assertTrue((skill / "SKILL.md").is_file())
                text = (skill / "SKILL.md").read_text()
                self.assertIn("references/extraction-contract.md", text)
                self.assertIn("references/source-evidence.md", text)
                self.assertTrue((skill / "references/extraction-contract.md").is_file())
                self.assertTrue((skill / "references/source-evidence.md").is_file())

    def test_grok_variant_is_explicit_and_separate_from_api_skill(self):
        cases = json.loads((ROOT / "evals/activation-cases.json").read_text())
        x_case = next(c for c in cases if c.get("variant") == "grok-bot" and c["expected"] == [])
        self.assertIn("native X", x_case["note"])
        integration = next(c for c in cases if "integrate mamitsu" in c["prompt"].lower())
        self.assertIn("mamitsu-app-integration", integration["expected"])
        self.assertNotIn("mamitsu-app-integration", integration["excluded"])

    def test_machine_contract_has_install_and_independent_modes(self):
        contract = json.loads((ROOT / "docs/client-installs.json").read_text())
        self.assertEqual(contract["mcp"]["endpoint"], "https://usemamitsu.com/mcp")
        self.assertIn("claude-code", contract["clients"])
        self.assertIn("claude-web-desktop", contract["clients"])
        self.assertIn("grok-bot", contract["clients"])
        self.assertEqual(contract["standaloneSkills"]["update"], "npx skills update")
        self.assertIsNone(contract["clients"]["cursor"]["combined"])
        self.assertNotIn("marketplace/publish", contract["clients"]["cursor"]["documentation"])
        self.assertIn("hermes plugins enable", contract["clients"]["hermes"]["combined"])

    def test_current_hosted_entrypoints_keep_customer_steps_actionable(self):
        contract = json.loads((ROOT / "docs/client-installs.json").read_text())
        chatgpt = json.dumps(contract["clients"]["chatgpt"])
        self.assertIn("Plugins > + > Add custom MCP server", chatgpt)
        self.assertIn("Create as a plugin", chatgpt)
        self.assertNotIn("Settings > Apps", chatgpt)
        self.assertNotIn("Developer mode", chatgpt)
        self.assertNotIn("permission to upload", chatgpt)
        cursor = contract["clients"]["cursor"]
        self.assertIsNone(cursor["combined"])
        self.assertTrue(all(step["kind"] == "instruction"
                            for step in cursor["routes"]["combined"]["steps"]))
        self.assertIn("Customize", json.dumps(cursor["routes"]["combined"]))
        self.assertIn("Install", json.dumps(cursor["routes"]["combined"]))
        self.assertNotIn("git clone", json.dumps(cursor))
        self.assertIn("Customize > MCPs", json.dumps(cursor["routes"]["mcp"]))
        instructions = (ROOT / "docs/install.md").read_text().replace("**", "")
        self.assertIn("Plugins > + > Add custom MCP server", instructions)
        self.assertNotIn("Settings > Apps", instructions)
        self.assertNotIn("Developer mode", instructions)
        self.assertNotIn("git clone", instructions)
        self.assertNotIn("permission to upload", instructions)
        self.assertIn("git clone", (ROOT / "docs/advanced-installs.md").read_text())

    def test_pi_package_login_and_hermes_focused_install_routes(self):
        client = json.loads((ROOT / "docs/client-installs.json").read_text())["clients"]["pi"]
        expected = 'pi install git:github.com/usemamitsu/agent-plugins@main && pi "/mcp login mamitsu"'
        self.assertEqual(client["combined"], expected)
        self.assertEqual(client["routes"]["combined"]["steps"][0]["command"], expected)
        hermes = json.loads((ROOT / "docs/client-installs.json").read_text())["clients"]["hermes"]
        self.assertEqual(hermes["package"], "dist/portable/mamitsu")
        self.assertIn("/dist/portable/mamitsu --no-enable", hermes["combined"])

    def test_gui_routes_are_actionable_without_fake_commands(self):
        contract = json.loads((ROOT / "docs/client-installs.json").read_text())
        for name in ("chatgpt", "grok-bot"):
            client = contract["clients"][name]
            self.assertEqual(client["primaryMode"], "separate")
            self.assertIsNone(client["combined"])
            self.assertIsNone(client["skillsOnly"])
            self.assertNotIn("combined", client["routes"])
            for route in ("mcp", "skills"):
                self.assertTrue(client["routes"][route]["steps"])
                self.assertFalse(any(step["kind"] == "command"
                                     for step in client["routes"][route]["steps"]))
        claude = contract["clients"]["claude-web-desktop"]
        self.assertTrue(claude["routes"]["combined"]["steps"])
        self.assertIn("Connectors", json.dumps(claude["routes"]["combined"]))
        self.assertIn("modal=add-custom-connector",
                      claude["routes"]["mcp"]["steps"][0]["url"])
        self.assertIn("other", contract["clients"])

    def test_download_contract_matches_shipped_assets_and_hashes(self):
        import hashlib
        contract = json.loads((ROOT / "docs/client-installs.json").read_text())
        manifest = json.loads((ROOT / contract["downloadsManifest"]).read_text())
        for item in manifest["files"]:
            self.assertEqual(hashlib.sha256((ROOT / item["path"]).read_bytes()).hexdigest(),
                             item["sha256"])
        self.assertEqual(len(manifest["files"]), 11)
        for client in contract["clients"].values():
            for route in client["routes"].values():
                for step in route["steps"]:
                    if step["kind"] == "download":
                        self.assertTrue((ROOT / step["artifact"]).is_file())
                        self.assertTrue(any(item["url"] == step["url"]
                                            for item in manifest["files"]))

    def test_grok_model_in_other_clients_keeps_x(self):
        for package in ("dist/pi/mamitsu", "dist/claude/mamitsu", "dist/portable/mamitsu"):
            self.assertTrue((ROOT / package / "skills/x-post-extraction/SKILL.md").is_file())
            self.assertNotIn("native X access",
                             (ROOT / package / "skills/mamitsu/SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
