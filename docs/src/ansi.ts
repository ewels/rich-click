/**
 * Render rich-codex `.ansi` captures as HTML for the homepage terminal.
 *
 * Spans get a class per role (`c` cyan, `y` bold yellow, `yl` yellow, `g` green,
 * `r` red, `d` dim, `b` bold) instead of inline colours, so CSS can recolour the
 * same capture for each colour scheme. Only the SGR codes rich-click's default
 * theme emits are handled.
 */

interface Style {
  fg: number | null;
  bold: boolean;
  dim: boolean;
}

const SGR = /\x1b\[([0-9;]*)m/g;

function roleClass({ fg, bold, dim }: Style): string {
  // Bright variants (90-97) carry the same role as their base colour.
  const base = fg !== null && fg >= 90 ? fg - 60 : fg;
  if (base === 36) return 'c';
  if (base === 32) return 'g';
  if (base === 31) return 'r';
  if (base === 33 && bold) return 'y';
  if (dim) return 'd';
  if (base === 33) return 'yl';
  if (bold) return 'b';
  return '';
}

function applyCodes(style: Style, params: string): Style {
  const next = { ...style };
  for (const raw of (params || '0').split(';')) {
    const code = Number(raw || 0);
    if (code === 0) Object.assign(next, { fg: null, bold: false, dim: false });
    else if (code === 1) next.bold = true;
    else if (code === 2) next.dim = true;
    else if (code === 22) next.bold = next.dim = false;
    else if (code === 39) next.fg = null;
    else if ((code >= 30 && code <= 37) || (code >= 90 && code <= 97)) next.fg = code;
  }
  return next;
}

const escapeHtml = (text: string) =>
  text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');

/** One HTML string per line, with surrounding blank lines and trailing whitespace removed. */
export function ansiToHtmlLines(ansi: string): string[] {
  const lines = ansi.replace(/\r/g, '').split('\n');
  while (lines.length && !lines.at(-1)!.replace(SGR, '').trim()) lines.pop();
  while (lines.length && !lines[0].replace(SGR, '').trim()) lines.shift();

  return lines.map((line) => {
    let style: Style = { fg: null, bold: false, dim: false };
    const segments: [string, string][] = [];
    let pos = 0;
    for (const match of line.matchAll(SGR)) {
      if (match.index > pos) segments.push([line.slice(pos, match.index), roleClass(style)]);
      style = applyCodes(style, match[1]);
      pos = match.index + match[0].length;
    }
    if (pos < line.length) segments.push([line.slice(pos), roleClass(style)]);

    // Trailing padding only widens the scroll area.
    while (segments.length && !segments.at(-1)![0].trim()) segments.pop();
    if (segments.length) segments[segments.length - 1][0] = segments.at(-1)![0].trimEnd();

    return segments
      .map(([text, cls]) => (cls ? `<span class="${cls}">${escapeHtml(text)}</span>` : escapeHtml(text)))
      .join('');
  });
}
