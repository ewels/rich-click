// Turns ```mermaid fenced code blocks into `<pre class="mermaid">` elements
// that are rendered client-side by the script in src/components/Header.astro.
// Running as an mdast plugin means the block never reaches the syntax
// highlighter, mirroring how mkdocs-material handled mermaid superfences.
import { element } from './admonition-common.mjs';

export function satteriMermaid() {
  return {
    name: 'rich-click-mermaid',
    code(node) {
      if (node.lang !== 'mermaid') return;
      return element('pre', { class: 'mermaid' }, [{ type: 'text', value: node.value }]);
    },
  };
}
