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

/** Site slug for a Markdown source file (`''` for the root index page). */
function slugFor(absolutePath) {
  return path
    .relative(CONTENT_ROOT, absolutePath)
    .replace(/\\/g, '/')
    .replace(/\.(md|mdx)$/, '')
    .replace(/(^|\/)index$/, '');
}

export function satteriMdLinks() {
  // Per-file relative prefix cache: one entry per document, hit once per link.
  const prefixCache = new Map();

  return {
    name: 'rich-click-md-links',
    link(node, ctx) {
      if (!ctx.fileURL) return;
      const match = MD_LINK_RE.exec(node.url);
      if (!match) return;
      const [, target, fragment = ''] = match;

      const currentDir = path.dirname(fileURLToPath(ctx.fileURL));
      const slug = slugFor(path.resolve(currentDir, `${target}.md`));

      // Emit a URL relative to the current page so it works under any base path.
      // Page URLs always end in a trailing slash (directory-style routing).
      let prefix = prefixCache.get(ctx.fileURL.href);
      if (prefix === undefined) {
        const currentSlug = slugFor(fileURLToPath(ctx.fileURL));
        prefix = '../'.repeat(currentSlug === '' ? 0 : currentSlug.split('/').length);
        prefixCache.set(ctx.fileURL.href, prefix);
      }
      const url = `${prefix}${slug === '' ? '' : `${slug}/`}${fragment}`;
      ctx.setProperty(node, 'url', url);
    },
  };
}
