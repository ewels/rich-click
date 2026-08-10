// Starlight route middleware: points every page's og:image / twitter:image at
// its generated social card (see pages/og/[...slug].ts). Pages without their
// own card (404, blog tag/author listings) fall back to the landing page card.
import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { base } from './base';
import { ogPages } from './og';

export const onRequest = defineRouteMiddleware((context) => {
  const { head, entry } = context.locals.starlightRoute;
  const id = entry?.id && entry.id in ogPages ? entry.id : 'index';
  const imageUrl = new URL(`${base}/og/${id}.png`, context.site).href;
  head.push(
    { tag: 'meta', attrs: { property: 'og:image', content: imageUrl } },
    { tag: 'meta', attrs: { name: 'twitter:image', content: imageUrl } },
    { tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } }
  );
});
