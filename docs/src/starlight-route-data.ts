// Starlight route middleware:
// - points every page's og:image / twitter:image at its generated social card
//   (see pages/og/[...slug].ts); pages without their own card (404, blog
//   tag/author listings) fall back to the landing page card;
// - advertises each page's raw Markdown with `<link rel="alternate">`, so an
//   agent on any page finds the source without guessing the URL scheme;
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

  // `<page>.md` is the convention starlight-page-actions serves and its "View
  // as Markdown" button fetches; nothing emits the head tag that tells a
  // crawler it exists. Only for real content files: the API reference pages
  // advertise their own (starlight-pydocs does emit it), and the injected blog
  // listing pages have no Markdown to point at.
  const pathname = context.url.pathname.replace(/\/$/, '');
  if (/\.mdx?$/.test(entry?.filePath ?? '')) {
    // The landing page is copied out as `index.md`, not `<base>.md`.
    const href = pathname === base ? `${base}/index.md` : `${pathname}.md`;
    head.push({ tag: 'link', attrs: { rel: 'alternate', type: 'text/markdown', href } });
  }

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
