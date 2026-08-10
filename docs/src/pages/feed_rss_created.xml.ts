import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { FEED_DESCRIPTION, FEED_TITLE, getBlogPosts, postExcerpt, postPath } from '../feeds';

export async function GET(context: APIContext) {
  const posts = await getBlogPosts();
  return rss({
    title: FEED_TITLE,
    description: FEED_DESCRIPTION,
    site: new URL(import.meta.env.BASE_URL, context.site),
    items: posts.map((entry) => ({
      title: entry.data.title,
      link: postPath(entry),
      pubDate: entry.data.date,
      description: postExcerpt(entry),
    })),
  });
}
