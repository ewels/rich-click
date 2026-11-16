// @ts-check
import { execFileSync } from 'node:child_process';
import { readdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { satteri } from '@astrojs/markdown-satteri';
import starlightBlog from 'starlight-blog';
import codeblocks, { linksValidatorExclude } from 'starlight-codeblocks';
import { python } from 'starlight-codeblocks/adapters/python';
import starlightLinksValidator from 'starlight-links-validator';
import starlightLlmsTxt from 'starlight-llms-txt';
import starlightPageActions from 'starlight-page-actions';
import starlightPydocs, { pydocsSidebarGroup } from 'starlight-pydocs';

import { satteriMermaid } from './plugins/satteri-mermaid.mjs';
import { API_PATH, DEFAULT_BASE, REPO, REPO_URL, sidebar, SITE_TAGLINE, SITE_TITLE } from './src/site.mjs';

// Each docs version is deployed to its own directory (e.g. /rich-click/1.9/,
// /rich-click/latest/): docs/_deploy.py builds once per directory, setting the base.
const site = 'https://ewels.github.io';
const base = process.env.ASTRO_BASE ?? DEFAULT_BASE;

// Every 1.x release tag, oldest first, patches included: starlight-pydocs badges
// each API object with the release it first appeared in. The oldest tag is the
// baseline and gets no badge; a clone without tags yields no badges at all.
const releaseTags = execFileSync('git', ['tag', '--list', 'v1.*', '--sort=v:refname'], {
  cwd: fileURLToPath(new URL('..', import.meta.url)),
  encoding: 'utf8',
})
  .split('\n')
  // Releases only: excludes the `v1.9.0.dev0` style prerelease tags.
  .filter((tag) => /^v\d+\.\d+(\.\d+)?$/.test(tag))
  .map((tag) => ({ ref: tag, label: tag.slice(1) }));

// Sphinx inventories of rich-click's dependencies and the other libraries the
// docs import, used to link names both in the API reference and in code blocks.
// asyncclick and colorama publish no inventory.
const inventories = [
  { url: 'https://click.palletsprojects.com/en/stable/objects.inv' },
  { url: 'https://rich.readthedocs.io/en/stable/objects.inv' },
  { url: 'https://typer.tiangolo.com/objects.inv' },
  { url: 'https://typing-extensions.readthedocs.io/en/stable/objects.inv' },
  { url: 'https://anyio.readthedocs.io/en/stable/objects.inv' },
  { url: 'https://maxludden.github.io/rich-gradient/objects.inv' },
];

// starlight-page-actions publishes each page's source verbatim as `.md`. Strip
// the `{/* RICH-CODEX ... */}` image-generation blocks from those copies, where
// they are noise to whoever reads the Markdown, but not from code examples.
// Closing fences may be followed by text: tidymd renders inline `<Code>` that way.
const FENCE_OR_MDX_COMMENT = /^ {0,3}(`{3,}|~{3,})[^\n]*\n[\s\S]*?^ {0,3}\1|\{\/\*[\s\S]*?\*\/\}\n?/gm;
/** @param {string} markdown */
const stripMdxComments = (markdown) =>
  markdown.replace(FENCE_OR_MDX_COMMENT, (match, fence) => (fence ? match : ''));

/** @type {import('astro').AstroIntegration} */
const stripMarkdownCopyComments = {
  name: 'rich-click:strip-mdx-comments',
  hooks: {
    'astro:build:done': async ({ dir }) => {
      const entries = await readdir(fileURLToPath(dir), { recursive: true });
      for (const entry of entries.filter((name) => name.endsWith('.md'))) {
        const path = fileURLToPath(new URL(entry, dir));
        const original = await readFile(path, 'utf8');
        const stripped = stripMdxComments(original);
        if (stripped !== original) await writeFile(path, stripped);
      }
    },
  },
};

// Starlight's default PageTitle shows `backticks` in titles literally. It can't
// be overridden through `components` without losing starlight-page-actions' own
// PageTitle override, which imports the default by path, so swap that path.
/** @type {import('vite').Plugin} */
const pageTitleWithCode = {
  name: 'rich-click:page-title-with-code',
  enforce: 'pre',
  resolveId(source) {
    if (source === '@astrojs/starlight/components/PageTitle.astro') {
      return fileURLToPath(new URL('./src/components/PageTitle.astro', import.meta.url));
    }
  },
};

export default defineConfig({
  site,
  base,
  vite: {
    plugins: [pageTitleWithCode],
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
      mdastPlugins: [satteriMermaid()],
    }),
  },
  redirects: {
    '/documentation/groups_and_sorting': `${base}/documentation/panels/overview/`,
    '/documentation/formatting_and_styles': `${base}/documentation/text_markup_and_formatting/`,
    // Old date-based blog URLs.
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
    stripMarkdownCopyComments,
    starlight({
      title: SITE_TITLE,
      description: SITE_TAGLINE,
      logo: {
        src: './src/content/docs/images/logo-square-large.svg',
        alt: 'rich-click logo',
      },
      favicon: '/images/favicon.svg',
      expressiveCode: {
        styleOverrides: {
          // Roboto Mono has no box-drawing characters, which Rich draws its panels with,
          // and the tighter line height joins their vertical lines.
          codeblocksRunnable: { outputFontFamily: "'Fira Code', monospace", outputLineHeight: '1.25' },
        },
      },
      // Replaced by src/pages/404.astro, which isn't a content entry so it stays
      // out of llms.txt and the [...slug] route.
      disable404Route: true,
      social: [{ icon: 'github', label: 'GitHub', href: REPO_URL }],
      editLink: {
        baseUrl: `${REPO_URL}/edit/main/docs/`,
      },
      customCss: [
        '@fontsource/noto-sans/400.css',
        '@fontsource/noto-sans/400-italic.css',
        '@fontsource/noto-sans/700.css',
        '@fontsource/roboto-mono/400.css',
        '@fontsource/roboto-mono/700.css',
        '@fontsource/fira-code/400.css',
        '@fontsource/fira-code/700.css',
        './src/styles/custom.css',
      ],
      components: {
        Header: './src/components/Header.astro',
        Hero: './src/components/Hero.astro',
        SocialIcons: './src/components/SocialIcons.astro',
        Footer: './src/components/Footer.astro',
      },
      // Adds the auto-generated social card meta tags (see src/pages/og/).
      routeMiddleware: './src/starlight-route-data.ts',
      // site.mjs is also loaded by plain `node`, so can't import starlight-pydocs:
      // swap its API Reference link for the plugin's generated module tree.
      sidebar: sidebar.map((entry) =>
        entry.link === API_PATH
          ? { label: entry.label, collapsed: true, items: [pydocsSidebarGroup] }
          : entry
      ),
      plugins: [
        // Must come before any plugin that sets Starlight's `expressiveCode` option.
        codeblocks({
          // Replaces the default adapters, dropping the Nextflow one.
          apiLinks: { adapters: [python({ inventories })] },
        }),
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
          exclude: linksValidatorExclude,
        }),
        // Site-level Markdown indexes for language models: llms.txt (index),
        // llms-full.txt (everything) and llms-small.txt (asides stripped).
        starlightLlmsTxt({
          projectName: SITE_TITLE,
          description:
            'rich-click is a shim around the Python Click library that formats command line ' +
            'help text and error messages with Rich: colours, boxed option panels, Markdown ' +
            'and Rich markup in docstrings, and configurable styles.',
          // Orientation first, long changelog last.
          promote: ['index*', 'documentation/introduction_to_click*'],
          demote: ['changelog*', 'blog/**'],
          // Prose-only readers don't need the blog archive or the contributor guide.
          exclude: ['blog/**', 'contributing'],
          customSets: [
            {
              label: 'Documentation',
              description: 'the prose guides: configuration, panels, styles, markup, CLI, Typer',
              paths: ['documentation/**'],
            },
            {
              label: 'Blog',
              description: 'release announcements and articles',
              paths: ['blog/**'],
            },
          ],
          // Starlight puts a "Section titled …" anchor link inside every
          // heading, which converts to a duplicate link line under each one;
          // .scb-deco is starlight-codeblocks' labels, buttons and notes.
          customSelectors: { all: ['.sl-anchor-link', '.scb-deco'] },
          // The API reference is generated by starlight-pydocs as injected
          // routes, which this plugin cannot see (it walks the `docs` content
          // collection). Point at the Markdown the plugin publishes itself.
          optionalLinks: [
            {
              label: 'rich_click API reference (Markdown)',
              url: `${site}${base}${API_PATH}llms.txt`,
              description: 'Every documented module, class and function in rich_click.',
            },
          ],
        }),
        // "Copy Markdown" / "Open in…" buttons, and the raw `.md` route behind
        // them. `baseUrl` is deliberately unset: with it the plugin writes its
        // own llms.txt, which would collide with starlight-llms-txt above.
        starlightPageActions({
          prompt:
            'Read {url}, part of the documentation for rich-click, a Python library that ' +
            'renders Click command line help text with Rich. I want to ask questions about it.',
          actions: { claude: true, chatgpt: true, cursor: true, markdown: true },
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
                repo: REPO,
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
          inventories: ['python', ...inventories],
        }),
      ],
    }),
  ],
});
