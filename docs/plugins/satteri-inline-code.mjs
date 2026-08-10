// Syntax highlighting for inline code with a `#!lang` prefix, e.g.
// `` `#!python import rich_click as click` `` — the same terse syntax the old
// mkdocs pymdownx.inlinehilite extension used. Highlighted with Shiki using
// light/dark CSS variables (applied by a rule in src/styles/custom.css).
import { codeToHtml } from 'shiki';

const SHEBANG_RE = /^#!([\w-]+) /;

export function satteriInlineCode() {
  return {
    name: 'rich-click-inline-code',
    async inlineCode(node) {
      const match = SHEBANG_RE.exec(node.value);
      if (!match) return;
      const code = node.value.slice(match[0].length);
      const spans = await codeToHtml(code, {
        lang: match[1],
        themes: { light: 'github-light', dark: 'github-dark' },
        defaultColor: false,
        structure: 'inline',
      });
      return { type: 'html', value: `<code>${spans}</code>` };
    },
  };
}
