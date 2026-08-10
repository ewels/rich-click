// Resolves mkdocs-style relative links to other Markdown source files
// (e.g. `[Themes](themes.md)` or `[editor](../editor.md)`) into site URLs,
// matching how mkdocs rewrote them relative to the source file.
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const CONTENT_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  '../src/content/docs'
);

const MD_LINK_RE = /^(?!ftp:|https?:|mailto:|#|\/)(.*)\.md(#.*)?$/;

export function satteriMdLinks() {
  return {
    name: 'rich-click-md-links',
    link(node, ctx) {
      if (!ctx.fileURL) return;
      const match = MD_LINK_RE.exec(node.url);
      if (!match) return;
      const [, target, fragment = ''] = match;

      const currentDir = path.dirname(fileURLToPath(ctx.fileURL));
      const targetPath = path.resolve(currentDir, `${target}.md`);
      let slug = path.relative(CONTENT_ROOT, targetPath).replace(/\\/g, '/');
      slug = slug.replace(/\.md$/, '').replace(/(^|\/)index$/, '');

      // The Live Style Editor page is a custom Astro page rather than content.
      if (slug === 'editor') slug = 'editor';

      // Emit a URL relative to the current page so it works under any base path.
      // Page URLs always end in a trailing slash (directory-style routing).
      const currentSlug = path
        .relative(CONTENT_ROOT, fileURLToPath(ctx.fileURL))
        .replace(/\\/g, '/')
        .replace(/\.(md|mdx)$/, '')
        .replace(/(^|\/)index$/, '');
      const depth = currentSlug === '' ? 0 : currentSlug.split('/').length;
      const prefix = '../'.repeat(depth);
      const url = `${prefix}${slug === '' ? '' : `${slug}/`}${fragment}`;
      ctx.setProperty(node, 'url', url);
    },
  };
}
