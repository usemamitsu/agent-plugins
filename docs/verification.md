# Package checks

From a repository checkout, run:

```sh
npm ci
npm run check
```

The checks validate:

- Generated file contents and package versions.
- Agent Plugins schemas, client install metadata, and skill YAML.
- All six standalone skills, bundled references, and relative links.
- Download digests and reproducible ZIP contents.
- Grok Bot's five-skill boundary and X support in other clients.

To list the independently installable skills:

```sh
npx skills add usemamitsu/agent-plugins --list
```

## Client package routes

| Client | Installation route | Update |
|---|---|---|
| Claude web/desktop | Marketplace plugin or individual skill upload | Marketplace update or replacement skill upload |
| Claude Code | Native plugin marketplace | `claude plugin update mamitsu@mamitsu` |
| ChatGPT | Custom MCP plugin and separate skill upload | Refresh MCP tools and replace uploaded skills |
| Codex | Native plugin marketplace | `codex plugin marketplace upgrade mamitsu` |
| Cursor | Customize > mamitsu > Install | Update in Customize |
| Hermes | `dist/portable/mamitsu` plugin | `hermes plugins update mamitsu` |
| Pi | Native Git package | `pi update --extensions` |
| Grok Bot | Custom MCP server and saved private skills | Replace saved instructions from the Grok Bot collection |
| Other agents | Remote MCP and independently installed skills | Client MCP controls and `npx skills update` |

See [installation instructions](install.md) for complete commands, downloads,
and account connection steps. Package checks validate distribution contents;
sign-in and consent happen separately in your client.
