// Renders `:::variant` container directives as Material for MkDocs style
// admonitions, using the same markup shape as Starlight's built-in asides.
//
// This handles the full set of admonition variants used by the docs (including
// ones Starlight has no aside for, like `info`, `success`, `failure` and
// `example`) plus collapsible admonitions:
//
//     :::info[Optional title]         !!! info "Optional title"   (mkdocs)
//     content
//     :::
//
//     :::details[Title]{variant=info open}   ??? / ???+ info "Title"  (mkdocs)
//     content
//     :::
//
// Runs before Starlight's own asides plugin; since every directive it claims is
// replaced outright, the two never overlap.
import { buildAside, DEFAULT_TITLES, VARIANTS } from './admonition-common.mjs';

export function satteriAdmonitions() {
  return {
    name: 'rich-click-admonitions',
    containerDirective(node, ctx) {
      const isDetails = node.name === 'details';
      if (!isDetails && !VARIANTS.includes(node.name)) return;

      const variant = isDetails
        ? String(node.attributes?.variant ?? 'note')
        : node.name;
      const open = isDetails && node.attributes?.open !== undefined;

      let title = DEFAULT_TITLES[variant] ?? DEFAULT_TITLES.note;
      let titleNodes = [{ type: 'text', value: title }];
      const children = [...(node.children ?? [])];
      const firstChild = children[0];
      if (
        firstChild?.type === 'paragraph' &&
        firstChild.data?.directiveLabel &&
        firstChild.children.length > 0
      ) {
        titleNodes = firstChild.children;
        title = ctx.textContent(firstChild);
        children.shift();
      }

      return buildAside(variant, titleNodes, title, children, isDetails ? { open } : null);
    },
  };
}
