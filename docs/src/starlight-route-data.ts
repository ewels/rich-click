// Starlight route middleware:
// - points every page's og:image / twitter:image at its generated social card
//   (see pages/og/[...slug].ts); pages without their own card (404, blog
//   tag/author listings) fall back to the landing page card;
// - rewrites canonical URLs to the `latest` alias, matching mike's
//   `canonical_version: latest` on the old site, so versioned deploys
//   (e.g. /rich-click/1.9/) don't compete with /rich-click/latest/ in search.
import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { base } from './base';
import { ogPages } from './og';

const canonicalBase = base.replace(/\/[^/]+$/, '/latest');

export const onRequest = defineRouteMiddleware((context) => {
  const { head, entry } = context.locals.starlightRoute;
  const id = entry?.id && entry.id in ogPages ? entry.id : 'index';
  const imageUrl = new URL(`${base}/og/${id}.png`, context.site).href;
  head.push(
    { tag: 'meta', attrs: { property: 'og:image', content: imageUrl } },
    { tag: 'meta', attrs: { name: 'twitter:image', content: imageUrl } },
    { tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } }
  );

  if (canonicalBase !== base) {
    for (const tag of head) {
      const isCanonical = tag.tag === 'link' && tag.attrs?.rel === 'canonical';
      const isOgUrl = tag.tag === 'meta' && tag.attrs?.property === 'og:url';
      const key = isCanonical ? 'href' : isOgUrl ? 'content' : undefined;
      if (!key) continue;
      const value = tag.attrs?.[key];
      if (typeof value === 'string') {
        tag.attrs![key] = value.replace(`${base}/`, `${canonicalBase}/`);
      }
    }
  }
});
