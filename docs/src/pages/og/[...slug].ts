// Build-time social card images (1200x630) for every page, replacing the
// mkdocs-material "social" plugin. Cards use the same Kode Mono font the old
// cards were configured with, on the site's black/indigo palette.
import { OGImageRoute } from 'astro-og-canvas';
import { ogPages } from '../../og';

export const { getStaticPaths, GET } = await OGImageRoute({
  pages: ogPages,
  // The default slug helper treats the end of entry ids like `blog/version-1.9`
  // as a file extension and would strip it; ids are already extension-free.
  getSlug: (path) => `${path}.png`,
  getImageOptions: (_path, page) => ({
    title: page.title,
    description: page.description,
    // The full logotype, not the square icon: 960 of the card's 1200px width.
    // Trimmed of its transparent margin by scripts/prepare-content.mjs, or 80%
    // of the width would be mostly empty canvas.
    logo: {
      path: './src/generated/og-logo.png',
      size: [960],
    },
    bgGradient: [
      [0, 0, 0],
      [30, 32, 41],
    ],
    border: { color: [64, 81, 181], width: 16, side: 'block-end' },
    // The logotype takes the top third of the card, so the type below it is
    // sized to leave room for the worst case in the docs: a title that wraps to
    // two lines above a three-line description.
    padding: 48,
    font: {
      title: {
        families: ['Kode Mono'],
        weight: 'Bold',
        color: [255, 255, 255],
        size: 52,
        lineHeight: 1.2,
      },
      description: {
        families: ['Kode Mono'],
        color: [196, 200, 214],
        size: 26,
        lineHeight: 1.4,
      },
    },
    fonts: [
      './node_modules/@fontsource/kode-mono/files/kode-mono-latin-400-normal.woff',
      './node_modules/@fontsource/kode-mono/files/kode-mono-latin-700-normal.woff',
    ],
  }),
});
