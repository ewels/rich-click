// Turns ```mermaid fenced code blocks into `<pre class="mermaid">` elements,
// rendered client-side by the script in src/components/Header.astro. As an
// mdast plugin it runs before the blocks reach the syntax highlighter.
export function satteriMermaid() {
  return {
    name: 'rich-click-mermaid',
    code(node) {
      if (node.lang !== 'mermaid') return;
      return {
        type: 'paragraph',
        data: { hName: 'pre', hProperties: { class: 'mermaid' } },
        children: [{ type: 'text', value: node.value }],
      };
    },
  };
}
