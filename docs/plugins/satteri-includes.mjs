// Replaces mkdocs-include-markdown-style `{% include "path" %}` directives found
// inside fenced code blocks with the contents of the referenced file, so code
// samples can be kept in standalone, runnable files (docs/src/content/docs/code_snippets).
//
// Optional `start="..."` / `end="..."` arguments slice the file between two
// marker strings (the markers themselves are excluded), e.g.:
//
//     ```python
//     {%
//         include '../../src/rich_click/rich_click.py'
//         start="#!STARTCONFIG"
//         end="#!ENDCONFIG"
//     %}
//     ```
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const INCLUDE_RE = /\{%-?\s*include(?:-markdown)?\s+["']([^"']+)["']([\s\S]*?)-?%\}/g;

function readInclude(spec, args, fileURL) {
  const dir = path.dirname(fileURLToPath(fileURL));
  const target = path.resolve(dir, spec);
  let content = fs.readFileSync(target, 'utf8');
  const start = /start\s*=\s*"([^"]+)"/.exec(args)?.[1];
  const end = /end\s*=\s*"([^"]+)"/.exec(args)?.[1];
  if (start) {
    const idx = content.indexOf(start);
    if (idx === -1) throw new Error(`start marker ${start} not found in ${target}`);
    content = content.slice(idx + start.length);
  }
  if (end) {
    const idx = content.indexOf(end);
    if (idx === -1) throw new Error(`end marker ${end} not found in ${target}`);
    content = content.slice(0, idx);
  }
  return content.replace(/^\r?\n/, '').replace(/\s+$/, '');
}

export function satteriIncludes() {
  return {
    name: 'rich-click-includes',
    code(node, ctx) {
      if (!node.value || !node.value.includes('{%') || !ctx.fileURL) return;
      let failed = false;
      const value = node.value.replace(INCLUDE_RE, (match, spec, args) => {
        try {
          return readInclude(spec, args, ctx.fileURL);
        } catch (error) {
          failed = true;
          ctx.report({ message: `Failed to process include: ${error.message}`, node, severity: 'error' });
          return match;
        }
      });
      if (!failed && value !== node.value) ctx.setProperty(node, 'value', value);
    },
  };
}
