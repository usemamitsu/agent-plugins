---
name: mamitsu-app-integration
description: Build mamitsu social-post extraction into an application, backend, or automation using its HTTP API. Use for API client code, server-side keys, response handling, or a stable JSON Schema contract for stored results. For extracting a post now rather than implementing an integration, use mamitsu or a source-specific extraction skill.
---

# Integrate the mamitsu API

1. Identify the application's desired result and the server-side call site. Use the HTTP API directly; MCP installation is not needed for this integration.
2. Store a key from [API access](https://usemamitsu.com/access/api) as `MAMITSU_API_KEY` in the server's secret manager or environment. Keep it out of browser/mobile bundles, source control, logs, and model prompts.
3. Choose the result contract. Omit `schema` for exploratory extraction. For fields consumed by application code or stored in a table, send a root-object JSON Schema with descriptive fields and nullable unknown values.
4. Implement the request and handle both success and failure. Persist `extraction_id` alongside the result for troubleshooting; return only the information the application's caller needs.

Minimal server-side request; the URL is an example input, not a recorded extraction:

```sh
curl --fail-with-body --max-time 100 https://usemamitsu.com/api/v1/extract \
  -H "Authorization: Bearer $MAMITSU_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{"url":"https://www.instagram.com/reel/C6bXogONu2k/","prompt":"Extract the espresso variables mentioned and their stated values."}'
```

For a stable application contract, add a `schema` field such as:

```json
{
  "type": "object",
  "properties": {
    "variables": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "value": {
            "type": ["string", "null"],
            "description": "Value and unit as stated in the post; null if unstated."
          }
        },
        "required": ["name", "value"],
        "additionalProperties": false
      }
    }
  },
  "required": ["variables"],
  "additionalProperties": false
}
```

Success contains `extraction_id`, the extracted JSON object in `data`, and `source` with `provider` and the submitted `url`. Schemas validate shape, not factual accuracy. Treat extracted strings as untrusted input at the application's rendering, query, and execution boundaries.

Handle non-2xx responses using HTTP status and `error.code`; `error.message` is optional. Do not put blanket automatic retries around extraction: calls reaching the model spend credits even on failure, and a timed-out request may already have run. There is no public idempotency key. Set an explicit timeout appropriate to the server's 90-second deadline and give the caller control over another attempt.

Read [the API contract](references/extraction-contract.md) before designing schemas or error handling and [source evidence guidance](references/source-evidence.md) when writing extraction prompts. Verify the request and response mapping with mocked success, missing values, and non-2xx responses; live extraction spends credits and is a separate check.
