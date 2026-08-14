// @ts-check
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { satteri } from '@astrojs/markdown-satteri';
import starlightBlog from 'starlight-blog';
import starlightLinksValidator from 'starlight-links-validator';
import starlightPydocs, { pydocsSidebarGroup } from 'starlight-pydocs';

import { satteriInlineCode } from './plugins/satteri-inline-code.mjs';
import { satteriMermaid } from './plugins/satteri-mermaid.mjs';
import { API_PATH, sidebar, SITE_TAGLINE, SITE_TITLE } from './src/site.mjs';

// The site is deployed to versioned directories on GitHub Pages, mirroring the
// layout previously managed by `mike` (e.g. /rich-click/latest/, /rich-click/1.9/).
// docs/_deploy.py builds once per deployed alias, overriding the base path; the
// default here must stay in sync with BASE_PREFIX/DEFAULT_ALIAS in that script.
const site = 'https://ewels.github.io';
const base = process.env.ASTRO_BASE ?? '/rich-click/latest';

// Every 1.x release tag, oldest first: starlight-pydocs extracts each one and
// badges each API object with the release it first appeared in. Features land in
// patch releases, so patches are listed too — one extraction costs ~0.3s, cached
// per commit afterwards. The oldest tag is the baseline and gets no badge.
// Read from git rather than listed by hand so new releases need no edit here; a
// clone without tags yields no badges (see fetch-depth in build-docs.yml).
const releaseTags = execFileSync('git', ['tag', '--list', 'v1.*', '--sort=v:refname'], {
  cwd: fileURLToPath(new URL('..', import.meta.url)),
  encoding: 'utf8',
})
  .split('\n')
  // Releases only: excludes the `v1.9.0.dev0` style prerelease tags.
  .filter((tag) => /^v\d+\.\d+(\.\d+)?$/.test(tag))
  .map((tag) => ({ ref: tag, label: tag.slice(1) }));

export default defineConfig({
  site,
  base,
  vite: {
    resolve: {
      // Only matters when starlight-pydocs is symlinked in from a local
      // checkout: without this its own copies of these get loaded too.
      dedupe: ['astro', '@astrojs/starlight'],
      alias: {
        // Runnable example snippets, imported into MDX pages via `?raw`.
        '@code_snippets': fileURLToPath(new URL('./code_snippets', import.meta.url)),
        // The rich-click Python source, for docs that quote from it.
        '@rich_click': fileURLToPath(new URL('../src/rich_click', import.meta.url)),
      },
    },
  },
  markdown: {
    processor: satteri({
      mdastPlugins: [satteriInlineCode(), satteriMermaid()],
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
      ],
      components: {
        Header: './src/components/Header.astro',
      },
      // Adds the auto-generated social card meta tags (see src/pages/og/).
      routeMiddleware: './src/starlight-route-data.ts',
      // site.mjs can't import starlight-pydocs (it is also loaded by plain
      // `node` scripts, which can't strip types), so the API Reference entry is
      // a plain link there — for the header tab — and becomes the placeholder
      // group here, which the plugin fills with the generated module tree.
      sidebar: sidebar.map((entry) =>
        entry.link === API_PATH
          ? { label: entry.label, collapsed: true, items: [pydocsSidebarGroup] }
          : entry
      ),
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
        // API reference, generated from the rich_click source with griffe.
        starlightPydocs({
          packages: [
            {
              name: 'rich_click',
              search: ['../src'],
              sidebar: { collapsed: true },
              ...(releaseTags.length > 0 && { versions: { refs: releaseTags } }),
              sourceLink: {
                host: 'github',
                repo: 'ewels/rich-click',
                // Docs are built from the checkout being released, so pin the
                // links to that commit rather than a moving branch.
                ref: process.env.GITHUB_SHA ?? 'main',
                root: '..',
              },
            },
          ],
          // Outside node_modules so `npm ci` cannot delete it, and so CI can
          // cache the per-release griffe dumps (see build-docs.yml).
          cacheDir: '.cache',
          // Link type annotations out to the libraries rich-click builds on.
          inventories: [
            'python',
            { url: 'https://click.palletsprojects.com/en/stable/objects.inv' },
            { url: 'https://rich.readthedocs.io/en/stable/objects.inv' },
            { url: 'https://typer.tiangolo.com/objects.inv' },
          ],
        }),
      ],
    }),
  ],
});
