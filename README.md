# mamitsu for agents

Turn public YouTube, Instagram, TikTok, and X posts into useful information.
mamitsu reads the post's text and media; these skills help your agent ask the
right questions and work with the result.

## Install

```sh
npx skills add usemamitsu/agent-plugins
```

Choose your agent and skills, or install one directly:

```sh
npx skills add usemamitsu/agent-plugins --skill instagram-extraction
```

Connect **`https://usemamitsu.com/mcp`** in your agent, sign in with GitHub,
and approve mamitsu. Skills provide instructions; MCP provides the `extract`
tool. You can install either independently.

**[Install for your client →](docs/install.md)** — Claude, Claude Code,
ChatGPT, Codex, Cursor, Hermes, Pi, Grok Bot, and other agents.

## Choose a skill

| Skill | Use it for |
|---|---|
| [`mamitsu`](skills/mamitsu/SKILL.md) | General extraction and choosing useful source-specific guidance |
| [`mamitsu-app-integration`](skills/mamitsu-app-integration/SKILL.md) | Building HTTP API extraction into an application |
| [`youtube-extraction`](skills/youtube-extraction/SKILL.md) | Tutorials, demonstrations, reviews, lectures, and Shorts |
| [`instagram-extraction`](skills/instagram-extraction/SKILL.md) | Reels, images, captions, and multi-slide carousels |
| [`tiktok-extraction`](skills/tiktok-extraction/SKILL.md) | Short-video demonstrations, hooks, offers, and CTAs |
| [`x-post-extraction`](skills/x-post-extraction/SKILL.md) | One post's text, images, video, and GIFs |

Each skill includes its references and works on its own. The Grok Bot
collection contains five skills and uses Grok's native X access for ordinary
X requests. All other clients retain the X skill, including those running a
Grok model.

## Update

For standalone skills, run `npx skills check` followed by `npx skills update`.
For a plugin, use [your client's update steps](docs/install.md).

[Client install contract](docs/client-installs.json) ·
[Package development](docs/README.md) ·
[mamitsu API docs](https://usemamitsu.com/docs)
