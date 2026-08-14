// Turns ```mermaid fenced code blocks into `<pre class="mermaid">` elements
// that are rendered client-side by the script in src/components/Header.astro.
// Running as an mdast plugin means the block never reaches the syntax
// highlighter, mirroring how mkdocs-material handled mermaid superfences.
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
