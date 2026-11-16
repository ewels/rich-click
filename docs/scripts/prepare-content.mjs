// Generates the docs pages that mirror repo-root Markdown files, replacing the
// mkdocs include-markdown plugin:
//
//   src/content/docs/changelog.md    <- CHANGELOG.md
//   src/content/docs/contributing.md <- CONTRIBUTING.md
//
// ...and the trimmed logotype the social cards are drawn with:
//
//   src/generated/og-logo.png        <- public/images/rich-click-dark.svg
//
// ...and the theme counts the homepage quotes:
//
//   src/generated/theme-counts.json  <- src/rich_click/rich_click_theme.py
//
// The generated files are gitignored and rebuilt on every `npm run dev` /
// `npm run build` (see the predev/prebuild scripts in package.json).
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';

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

// --- Theme counts --------------------------------------------------------------

// Python counts them because COLORS builds some schemes in a loop. The theme
// module only imports the standard library, so it loads without dependencies.
const themeCountsScript = `
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("theme", sys.argv[1])
theme = importlib.util.module_from_spec(spec)
spec.loader.exec_module(theme)
print(json.dumps({"colours": len(theme.COLORS), "formats": len(theme.FORMATS)}))
`;
const themeCounts = execFileSync(
  'uv',
  ['run', '--no-project', '--quiet', 'python', '-c', themeCountsScript, path.join(repoRoot, 'src/rich_click/rich_click_theme.py')],
  { encoding: 'utf8' }
);
const themeCountsOut = path.join(docsRoot, 'src/generated/theme-counts.json');
fs.mkdirSync(path.dirname(themeCountsOut), { recursive: true });
fs.writeFileSync(themeCountsOut, themeCounts);
console.log(`generated ${path.relative(repoRoot, themeCountsOut)}`);

// --- Social card logotype -----------------------------------------------------

// astro-og-canvas draws the logo from the left padding edge at whatever size it
// is given: it has no alignment option, and the shipped logotype sits on a
// 960x360 canvas with the artwork occupying only 656x147 of it. So both the
// size and the centring are baked in here — trim the transparent margin, scale
// the wordmark to 60% of the card, and re-pad it symmetrically to the full
// width between the card's paddings. The card route then draws the file at its
// own dimensions and needs no numbers of its own (see src/pages/og/[...slug].ts).
const CARD_WIDTH = 1200;
const CARD_PADDING = 36;
const WORDMARK_SHARE = 0.6;
const TRANSPARENT = { r: 0, g: 0, b: 0, alpha: 0 };

const contentWidth = CARD_WIDTH - CARD_PADDING * 2;
const wordmarkWidth = Math.round(CARD_WIDTH * WORDMARK_SHARE);
const ogLogoSource = path.join(docsRoot, 'public/images/rich-click-dark.svg');
const ogLogoOut = path.join(docsRoot, 'src/generated/og-logo.png');
fs.mkdirSync(path.dirname(ogLogoOut), { recursive: true });
// Unconditional: the output depends on the constants above as well as on the
// source file, and it costs tens of milliseconds. astro-og-canvas keys its own
// cache on the logo's contents, so an unchanged result still costs nothing.
// Rasterised well above the target size so the downscale stays sharp.
const wordmark = await sharp(ogLogoSource, { density: 72 * 4 })
  .trim({ threshold: 0 })
  .resize({ width: wordmarkWidth })
  .toBuffer();
const sideMargin = Math.round((contentWidth - wordmarkWidth) / 2);
await sharp(wordmark)
  .extend({
    left: sideMargin,
    right: contentWidth - wordmarkWidth - sideMargin,
    background: TRANSPARENT,
  })
  .toFile(ogLogoOut);
console.log(`generated ${path.relative(repoRoot, ogLogoOut)}`);
