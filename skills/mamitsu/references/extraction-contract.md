# mamitsu extraction contract

Request and source behavior shared by the public API and MCP.

## Agent and API request

`POST https://usemamitsu.com/api/v1/extract` accepts JSON with required `url`
and `prompt` (1–10,000 characters after trimming), and optional `schema`.
Unknown request keys are rejected; omit `schema` rather than sending `null`.
Authenticate API requests with a
server-side `Authorization: Bearer xtk_…` key. Never expose that key in a
browser, mobile bundle, prompt, or client-visible log. MCP uses the same
inputs through `extract` and OAuth instead of an API key.

Without `schema`, mamitsu chooses descriptive JSON object fields from the
prompt. Missing scalar facts are `null`, absent observed collections are `[]`,
and unrelated fields are omitted. No schema is generated or returned. Use an
optional root-object JSON Schema only when downstream code needs a fixed,
validated shape. This is shape validation, not a guarantee of semantic
correctness. The accepted subset includes types, descriptions/titles, object
properties/required/additionalProperties, arrays/items/minItems/maxItems,
enum, numeric bounds, date/date-time/time formats, and anyOf. `$ref`, `$defs`,
`pattern`, `minLength`, and unsupported JSON Schema keywords are rejected.
Schema maximum is 16 KiB, depth 8, 200 nodes; request body max 64 KiB.

Success: `{ "extraction_id": "...", "data": { ... }, "source": { "provider": "...", "url": "..." } }`.
REST failures use `{ "extraction_id": "...", "error": { "code": "...", "message"?: "..." } }`.
MCP returns the same values in `structuredContent` and text; extraction
failures set `isError`. Authentication and invalid MCP protocol requests are
transport/protocol errors instead. Public API errors include `unauthorized` (401),
`insufficient_credits` (402), `account_not_enabled` (403),
`invalid_request`/`invalid_schema` (400), `payload_too_large` (413),
`unsupported_url`/source and media limits (422), and model/output failures
`invalid_extraction`/`extraction_failed` (502). Do not retry automatically:
calls reaching the model spend credits, including model failures. Validation,
discovery and source failures before the model are free.

## Supported public sources and limits

- YouTube videos, Shorts, `watch?v=` and `youtu.be`, up to 30 minutes.
  Use HTTPS links with just the video ID, without extra query parameters or
  fragments. A request about a segment is still subject to the whole video's
  length limit.
- Instagram posts, reels and carousels: up to 20 media items; videos up to
  five minutes combined per post. Caption and attached media are evidence.
  `img_index` selects the whole post, not one slide.
- TikTok videos up to five minutes; photo posts are not supported. Full
  `/@user/video/<id>` links, `m.tiktok.com/v/<id>.html`, `vm.`/`vt.tiktok.com`
  share links and `www.tiktok.com/t/<code>` are supported.
- X/Twitter posts: text, up to four attached images/videos/GIFs, six minutes of
  video combined, 32 MiB per image, 50 MiB per video, and 64 MiB total.
  Native attachment permalinks select the whole post. Surrounding conversation,
  quoted-post targets and linked sites are not included. A reply can be
  extracted as its own post using its status URL.

Only public posts are supported. The source may be inaccessible, changed,
removed, or withheld. Base the answer on the post's text, images, visible
actions and speech. Do not infer unseen content or treat linked pages as
part of the post.
The server's extraction deadline is 90 seconds. There is no public batch,
webhook, SDK, or idempotency-key contract. Use separate requests for separate
posts and avoid automatic retries after ambiguous network failures.

## Charging

Each extraction that reaches the model costs at least one credit. Non-YouTube video
costs one credit per started minute; photos cost one per started three images,
added together for mixed posts. YouTube costs one per started minute for the
first five minutes, then one per started five-minute block. Source and
validation failures before the model is reached are free. These rates describe
extraction credits, not monetary pricing.

See the [public API documentation](https://usemamitsu.com/docs) for the full
reference.
