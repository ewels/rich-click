// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { satteri } from '@astrojs/markdown-satteri';
import starlightBlog from 'starlight-blog';
import starlightLinksValidator from 'starlight-links-validator';

import { satteriIncludes } from './plugins/satteri-includes.mjs';
import { satteriAdmonitions } from './plugins/satteri-admonitions.mjs';
import { satteriTabs } from './plugins/satteri-tabs.mjs';
import { satteriImageAttrs } from './plugins/satteri-image-attrs.mjs';
import { satteriGithubAlerts } from './plugins/satteri-github-alerts.mjs';
import { satteriMdLinks } from './plugins/satteri-md-links.mjs';
import { satteriMermaid } from './plugins/satteri-mermaid.mjs';

// The site is deployed to versioned directories on GitHub Pages, mirroring the
// layout previously managed by `mike` (e.g. /rich-click/latest/, /rich-click/1.9/).
// `docs/_deploy.py` builds once per deployed alias, overriding the base path.
const site = 'https://ewels.github.io';
const base = process.env.ASTRO_BASE ?? '/rich-click/latest';

export default defineConfig({
  site,
  base,
  markdown: {
    processor: satteri({
      features: {
        directive: true,
      },
      mdastPlugins: [
        // Plugins operating on the pristine tree first; the structural
        // transforms (admonitions, tabs) come last.
        satteriIncludes(),
        satteriImageAttrs(),
        satteriMdLinks(),
        satteriMermaid(),
        satteriGithubAlerts(),
        satteriAdmonitions(),
        // Passed as a factory so the tab-set id counter resets per document.
        satteriTabs,
      ],
    }),
  },
  redirects: {
    // Carried over from the mkdocs-redirects plugin.
    '/documentation/groups_and_sorting': `${base}/documentation/panels/overview/`,
    '/documentation/formatting_and_styles': `${base}/documentation/text_markup_and_formatting/`,
    // The mkdocs-material blog used date-based URLs; starlight-blog uses flat slugs.
    '/blog/2024/04/30/version-1.8': `${base}/blog/version-1.8/`,
    '/blog/2024/11/13/three-pre-made-styles': `${base}/blog/three-pre-made-styles/`,
    '/blog/2024/11/15/pycon-sweden-2024': `${base}/blog/pycon-sweden-2024/`,
    '/blog/2025/09/16/version-1.9': `${base}/blog/version-1.9/`,
    '/blog/category/release-notes': `${base}/blog/tags/release-notes/`,
    '/blog/category/miscellaneous': `${base}/blog/tags/miscellaneous/`,
    '/blog/archive/2024': `${base}/blog/`,
    '/blog/archive/2025': `${base}/blog/`,
  },
  integrations: [
    starlight({
      title: 'rich-click',
      description: 'Richly rendered command line interfaces in click.',
      logo: {
        src: './src/content/docs/images/logo-square-large.png',
        alt: 'rich-click logo',
      },
      favicon: '/images/favicon.png',
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/ewels/rich-click' }],
      editLink: {
        baseUrl: 'https://github.com/ewels/rich-click/edit/main/docs/',
      },
      customCss: [
        '@fontsource/noto-sans/400.css',
        '@fontsource/noto-sans/400-italic.css',
        '@fontsource/noto-sans/700.css',
        '@fontsource/roboto-mono/400.css',
        '@fontsource/roboto-mono/700.css',
        './src/styles/custom.css',
        './src/styles/admonitions.css',
        './src/styles/tabs.css',
      ],
      components: {
        Header: './src/components/Header.astro',
      },
      head: [
        {
          tag: 'meta',
          attrs: { property: 'og:image', content: `${site}${base}/images/logo-square-large.png` },
        },
      ],
      sidebar: [
        { label: 'Home', link: '/' },
        { label: 'Live Style Editor', link: '/editor/' },
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
      ],
      plugins: [
        starlightBlog({
          // The header link is handled by the custom Header component tabs.
          navigation: 'none',
          authors: {
            ewels: {
              name: 'Phil Ewels',
              title: 'rich-click creator',
              picture: 'https://github.com/ewels.png',
              url: 'https://github.com/ewels',
            },
            dwreeves: {
              name: 'Daniel Reeves',
              title: 'Co-maintainer',
              picture: 'https://github.com/dwreeves.png',
              url: 'https://github.com/dwreeves',
            },
          },
        }),
        starlightLinksValidator({
          errorOnRelativeLinks: false,
        }),
      ],
    }),
  ],
});
