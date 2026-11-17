// Single source of truth for site metadata and top-level navigation.
// Plain JavaScript so it can be imported from astro.config.mjs, node scripts
// (scripts/prepare-content.mjs) and TypeScript/Astro modules alike.

export const SITE_TITLE = 'rich-click';
export const SITE_TAGLINE = 'Richly rendered command line interfaces in Click.';
export const REPO = 'ewels/rich-click';
export const REPO_URL = `https://github.com/${REPO}`;

// The Live Style Editor is a custom page (src/pages/editor.astro) outside the
// content collection, so pieces like social cards need its metadata here.
export const EDITOR_PAGE = {
  label: 'Live Style Editor',
  link: '/editor/',
  description: 'A live editor for rich-click styles.',
};

// Avatars are self-hosted, named by key: src/assets/authors/<key>.jpg (src/avatars.ts).
export const BLOG_AUTHORS = {
  ewels: {
    name: 'Phil Ewels',
    title: 'rich-click creator',
    url: 'https://github.com/ewels',
  },
  dwreeves: {
    name: 'Daniel Reeves',
    title: 'Co-maintainer',
    url: 'https://github.com/dwreeves',
  },
};

// Keep in sync with BASE_PREFIX/DEFAULT_ALIAS in docs/_deploy.py.
export const BASE_PREFIX = '/rich-click';
export const DEFAULT_ALIAS = 'latest';
/** Base path when ASTRO_BASE isn't set. */
export const DEFAULT_BASE = `${BASE_PREFIX}/${DEFAULT_ALIAS}`;

// Root of the generated API reference pages (starlight-pydocs `base` default).
export const API_PATH = '/api/rich_click/';

// Social cards: the logo is pre-padded to the width between the card paddings
// by scripts/prepare-content.mjs, and drawn by src/pages/og/[...slug].ts.
export const OG_CARD = { width: 1200, padding: 36, logo: 'src/generated/og-logo.png' };

// Starlight sidebar config; the header tabs row (components/Header.astro) is
// derived from the same top-level entries.
export const sidebar = [
  { label: 'Home', link: '/' },
  { label: EDITOR_PAGE.label, link: EDITOR_PAGE.link },
  {
    label: 'Documentation',
    items: [
      { label: 'Quickstart', slug: 'documentation/quickstart' },
      { label: 'Introduction to Click', slug: 'documentation/introduction_to_click' },
      {
        label: 'Comparison of Click & rich-click',
        slug: 'documentation/comparison_of_click_and_rich_click',
      },
      { label: 'Themes', slug: 'documentation/themes' },
      { label: 'Configuration', slug: 'documentation/configuration' },
      {
        label: 'Panels',
        items: [
          { label: 'Overview', slug: 'documentation/panels/overview' },
          { label: 'Tips', slug: 'documentation/panels/tips' },
          { label: 'Advanced', slug: 'documentation/panels/advanced' },
        ],
      },
      {
        label: 'Text Markup & Formatting',
        slug: 'documentation/text_markup_and_formatting',
      },
      { label: 'Custom Styles', slug: 'documentation/custom_styles' },
      { label: 'rich-click CLI tool', slug: 'documentation/rich_click_cli' },
      { label: 'Asyncclick Support', slug: 'documentation/asyncclick_support' },
      { label: 'Typer Support', slug: 'documentation/typer_support' },
      { label: 'Accessibility', slug: 'documentation/accessibility' },
      { label: 'Testing', slug: 'documentation/testing' },
    ],
  },
  // A link here so the header tab has somewhere to point; astro.config.mjs
  // turns it into the starlight-pydocs placeholder group for the sidebar.
  { label: 'API Reference', link: API_PATH },
  { label: 'Blog', link: '/blog/' },
  { label: 'Changelog', slug: 'changelog' },
  { label: 'Contributing', slug: 'contributing' },
];

/** Root-relative URL path (no base) for a sidebar entry; groups resolve to their first page. */
export function entryPath(entry) {
  if (entry.link) return entry.link;
  if (entry.slug) return `/${entry.slug}/`;
  return entryPath(entry.items[0]);
}
