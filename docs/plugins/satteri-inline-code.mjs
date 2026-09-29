// Syntax highlighting for inline code with a `#!lang` prefix, e.g.
// `` `#!python import rich_click as click` `` — the same terse syntax the old
// mkdocs pymdownx.inlinehilite extension used. Highlighted with Shiki using
// light/dark CSS variables (applied by a rule in src/styles/custom.css).
import { codeToHtml } from 'shiki';

const SHEBANG_RE = /^#!([\w-]+) /;

export function satteriInlineCode() {
  return {
    name: 'rich-click-inline-code',
    async inlineCode(node, ctx) {
      const match = SHEBANG_RE.exec(node.value);
      if (!match) return;
      const code = node.value.slice(match[0].length);
      const spans = await codeToHtml(code, {
        lang: match[1],
        themes: { light: 'github-light', dark: 'github-dark' },
        defaultColor: false,
        structure: 'inline',
      });
      const html = `<code>${spans}</code>`;
      // Markdown and MDX require different AST shapes for raw HTML content.
      if (ctx.sourceFormat === 'mdx') {
        return {
          type: 'mdxJsxTextElement',
          name: 'Fragment',
          attributes: [{ type: 'mdxJsxAttribute', name: 'set:html', value: html }],
          children: [],
        };
      }
      return { type: 'html', value: html };
    },
  };
}
