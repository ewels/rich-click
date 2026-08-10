// Single source of truth for site metadata and top-level navigation.
// Plain JavaScript so it can be imported from astro.config.mjs, node scripts
// (scripts/prepare-content.mjs) and TypeScript/Astro modules alike.

export const SITE_TITLE = 'rich-click';
export const SITE_TAGLINE = 'Richly rendered command line interfaces in click.';

// The Live Style Editor is a custom page (src/pages/editor.astro) outside the
// content collection, so pieces like social cards need its metadata here.
export const EDITOR_PAGE = {
  label: 'Live Style Editor',
  description: 'A live editor for rich-click styles.',
};

// Starlight sidebar config; the header tabs row (components/Header.astro) is
// derived from the same top-level entries.
export const sidebar = [
  { label: 'Home', link: '/' },
  { label: EDITOR_PAGE.label, link: '/editor/' },
  {
    label: 'Documentation',
    items: [
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
      { label: 'Typer Support', slug: 'documentation/typer_support' },
      { label: 'Accessibility', slug: 'documentation/accessibility' },
    ],
  },
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
