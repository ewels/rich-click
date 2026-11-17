/** URL slug of a tag or author name; tags also key their colour (`[data-tag]` in custom.css). */
export const slug = (label: string): string => label.toLowerCase().replace(/\W+/g, '-');

/** "Sep 16": the year is shown by the group heading. */
export const shortDate = (date: Date): string =>
  date.toLocaleDateString('en', { month: 'short', day: 'numeric', timeZone: 'UTC' });

export const isoDate = (date: Date): string => date.toISOString().slice(0, 10);

/** Anchor of a post in the blog index, linked from its table of contents. */
export const postAnchor = (entryId: string): string => entryId.split('/').at(-1)!;
