// Renders GitHub-style blockquote alerts as Material-style admonitions:
//
//     > [!NOTE]
//     > Useful information.
//
// These appear in the root CHANGELOG.md and CONTRIBUTING.md files, which are
// pulled into the docs by scripts/prepare-content.mjs. Replaces the
// mkdocs-github-admonitions plugin.
import { buildAside, DEFAULT_TITLES } from './admonition-common.mjs';

const ALERT_RE = /^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*/;

// GitHub alert type -> admonition variant. Titles come from DEFAULT_TITLES,
// except CAUTION which keeps its GitHub name on the danger styling.
const ALERT_VARIANTS = {
  NOTE: 'note',
  TIP: 'tip',
  IMPORTANT: 'important',
  WARNING: 'warning',
  CAUTION: 'danger',
};

export function satteriGithubAlerts() {
  return {
    name: 'rich-click-github-alerts',
    blockquote(node) {
      if (!node.children) return;
      const firstParagraph = node.children[0];
      if (firstParagraph?.type !== 'paragraph') return;
      const firstText = firstParagraph.children[0];
      if (firstText?.type !== 'text') return;
      const match = ALERT_RE.exec(firstText.value);
      if (!match) return;

      const variant = ALERT_VARIANTS[match[1]];
      const title = match[1] === 'CAUTION' ? 'Caution' : DEFAULT_TITLES[variant];
      const remainder = firstText.value.slice(match[0].length);
      const inlineRest = [...firstParagraph.children.slice(1)];
      if (remainder.length > 0) {
        inlineRest.unshift({ type: 'text', value: remainder });
      }
      const children = [...node.children.slice(1)];
      if (inlineRest.length > 0) {
        children.unshift({ type: 'paragraph', children: inlineRest });
      }

      return buildAside(variant, [{ type: 'text', value: title }], title, children);
    },
  };
}
