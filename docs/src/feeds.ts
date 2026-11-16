// Legacy feed endpoints (src/pages/feed_*.ts), kept so the URLs the old site
// published keep working. starlight-blog serves its own feed at /blog/rss.xml.
import { getCollection, type CollectionEntry } from 'astro:content';
import { base } from './base';
import { SITE_TAGLINE, SITE_TITLE } from './site.mjs';

export async function getBlogPosts(): Promise<CollectionEntry<'docs'>[]> {
  const posts = await getCollection(
    'docs',
    (entry) =>
      entry.id.startsWith('blog/') &&
      entry.data.date !== undefined &&
      !(import.meta.env.PROD && entry.data.draft)
  );
  return posts.sort((a, b) => b.data.date!.getTime() - a.data.date!.getTime());
}

export function postPath(entry: CollectionEntry<'docs'>): string {
  return `${base}/${entry.id}/`;
}

function postUrl(site: URL | undefined, entry: CollectionEntry<'docs'>): string {
  return new URL(postPath(entry), site).href;
}

export const feedMeta = (site: URL | undefined) => ({
  title: SITE_TITLE,
  description: SITE_TAGLINE,
  homeUrl: new URL(`${base}/`, site).href,
});

// Markdown posts mark the end of their summary with an HTML comment; MDX posts
// use a JSX comment, since MDX forbids HTML comments.
const EXCERPT_DELIMITER = /<!--\s*excerpt\s*-->|\{\/\*\s*excerpt\s*\*\/\}/;

/**
 * Plain-text post excerpt for feed descriptions: the frontmatter `excerpt` if
 * set, otherwise the post body up to the excerpt delimiter.
 */
export function postExcerpt(entry: CollectionEntry<'docs'>): string | undefined {
  const source = entry.data.excerpt ?? entry.body?.split(EXCERPT_DELIMITER)[0];
  if (!source) return undefined;
  return source
    .replace(/^\s*import\s.+$/gm, '') // MDX imports precede the excerpt
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '') // images
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1') // links -> text
    .replace(/[*_`]/g, '')
    .trim();
}

export function jsonFeed(site: URL | undefined, posts: CollectionEntry<'docs'>[]) {
  const { title, description, homeUrl } = feedMeta(site);
  return Response.json({
    version: 'https://jsonfeed.org/version/1',
    title,
    home_page_url: homeUrl,
    description,
    items: posts.map((entry) => ({
      id: postUrl(site, entry),
      url: postUrl(site, entry),
      title: entry.data.title,
      date_published: entry.data.date!.toISOString(),
    })),
  });
}
