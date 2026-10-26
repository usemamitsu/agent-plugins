import fs from 'node:fs';
import path from 'node:path';
import Ajv2020 from 'ajv/dist/2020.js';
import { parseDocument } from 'yaml';

const root = path.resolve(import.meta.dirname, '..');
const schemaRoot = path.join(root, 'tools/schemas');
const pluginSchema = JSON.parse(fs.readFileSync(path.join(schemaRoot, 'plugin.schema.json'), 'utf8'));
const mcpSchema = JSON.parse(fs.readFileSync(path.join(schemaRoot, 'mcp.schema.json'), 'utf8'));
const ajv = new Ajv2020({ allErrors: true, strict: false });
const validatePlugin = ajv.compile(pluginSchema);
const validateMcp = ajv.compile(mcpSchema);
const validateClientInstalls = ajv.compile(JSON.parse(fs.readFileSync(
  path.join(root, 'docs/client-installs.schema.json'), 'utf8')));

const artifacts = [
  ['plugin.json', validatePlugin],
  ['dist/portable/mamitsu/plugin.json', validatePlugin],
  ['dist/grok-bot/mamitsu/plugin.json', validatePlugin],
  ['mcp.json', validateMcp],
  ['dist/portable/mamitsu/mcp.json', validateMcp],
  ['dist/grok-bot/mamitsu/mcp.json', validateMcp],
  ['docs/client-installs.json', validateClientInstalls],
];
let failures = 0;
for (const [relative, validate] of artifacts) {
  const file = path.join(root, relative);
  const value = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!validate(value)) {
    failures++;
    console.error(`${relative}: ${ajv.errorsText(validate.errors, { separator: '; ' })}`);
  } else {
    console.log(`${relative}: valid`);
  }
}

// Check the actual YAML and every bundled local link, not a frontmatter substring.
function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(directory, entry.name);
    return entry.isDirectory() ? walk(file) : [file];
  });
}
for (const file of [...walk(path.join(root, 'skills')), ...walk(path.join(root, 'dist'))]
  .filter(file => file.endsWith('/SKILL.md'))) {
  const relative = path.relative(root, file);
  try {
    const text = fs.readFileSync(file, 'utf8');
    const match = /^---\n([\s\S]*?)\n---\n/.exec(text);
    if (!match) throw new Error('missing YAML frontmatter');
    const document = parseDocument(match[1], { uniqueKeys: true });
    if (document.errors.length) throw new Error(document.errors.map(e => e.message).join('; '));
    const value = document.toJS();
    if (!value || Array.isArray(value)) throw new Error('frontmatter must be an object');
    const allowed = ['name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'];
    if (Object.keys(value).some(key => !allowed.includes(key))) throw new Error('unknown frontmatter field');
    if (typeof value.name !== 'string' || value.name.length > 64 ||
        !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value.name) ||
        value.name !== path.basename(path.dirname(file))) throw new Error('invalid skill name');
    if (typeof value.description !== 'string' || !value.description.trim() ||
        value.description.length > 1024) throw new Error('invalid skill description');
    if (text.split('\n').length > 500) throw new Error('skill exceeds 500-line loading budget');
    for (const link of text.matchAll(/\]\(([^)]+)\)/g)) {
      if (/^(?:https?:|#|mailto:)/.test(link[1])) continue;
      const target = path.resolve(path.dirname(file), link[1].split('#')[0]);
      if (!target.startsWith(path.dirname(file) + path.sep) || !fs.existsSync(target)) {
        throw new Error(`missing or non-bundled reference: ${link[1]}`);
      }
    }
  } catch (error) {
    failures++;
    console.error(`${relative}: ${error.message}`);
  }
}
console.log('Skill YAML, names, descriptions, loading budget, and bundled links checked.');
if (failures) process.exitCode = 1;
