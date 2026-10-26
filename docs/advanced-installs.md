# Advanced installs

Use [the customer install steps](install.md) for native client installation.
These alternatives let you inspect and manage a local plugin checkout.

## Cursor local plugin

Cursor supports an alternative local Git checkout:

```sh
mkdir -p ~/.cursor/plugins/local
git clone https://github.com/usemamitsu/agent-plugins.git ~/.cursor/plugins/local/mamitsu
```

Run **Developer: Reload Window** and inspect the skills and MCP server in
**Customize**. Connect mamitsu and complete OAuth. On managed workspaces,
local imports require the administrator's **Allow Local Plugin Imports** setting.

Update this local checkout and reload the window:

```sh
git -C ~/.cursor/plugins/local/mamitsu pull --ff-only
```

Use **Customize > mamitsu > Install** for native plugin management, or maintain
the Git checkout directly with the commands above.

[Cursor plugin documentation](https://cursor.com/docs/plugins)
