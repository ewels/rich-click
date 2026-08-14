// Generates the docs pages that mirror repo-root Markdown files, replacing the
// mkdocs include-markdown plugin:
//
//   src/content/docs/index.md        <- landing page header + README.md tail
//   src/content/docs/changelog.md    <- CHANGELOG.md
//   src/content/docs/contributing.md <- CONTRIBUTING.md
//
// The generated files are gitignored and rebuilt on every `npm run dev` /
// `npm run build` (see the predev/prebuild scripts in package.json).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { SITE_TAGLINE, SITE_TITLE } from '../src/site.mjs';

const docsRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(docsRoot, '..');
const contentRoot = path.join(docsRoot, 'src/content/docs');

const GENERATED_NOTICE =
  '<!-- GENERATED FILE — built by docs/scripts/prepare-content.mjs; edit the source file instead. -->';

// GitHub alert type -> Starlight aside variant + title. The source files keep
// GitHub-flavoured syntax so they render on github.com; here they become
// native asides.
const GITHUB_ALERTS = {
  NOTE: ['note', 'Note'],
  TIP: ['tip', 'Tip'],
  IMPORTANT: ['tip', 'Important'],
  WARNING: ['caution', 'Warning'],
  CAUTION: ['danger', 'Caution'],
};

/** Rewrite `> [!NOTE]` blockquote alerts as Starlight `:::note[Title]` asides. */
function rewriteGithubAlerts(markdown) {
  const lines = markdown.split('\n');
  const out = [];
  for (let i = 0; i < lines.length; i++) {
    const match = /^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$/.exec(lines[i]);
    if (!match) {
      out.push(lines[i]);
      continue;
    }
    const [variant, title] = GITHUB_ALERTS[match[1]];
    const body = [];
    while (i + 1 < lines.length && lines[i + 1].startsWith('>')) {
      body.push(lines[++i].replace(/^>\s?/, ''));
    }
    out.push(`:::${variant}[${title}]`, ...body, ':::');
  }
  return out.join('\n');
}

function write(relPath, content) {
  const target = path.join(contentRoot, relPath);
  // Skip identical rewrites so mtimes (and Astro's content cache) stay stable.
  if (fs.existsSync(target) && fs.readFileSync(target, 'utf8') === content) return;
  fs.writeFileSync(target, content);
  console.log(`generated ${path.relative(repoRoot, target)}`);
}

// --- Landing page (README.md) ------------------------------------------------

const readme = fs.readFileSync(path.join(repoRoot, 'README.md'), 'utf8');
const marker = '<!--include-start-->';
const markerIndex = readme.indexOf(marker);
if (markerIndex === -1) throw new Error(`marker ${marker} not found in README.md`);
const readmeTail = readme
  .slice(markerIndex + marker.length)
  // Image paths in the README are relative to the repository root; the landing
  // page lives at the content root, next to the images directory.
  .replaceAll('docs/src/content/docs/images/', 'images/')
  .trim();

// The links validator doesn't cover images, so fail loudly here if a relative
// image referenced by the landing page doesn't exist (e.g. a README image path
// that the rewrite above didn't catch).
for (const [, src] of readmeTail.matchAll(/!\[[^\]]*\]\(([^)\s]+)\)/g)) {
  if (/^[a-z]+:/.test(src)) continue;
  const target = path.join(contentRoot, src);
  if (!fs.existsSync(target)) {
    throw new Error(`Landing page references missing image: ${src} (from README.md)`);
  }
}

write(
  'index.md',
  `---
title: ${SITE_TITLE}
description: ${SITE_TAGLINE}
template: splash
hero:
  tagline: ${SITE_TAGLINE}
  image:
    html: |
      <span class="rc-hero-logo">
        <img src="images/rich-click-logo.png" alt="rich-click" class="dark:sl-hidden" width="960" height="360">
        <img src="images/rich-click-logo-darkmode.png" alt="rich-click" class="light:sl-hidden" width="960" height="360">
      </span>
editUrl: false
tableOfContents: false
---

${GENERATED_NOTICE}

<p align="center">
    <img src="https://img.shields.io/pypi/v/rich-click?logo=pypi" alt="PyPI"/>
    <img src="https://github.com/ewels/rich-click/workflows/Test%20Coverage/badge.svg" alt="Test Coverage badge">
    <img src="https://github.com/ewels/rich-click/workflows/Lint%20code/badge.svg" alt="Lint code badge">
</p>

<p align="center">
    <a href="documentation/introduction_to_click/">Documentation</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="https://github.com/ewels/rich-click">Source Code</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="changelog/">Changelog</a>
</p>

---

${readmeTail}
`
);

// --- Changelog / Contributing ------------------------------------------------

function rootPage(sourceFile, title, description, outFile) {
  let content = fs.readFileSync(path.join(repoRoot, sourceFile), 'utf8');
  // Drop the first level-1 heading: the page title comes from the frontmatter.
  content = content.replace(/^# .+\n/, '').trim();
  content = rewriteGithubAlerts(content);
  write(
    outFile,
    `---
title: ${title}
description: ${description}
editUrl: https://github.com/ewels/rich-click/edit/main/${sourceFile}
---

${GENERATED_NOTICE}

${content}
`
  );
}

rootPage(
  'CHANGELOG.md',
  'Changelog',
  'Release notes for every rich-click version, newest first.',
  'changelog.md'
);
rootPage(
  'CONTRIBUTING.md',
  'Contributing',
  'How to set up a rich-click development environment, run the tests and open a pull request.',
  'contributing.md'
);
