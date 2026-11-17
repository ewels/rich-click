// Generates the gitignored files the site builds from, out of sources elsewhere
// in the repo. Run before every `npm run dev` / `npm run build`.
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import sharp from 'sharp';
import { OG_CARD, REPO_URL } from '../src/site.mjs';

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

function write(target, content) {
  // Skip identical rewrites so mtimes (and Astro's content cache) stay stable.
  try {
    if (fs.readFileSync(target).equals(Buffer.from(content))) return;
  } catch {
    fs.mkdirSync(path.dirname(target), { recursive: true });
  }
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
    path.join(contentRoot, outFile),
    `---
title: ${title}
description: ${description}
editUrl: ${REPO_URL}/edit/main/${sourceFile}
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
write(path.join(docsRoot, 'src/generated/theme-counts.json'), themeCounts);

// --- Social card logotype -----------------------------------------------------

// astro-og-canvas can't align the logo: it draws it from the left padding edge,
// at its own size. So trim the logotype's transparent margin, scale it to 60%
// of the card width and pad it back out, centred, to the width between the
// card's paddings. Rasterised well above that size so the downscale stays sharp.
const WORDMARK_SHARE = 0.6;
const TRANSPARENT = { r: 0, g: 0, b: 0, alpha: 0 };

const contentWidth = OG_CARD.width - OG_CARD.padding * 2;
const wordmarkWidth = Math.round(OG_CARD.width * WORDMARK_SHARE);
const ogLogoSource = path.join(docsRoot, 'public/images/rich-click-dark.svg');
const wordmark = await sharp(ogLogoSource, { density: 72 * 4 })
  .trim({ threshold: 0 })
  .resize({ width: wordmarkWidth })
  .toBuffer();
const sideMargin = Math.round((contentWidth - wordmarkWidth) / 2);
const ogLogo = await sharp(wordmark)
  .extend({
    left: sideMargin,
    right: contentWidth - wordmarkWidth - sideMargin,
    background: TRANSPARENT,
  })
  .png()
  .toBuffer();
write(path.join(docsRoot, OG_CARD.logo), ogLogo);
