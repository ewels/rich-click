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
    // The full logotype, not the square icon. Sized and centred by
    // scripts/prepare-content.mjs, which pads it out to the width between the
    // card paddings below — so no `size` here, or that padding gets rescaled.
    logo: {
      path: './src/generated/og-logo.png',
    },
    bgGradient: [
      [0, 0, 0],
      [30, 32, 41],
    ],
    border: { color: [64, 81, 181], width: 16, side: 'block-end' },
    // Kept in sync with CARD_PADDING in scripts/prepare-content.mjs, which pads
    // the logo out to the width this leaves.
    padding: 36,
    font: {
      title: {
        families: ['Kode Mono'],
        weight: 'Bold',
        color: [255, 255, 255],
        size: 60,
        lineHeight: 1.25,
      },
      description: {
        families: ['Kode Mono'],
        color: [196, 200, 214],
        size: 30,
        lineHeight: 1.5,
      },
    },
    fonts: [
      './node_modules/@fontsource/kode-mono/files/kode-mono-latin-400-normal.woff',
      './node_modules/@fontsource/kode-mono/files/kode-mono-latin-700-normal.woff',
    ],
  }),
});
