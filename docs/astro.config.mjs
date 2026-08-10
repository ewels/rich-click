// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { satteri } from '@astrojs/markdown-satteri';
import starlightBlog from 'starlight-blog';
import starlightLinksValidator from 'starlight-links-validator';

import { features, mdastPlugins } from './plugins/pipeline.mjs';
import { sidebar, SITE_TAGLINE, SITE_TITLE } from './src/site.mjs';

// The site is deployed to versioned directories on GitHub Pages, mirroring the
// layout previously managed by `mike` (e.g. /rich-click/latest/, /rich-click/1.9/).
// docs/_deploy.py builds once per deployed alias, overriding the base path; the
// default here must stay in sync with BASE_PREFIX/DEFAULT_ALIAS in that script.
const site = 'https://ewels.github.io';
const base = process.env.ASTRO_BASE ?? '/rich-click/latest';

export default defineConfig({
  site,
  base,
  markdown: {
    processor: satteri({ features, mdastPlugins }),
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
      title: SITE_TITLE,
      description: SITE_TAGLINE,
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
      // Adds the auto-generated social card meta tags (see src/pages/og/).
      routeMiddleware: './src/starlight-route-data.ts',
      sidebar,
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
