import { defineRouteMiddleware } from '@astrojs/starlight/route-data';
import { base, canonicalBase, sitePath } from './base';
import { postAnchor, slug } from './blog';
import { ogPages, plainTitle } from './og';
import { authorAvatars } from './avatars';
import notoSans400 from '@fontsource/noto-sans/files/noto-sans-latin-400-normal.woff2?url';
import notoSans700 from '@fontsource/noto-sans/files/noto-sans-latin-700-normal.woff2?url';
import firaCode400 from '@fontsource/fira-code/files/fira-code-latin-400-normal.woff2?url';
import firaCode700 from '@fontsource/fira-code/files/fira-code-latin-700-normal.woff2?url';
import pixelmix from './fonts/pixelmix.ttf?url';

// Preloaded so even cached fonts are ready for the first paint, and text (e.g.
// the header tabs, the blog sidebar) doesn't reflow when they swap in.
const preloadFonts = [
  [notoSans400, 'font/woff2'],
  [notoSans700, 'font/woff2'],
  [firaCode400, 'font/woff2'],
  [firaCode700, 'font/woff2'],
  [pixelmix, 'font/ttf'],
] as const;

export const onRequest = defineRouteMiddleware(async (context, next) => {
  const route = context.locals.starlightRoute;
  const { head, entry } = route;

  // starlight-blog's middleware (run by next()) swaps in the blog sidebar. The
  // blog index keeps the site sidebar: its tag filters do the blog sidebar's job.
  const siteSidebar = route.sidebar;
  await next();
  const path = sitePath(context.url);
  if (path.startsWith('/blog/') && path !== '/blog/') {
    // Marks the blog sidebar for its Rich-panel styles (custom.css). On its
    // first link, so the styles apply from the first paint, not once the page
    // body has loaded.
    const [allPosts] = route.sidebar;
    if (allPosts?.type === 'link') allPosts.attrs = { ...allPosts.attrs, class: 'rc-blog-sidebar' };
  }
  if (path === '/blog/') {
    route.sidebar = siteSidebar;
    // Overview, then a link to each post (heading ids in components/BlogPosts.astro).
    if (route.toc) {
      route.toc.items = [
        ...route.toc.items.slice(0, 1),
        ...context.locals.starlightBlog.posts.map((post) => ({
          depth: 2,
          slug: postAnchor(post.entry.id),
          text: post.title,
          children: [],
        })),
      ];
    }
  }

  // starlight-blog's author links are text only: add avatars (custom.css).
  const avatars = await authorAvatars();
  for (const group of route.sidebar) {
    if (group.type !== 'group') continue;
    for (const link of group.entries) {
      if (link.type !== 'link') continue;
      const name = [...avatars.keys()].find((n) => link.href.endsWith(`/blog/authors/${slug(n)}/`));
      if (name) link.attrs = { ...link.attrs, class: 'rc-sidebar-author', style: `--rc-avatar: url(${avatars.get(name)})` };
    }
  }

  // Splash pages have no sidebar, so no mobile menu button either, and the
  // header tabs only show from 72rem. Give them the sidebar, but hide it (with
  // Starlight's no-sidebar layout) once the tabs are there.
  if (entry?.data.template === 'splash') {
    route.hasSidebar = true;
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
