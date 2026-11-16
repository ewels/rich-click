import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { base, canonicalBase } from './base';
import { ogPages, plainTitle } from './og';
import notoSans400 from '@fontsource/noto-sans/files/noto-sans-latin-400-normal.woff2?url';
import notoSans700 from '@fontsource/noto-sans/files/noto-sans-latin-700-normal.woff2?url';
import pixelmix from './fonts/pixelmix.ttf?url';

// Preloaded so even cached fonts are ready for the first paint, and text (e.g.
// the header tabs) doesn't reflow when they swap in.
const preloadFonts = [
  [notoSans400, 'font/woff2'],
  [notoSans700, 'font/woff2'],
  [pixelmix, 'font/ttf'],
] as const;

export const onRequest = defineRouteMiddleware((context) => {
  const { head, entry } = context.locals.starlightRoute;
  // Splash pages have no sidebar, so no mobile menu button either, and the
  // header tabs only show from 72rem. Give them the sidebar, but hide it (with
  // Starlight's no-sidebar layout) once the tabs are there.
  if (entry?.data.template === 'splash') {
    context.locals.starlightRoute.hasSidebar = true;
    head.push({
      tag: 'style',
      content:
        ':root[data-has-sidebar]{--sl-content-width:67.5rem}' +
        '@media (min-width:72rem){:root[data-has-sidebar]{--sl-content-inline-start:0}.sidebar-pane{display:none}}',
    });
  }

  for (const [href, type] of preloadFonts) {
    head.push({ tag: 'link', attrs: { rel: 'preload', as: 'font', type, href, crossorigin: '' } });
  }

  // Pages without their own social card (404, blog tag/author listings) use the homepage's.
  const id = entry?.id && entry.id in ogPages ? entry.id : 'index';
  const imageUrl = new URL(`${base}/og/${id}.png`, context.site).href;
  head.push(
    { tag: 'meta', attrs: { property: 'og:image', content: imageUrl } },
    { tag: 'meta', attrs: { name: 'twitter:image', content: imageUrl } }
  );

  // Nothing else advertises the `.md` copy that starlight-page-actions serves
  // (Footer.astro links to it from here). Custom StarlightPage pages get a
  // made-up `.md` filePath but an empty body; starlight-pydocs pages already
  // carry their own link.
  if (entry?.body && /\.mdx?$/.test(entry.filePath ?? '')) {
    const href = `${context.url.pathname.replace(/\/$/, '')}.md`;
    head.push({ tag: 'link', attrs: { rel: 'alternate', type: 'text/markdown', href } });
  }

  for (const tag of head) {
    // Titles may use `backticks` for inline code (see components/PageTitle.astro).
    if (tag.tag === 'title' && tag.content) tag.content = plainTitle(tag.content);
    const attrs = tag.attrs ?? {};
    if (tag.tag === 'meta' && attrs.property === 'og:title' && typeof attrs.content === 'string') {
      attrs.content = plainTitle(attrs.content);
    }

    // Versioned deploys (e.g. /rich-click/1.9/) point search engines at `latest`.
    const urlKey =
      (tag.tag === 'link' && attrs.rel === 'canonical' && 'href') ||
      (tag.tag === 'meta' && attrs.property === 'og:url' && 'content');
    const url = urlKey && attrs[urlKey];
    if (urlKey && typeof url === 'string' && canonicalBase !== base) {
      attrs[urlKey] = url.replace(`${base}/`, `${canonicalBase}/`);
    }
  }
});
