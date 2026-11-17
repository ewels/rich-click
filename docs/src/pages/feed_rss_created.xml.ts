import rss from '@astrojs/rss';
import type { APIContext } from 'astro';
import { feedMeta, getBlogPosts, postExcerpt, postPath } from '../feeds';

export async function GET(context: APIContext) {
  const { title, description, homeUrl } = feedMeta(context.site);
  const posts = await getBlogPosts();
  return rss({
    title,
    description,
    site: homeUrl,
    items: posts.map((entry) => ({
      title: entry.data.title,
      link: postPath(entry),
      pubDate: entry.data.date,
      description: postExcerpt(entry),
    })),
  });
}
