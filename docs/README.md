# Package development

[Install mamitsu](install.md) · [Package checks](verification.md) ·
[Advanced installs](advanced-installs.md)

## Client install contract

[`client-installs.json`](client-installs.json) describes installation,
authorization, and updates for each client. Its format is validated by
[`client-installs.schema.json`](client-installs.schema.json).

- `routes` contains ordered `command`, `link`, `download`, or `instruction`
  steps. GUI routes do not need a shell command.
- `primaryMode` selects a combined plugin or separate MCP and skills routes.
- `authorize` describes account connection separately from installation.
- `combined`, `skillsOnly`, and `update` are convenient text fields; use
  `routes` when rendering complete steps.

The download manifest at `dist/downloads/index.json` lists each artifact's
skill name, client collection, URL, and SHA-256 digest.

## Source and generated packages

Skill bodies live in `skills/*/SKILL.md`; shared references live in
`src/shared/references/`. Each standalone skill includes its own references.

After editing those sources:

```sh
npm ci
npm run generate
npm run check
```

Commit generated outputs with their source changes. Installers use these
ready-to-install packages without a build step:

| Package | Clients |
|---|---|
| Root `plugin.json`, `mcp.json`, `skills/` | Codex and Cursor |
| `dist/portable/mamitsu/` | Hermes |
| `dist/claude/mamitsu/` | Claude |
| Root `package.json` and `dist/pi/mamitsu/` | Pi |
| `dist/grok-bot/mamitsu/` | Grok Bot five-skill variant |
| `dist/downloads/` | Individual skill ZIPs and Grok Bot instructions |

Grok Bot omits `x-post-extraction` and uses native X access for ordinary
X requests. All other packages retain X, including clients using a Grok model.

## Behavioral cases

`evals/activation-cases.json` covers skill selection, result shape, source
limits, source-content safety, and client-specific routing. Each case includes
expected and excluded skills plus observable behavior to check. The tests
validate case coverage; they do not measure model accuracy.
