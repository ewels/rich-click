// Renders GitHub-style blockquote alerts as Starlight asides:
//
//     > [!NOTE]
//     > Useful information.
//
// These appear in the root CHANGELOG.md and CONTRIBUTING.md files (which must
// keep GitHub-flavoured syntax so they render on github.com) and are pulled
// into the docs by scripts/prepare-content.mjs.
import { element } from './mdast-helpers.mjs';

const ALERT_RE = /^\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*/;

// GitHub alert type -> [Starlight aside variant, displayed title].
// `important` is a custom variant (styled in src/styles/admonitions.css);
// the rest use Starlight's built-in aside styling.
const ALERT_VARIANTS = {
  NOTE: ['note', 'Note'],
  TIP: ['tip', 'Tip'],
  IMPORTANT: ['important', 'Important'],
  WARNING: ['caution', 'Warning'],
  CAUTION: ['danger', 'Caution'],
};

// Material Design icon paths (https://pictogrammers.com/library/mdi/).
const ICONS = {
  note: 'M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',
  tip: 'M12,2A7,7 0 0,1 19,9C19,11.38 17.81,13.47 16,14.74V17A1,1 0 0,1 15,18H9A1,1 0 0,1 8,17V14.74C6.19,13.47 5,11.38 5,9A7,7 0 0,1 12,2M9,21V20H15V21A1,1 0 0,1 14,22H10A1,1 0 0,1 9,21Z',
  important: 'M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',
  caution: 'M13,14H11V9H13M13,18H11V16H13M1,21H23L12,2L1,21Z',
  danger: 'M13,14H11V9H13M13,18H11V16H13M1,21H23L12,2L1,21Z',
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

      const [variant, title] = ALERT_VARIANTS[match[1]];
      const remainder = firstText.value.slice(match[0].length);
      const inlineRest = [...firstParagraph.children.slice(1)];
      if (remainder.length > 0) {
        inlineRest.unshift({ type: 'text', value: remainder });
      }
      const children = [...node.children.slice(1)];
      if (inlineRest.length > 0) {
        children.unshift({ type: 'paragraph', children: inlineRest });
      }

      const icon = {
        type: 'html',
        value: `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" class="starlight-aside__icon"><path d="${ICONS[variant]}"/></svg>`,
      };
      return element(
        'aside',
        { 'aria-label': title, class: `starlight-aside starlight-aside--${variant}` },
        [
          element('p', { class: 'starlight-aside__title', 'aria-hidden': 'true' }, [
            icon,
            { type: 'text', value: title },
          ]),
          element('div', { class: 'starlight-aside__content' }, children),
        ]
      );
    },
  };
}
