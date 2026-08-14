import type { APIContext } from 'astro';
import { getBlogPosts, jsonFeed } from '../feeds';

export async function GET(context: APIContext) {
  return jsonFeed(context.site, await getBlogPosts());
}
