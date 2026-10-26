import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerMcpServer("mamitsu", {
    url: "https://usemamitsu.com/mcp",
    description: "Extract structured data from public social posts.",
  });
}
