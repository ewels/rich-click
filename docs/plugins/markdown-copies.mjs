// Tidies the Markdown copy of each page: starlight-page-actions publishes each
// page's source as `.md` (with its front matter replaced by a `# title`), and
// starlight-pydocs writes `.md` and identical `.md.txt` copies of the API pages.
import { existsSync } from 'node:fs';
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { SITE_TITLE } from '../src/site.mjs';

// Strip the `{/* RICH-CODEX ... */}` image-generation blocks (and other MDX
// comments), which are noise to whoever reads the Markdown, but not from code
// examples. Closing fences may be followed by text: tidymd renders inline
// `<Code>` that way.
const FENCE_OR_MDX_COMMENT = /^ {0,3}(`{3,}|~{3,})[^\n]*\n[\s\S]*?^ {0,3}\1|\{\/\*[\s\S]*?\*\/\}\n?/gm;
/** @param {string} markdown */
const stripMdxComments = (markdown) =>
  markdown.replace(FENCE_OR_MDX_COMMENT, (match, fence) => (fence ? match : ''));

/** @type {Record<string, string>} */
const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', '#39': "'", '#x27': "'" };
/** @param {string} html @param {RegExp} pattern */
const htmlAttr = (html, pattern) =>
  html.match(pattern)?.[1]?.replace(/&(amp|lt|gt|quot|#39|#x27);/g, (_, name) => ENTITIES[name]);

/**
 * YAML front matter from a page's built HTML, so it carries the same title,
 * description and canonical URL as the page itself. Blog posts add their date,
 * authors and tags from starlight-blog's structured data.
 * @param {string} html
 */
function frontMatter(html) {
  /** @type {Record<string, string | string[] | undefined>} */
  const fields = {
    project: SITE_TITLE,
    title: htmlAttr(html, /<meta property="og:title" content="([^"]*)"/),
    description: htmlAttr(html, /<meta name="description" content="([^"]*)"/),
    url: htmlAttr(html, /<link rel="canonical" href="([^"]*)"/),
  };
  const jsonLd = html.match(/<script type="application\/ld\+json">([^<]*)<\/script>/)?.[1];
  /** @type {any} */
  const post = jsonLd && JSON.parse(jsonLd)['@graph']?.find((/** @type {any} */ node) => node['@type'] === 'BlogPosting');
  if (post) {
    fields.date = post.datePublished?.slice(0, 10);
    fields.authors = post.author?.map((/** @type {{ name: string }} */ author) => author.name);
    fields.tags = post.keywords;
  }

  const lines = [];
  for (const [key, value] of Object.entries(fields)) {
    if (Array.isArray(value)) {
      if (value.length) lines.push(`${key}:`, ...value.map((item) => `  - ${JSON.stringify(item)}`));
    } else if (value !== undefined) {
      // The date unquoted, so YAML reads it as a date.
      lines.push(`${key}: ${key === 'date' ? value : JSON.stringify(value)}`);
    }
  }
  return `---\n${lines.join('\n')}\n---\n\n`;
}

/** @type {import('astro').AstroIntegration} */
export const markdownCopies = {
  name: 'rich-click:markdown-copies',
  hooks: {
    'astro:build:done': async ({ dir }) => {
      const entries = await readdir(fileURLToPath(dir), { recursive: true });
      for (const entry of entries.filter((name) => /\.md(\.txt)?$/.test(name))) {
        const path = fileURLToPath(new URL(entry, dir));
        // `guide/page.md` is the copy of `guide/page/index.html`.
        const htmlPath = path.replace(/\.md(\.txt)?$/, '/index.html');
        const header = existsSync(htmlPath) ? frontMatter(await readFile(htmlPath, 'utf8')) : '';
        const original = await readFile(path, 'utf8');
        const updated = header + stripMdxComments(original);
        if (updated !== original) await writeFile(path, updated);
      }
    },
  },
};
