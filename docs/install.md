# Install mamitsu

Connect MCP for the extraction tool. Add skills for reusable extraction
workflows. Plugin-capable clients can install both together.

## Claude web and desktop

1. Open **Customize > Plugins > Add > Add marketplace**.
2. Enter `usemamitsu/agent-plugins` and install **mamitsu**.
3. In the plugin's **Connectors** section, choose **Add** or **Connect** for
   mamitsu. Sign in with GitHub and approve access.

Update mamitsu through its marketplace in **Customize > Plugins**.

**MCP only:** [Add the mamitsu connector](https://claude.ai/customize/connectors?modal=add-custom-connector&connectorName=mamitsu&connectorUrl=https%3A%2F%2Fusemamitsu.com%2Fmcp).
Confirm the connector and sign in. This installs no skills.

**Skills only:** download an individual [skill ZIP](#downloadable-skills),
upload it under **Customize > Skills**, and enable it. To update an uploaded
skill, replace it with the current ZIP.

[Claude's plugin instructions](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)

## Claude Code

```sh
claude plugin marketplace add usemamitsu/agent-plugins
claude plugin install mamitsu@mamitsu
```

Start Claude Code, run `/mcp`, select mamitsu, and finish sign-in.

Update:

```sh
claude plugin marketplace update mamitsu
claude plugin update mamitsu@mamitsu
```

Restart Claude Code to apply the update.
[Claude Code plugin instructions](https://code.claude.com/docs/en/discover-plugins)

## ChatGPT

Install the MCP plugin and skills separately in your ChatGPT account.

### Connect MCP

1. In ChatGPT on the web, open **Plugins > + > Add custom MCP server**.
2. Name it **mamitsu**. Under **Connection**, enter
   `https://usemamitsu.com/mcp` and select OAuth. Review the permissions,
   choose **Create as a plugin**, and install the resulting MCP plugin.
3. Complete GitHub sign-in and mamitsu consent. Start a new conversation,
   type `@`, and choose **mamitsu**.

### Add skills

1. Download the individual [skill ZIPs](#downloadable-skills) you want.
2. Open **Plugins > Skills > Create > Upload from your computer**.
3. Upload each skill and complete its review.

Uploading a skill does not connect the MCP plugin. To update, refresh MCP tools
in the plugin settings. Download the current ZIPs and replace uploaded skills
separately in **Plugins > Skills**.

[ChatGPT skills](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) ·
[Custom MCP servers](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)

## Codex

For Codex CLI with native plugin commands:

```sh
codex plugin marketplace add usemamitsu/agent-plugins
codex plugin add mamitsu@mamitsu
```

Complete the plugin's connection prompt in Codex. You can also browse and
install it through `/plugins` after adding the marketplace.

Update the marketplace, then start a new Codex session:

```sh
codex plugin marketplace upgrade mamitsu
```

[Using plugins in Codex](https://developers.openai.com/learn/developers-codex-plugin)

## Cursor

1. Open **Customize** in Cursor's sidebar and search for **mamitsu**.
2. Choose **Install** and select your project or user scope.
3. Find mamitsu's MCP server in **Customize** and choose **Connect**.
   Complete GitHub sign-in and mamitsu consent.

Update mamitsu in **Customize**, then start a new agent. For skills installed
separately, run `npx skills update`.

[Cursor plugin instructions](https://cursor.com/docs/plugins)

## Hermes

```sh
hermes plugins install usemamitsu/agent-plugins/dist/portable/mamitsu --no-enable
hermes plugins enable mamitsu
```

Start Hermes and complete mamitsu's MCP sign-in prompt.

Update, then start a new session:

```sh
hermes plugins update mamitsu
```

[Hermes plugin instructions](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins/)

## Pi

```sh
pi install git:github.com/usemamitsu/agent-plugins@main && pi "/mcp login mamitsu"
```

Pi loads mamitsu and its skills, then opens the browser for sign-in. Sign in
with GitHub and approve mamitsu. If Pi asks for first-run terminal setup,
press Enter to continue.

Update packages, then run `/reload` in an existing Pi session:

```sh
pi update --extensions
```

[Pi package instructions](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/packages.md)

## Grok Bot

Install MCP and skills separately. This collection uses Grok's native X access
for ordinary X requests, while mamitsu handles YouTube, Instagram, and TikTok.
Explicit mamitsu X requests and API integrations remain supported.

### Connect MCP

1. Ask your Bot to add a custom MCP server named **mamitsu**, using
   **Remote HTTPS** at `https://usemamitsu.com/mcp`.
2. Complete GitHub sign-in and mamitsu consent.

For a Team Bot, its owner or manager can manage the server in **Setup > Plugins**.
Each person signs in with their own account for OAuth plugins.

### Save the skills

1. Download a self-contained instruction file from the
   [Grok Bot collection](../dist/downloads/grok-bot/).
2. Give the Bot its contents and ask: **“Save these instructions as a skill
   named mamitsu, including the reference sections.”** Use the file's skill
   name for each additional skill.
3. If it is missing from the `/` menu, open **Connect apps**, select the
   connected count, and enable it under **Private skills**.

To update, download the current Grok Bot files and ask the Bot to replace the
saved instructions and references, keeping each skill's name. Use this
five-skill collection for both install and update; it excludes the X skill.

[Grok Bot skills](https://docs.x.ai/grok-bot/skills-routines-and-automations) ·
[Remote MCP and Team Bot setup](https://docs.x.ai/grok-bot/team-bots)

## Other agents and independent installs

**MCP:** add `https://usemamitsu.com/mcp` as a remote Streamable HTTP server
in a client with OAuth support. Sign in with GitHub and approve mamitsu.

**Skills:**

```sh
npx skills add usemamitsu/agent-plugins
```

Choose your agent and skills. To select one directly:

```sh
npx skills add usemamitsu/agent-plugins --skill instagram-extraction
```

Each skill carries its references. Standalone skill updates:

```sh
npx skills check
npx skills update
```

For MCP-only CLI configuration:

```sh
claude mcp add --transport http mamitsu https://usemamitsu.com/mcp
codex mcp add mamitsu --url https://usemamitsu.com/mcp
hermes mcp add mamitsu --url https://usemamitsu.com/mcp
pi mcp add mamitsu --url https://usemamitsu.com/mcp
```

Finish OAuth in your client. For standalone Codex and Pi configurations,
`codex mcp login mamitsu` and `pi mcp login mamitsu` start sign-in.
For Cursor, open **Customize > MCPs > Add New MCP Server**. Add mamitsu with
URL `https://usemamitsu.com/mcp`, then choose **Connect**.

## Downloadable skills

Each ZIP includes one skill directory, its `SKILL.md`, and both references.
Choose only the workflows you want.

| Skill | Download |
|---|---|
| mamitsu | [ZIP](https://raw.githubusercontent.com/usemamitsu/agent-plugins/main/dist/downloads/chatgpt/mamitsu.zip) |
| mamitsu-app-integration | [ZIP](https://raw.githubusercontent.com/usemamitsu/agent-plugins/main/dist/downloads/chatgpt/mamitsu-app-integration.zip) |
| youtube-extraction | [ZIP](https://raw.githubusercontent.com/usemamitsu/agent-plugins/main/dist/downloads/chatgpt/youtube-extraction.zip) |
| instagram-extraction | [ZIP](https://raw.githubusercontent.com/usemamitsu/agent-plugins/main/dist/downloads/chatgpt/instagram-extraction.zip) |
| tiktok-extraction | [ZIP](https://raw.githubusercontent.com/usemamitsu/agent-plugins/main/dist/downloads/chatgpt/tiktok-extraction.zip) |
| x-post-extraction | [ZIP](https://raw.githubusercontent.com/usemamitsu/agent-plugins/main/dist/downloads/chatgpt/x-post-extraction.zip) |

Grok Bot uses its [five written-instruction downloads](../dist/downloads/grok-bot/)
instead of these ZIPs. All downloadable files, URLs, and SHA-256 digests are
listed in the [download manifest](../dist/downloads/index.json).
