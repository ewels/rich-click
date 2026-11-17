// Shared by the Live Style Editor's build-time markup (editor-data.ts) and its
// client script, which shouldn't bundle the markup.

export interface StyleFlags {
  color: string | null;
  bold: boolean;
  dim: boolean;
  italic: boolean;
}

/** Render style flags as a rich style string, e.g. `bold dim cyan`. */
export const styleString = (style: StyleFlags): string =>
  [style.bold && 'bold', style.dim && 'dim', style.italic && 'italic', style.color]
    .filter(Boolean)
    .join(' ');
