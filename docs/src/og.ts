// Social cards: one per docs/blog page, keyed by collection entry id, plus the
// custom homepage and Live Style Editor pages.
import { getCollection } from 'astro:content';
import { EDITOR_PAGE, SITE_TAGLINE, SITE_TITLE } from './site.mjs';

interface OgPageData {
  title: string;
  description: string;
}

/** A frontmatter title without the `backticks` PageTitle.astro renders as inline code. */
export const plainTitle = (title: string): string => title.replaceAll('`', '');

const entries = await getCollection('docs');

export const ogPages: Record<string, OgPageData> = Object.fromEntries([
  ...entries.map((entry) => [
    entry.id,
    { title: plainTitle(entry.data.title), description: entry.data.description ?? SITE_TAGLINE },
  ]),
  ['index', { title: SITE_TITLE, description: SITE_TAGLINE }],
  ['editor', { title: EDITOR_PAGE.label, description: EDITOR_PAGE.description }],
]);
