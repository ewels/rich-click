import { getImage } from 'astro:assets';
import type { ImageMetadata } from 'astro';
import { BLOG_AUTHORS } from './site.mjs';

// Self-hosted, as github.com/<user>.png is an uncached redirect to an image
// cached for only 5 minutes. Named by BLOG_AUTHORS key.
const images = import.meta.glob<{ default: ImageMetadata }>('./assets/authors/*.jpg', { eager: true });

let avatars: Promise<Map<string, string>> | undefined;

/** Blog author avatar URLs by author name, sized for display at up to 36px. */
export const authorAvatars = (): Promise<Map<string, string>> =>
  (avatars ??= Promise.all(
    Object.entries(BLOG_AUTHORS).map(async ([key, author]) => {
      const image = images[`./assets/authors/${key}.jpg`]!.default;
      const { src } = await getImage({ src: image, width: 72, height: 72 });
      return [author.name, src] as const;
    })
  ).then((entries) => new Map(entries)));
