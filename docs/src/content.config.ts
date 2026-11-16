import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { docsLoader } from '@astrojs/starlight/loaders';
import { docsSchema } from '@astrojs/starlight/schema';
import { blogSchema } from 'starlight-blog/schema';

export const collections = {
  docs: defineCollection({
    loader: docsLoader(),
    schema: docsSchema({
      extend: (context) =>
        blogSchema(context).extend({
          // Blog posts: also show the `cover` image at the top of the post, not
          // just in the blog index (components/PostCover.astro).
          showCover: z.boolean().optional(),
        }),
    }),
  }),
};
