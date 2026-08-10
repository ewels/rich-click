// Shared data for the auto-generated social cards: every docs/blog page gets a
// card keyed by its collection entry id, plus one for the Live Style Editor
// (a custom page outside the content collection). Used by the image endpoint
// (pages/og/[...slug].ts) and the route middleware (starlight-route-data.ts).
import { getCollection } from 'astro:content';

export const SITE_TAGLINE = 'Richly rendered command line interfaces in click.';

interface OgPageData {
  title: string;
  description: string;
}

const entries = await getCollection('docs');

export const ogPages: Record<string, OgPageData> = Object.fromEntries([
  ...entries.map((entry) => [
    entry.id,
    { title: entry.data.title, description: entry.data.description ?? SITE_TAGLINE },
  ]),
  ['editor', { title: 'Live Style Editor', description: 'A live editor for rich-click styles.' }],
]);
