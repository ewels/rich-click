// Renders runs of consecutive `:::tab[Label]` container directives as Material
// for MkDocs style content tabs (the `pymdownx.tabbed` "alternate style"
// markup), so the existing tab styling and behaviour carry over:
//
//     :::tab[pip]
//     ```shell
//     pip install rich-click
//     ```
//     :::
//     :::tab[uv]
//     ...
//     :::
//
// The generated markup is a radio-input based tab set (styled by
// src/styles/tabs.css); a small script in the Header component links tabs with
// identical labels together, mirroring Material's `content.tabs.link` feature.
import { element } from './admonition-common.mjs';

export function satteriTabs() {
  // Factory form: state resets for each document.
  let tabSetCount = 0;

  const isTab = (node) => node?.type === 'containerDirective' && node.name === 'tab';

  return {
    name: 'rich-click-tabs',
    containerDirective(node, ctx) {
      if (!isTab(node)) return;
      const parent = ctx.parent(node);
      if (!parent || !parent.children) return;
      const index = ctx.indexOf(node);
      if (index === undefined) return;

      // Only handle the first tab of a run; the rest are folded into the set.
      if (index > 0 && isTab(parent.children[index - 1])) return;

      const run = [];
      for (let i = index; i < parent.children.length; i++) {
        const sibling = parent.children[i];
        if (!isTab(sibling)) break;
        run.push(sibling);
      }

      tabSetCount += 1;
      const setId = tabSetCount;
      const inputs = [];
      const labels = [];
      const blocks = [];
      run.forEach((tab, i) => {
        const inputProperties = {
          id: `__tabbed_${setId}_${i + 1}`,
          name: `__tabbed_${setId}`,
          type: 'radio',
        };
        if (i === 0) inputProperties.checked = true;
        inputs.push(element('input', inputProperties));

        let labelChildren = [{ type: 'text', value: `Tab ${i + 1}` }];
        const children = [...(tab.children ?? [])];
        const firstChild = children[0];
        if (firstChild?.type === 'paragraph' && firstChild.data?.directiveLabel) {
          labelChildren = firstChild.children;
          children.shift();
        }
        labels.push(element('label', { for: `__tabbed_${setId}_${i + 1}` }, labelChildren));
        blocks.push(element('div', { class: 'tabbed-block' }, children));
      });

      const tabSet = element(
        'div',
        { class: 'tabbed-set tabbed-alternate', 'data-tabs': `${setId}:${run.length}` },
        [
          ...inputs,
          element('div', { class: 'tabbed-labels' }, labels),
          element('div', { class: 'tabbed-content' }, blocks),
        ]
      );

      ctx.replaceNode(node, tabSet);
      for (const sibling of run.slice(1)) ctx.removeNode(sibling);
    },
  };
}
