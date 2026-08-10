// Shared helpers for rendering Material for MkDocs style admonitions as
// Starlight-compatible asides. Used by the admonitions and GitHub-alerts plugins.

// Material Design icon paths (https://pictogrammers.com/library/mdi/), matching
// the icons Material for MkDocs uses for each admonition type.
export const ICONS = {
  // pencil
  note: 'M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z',
  // information
  info: 'M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',
  // fire
  tip: 'M17.66,11.2C17.43,10.9 17.15,10.64 16.89,10.38C16.22,9.78 15.46,9.35 14.82,8.72C13.33,7.26 13,4.85 13.95,3C13,3.23 12.17,3.75 11.46,4.32C8.87,6.4 7.85,10.07 9.07,13.22C9.11,13.32 9.15,13.42 9.15,13.55C9.15,13.77 9,13.97 8.8,14.05C8.57,14.15 8.33,14.09 8.14,13.93C8.08,13.88 8.04,13.83 8,13.76C6.87,12.33 6.69,10.28 7.45,8.64C5.78,10 4.87,12.3 5,14.47C5.06,14.97 5.12,15.47 5.29,15.97C5.43,16.57 5.7,17.17 6,17.7C7.08,19.43 8.95,20.67 10.96,20.92C13.1,21.19 15.39,20.8 17.03,19.32C18.86,17.66 19.5,15 18.56,12.72L18.43,12.46C18.22,12 17.66,11.2 17.66,11.2M14.5,17.5C14.22,17.74 13.76,18 13.4,18.1C12.28,18.5 11.16,17.94 10.5,17.28C11.69,17 12.4,16.12 12.61,15.23C12.78,14.43 12.46,13.77 12.33,13C12.21,12.26 12.23,11.63 12.5,10.94C12.69,11.32 12.89,11.7 13.13,12C13.9,13 15.11,13.44 15.37,14.8C15.41,14.94 15.43,15.08 15.43,15.23C15.46,16.05 15.1,16.95 14.5,17.5Z',
  // check-circle
  success: 'M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z',
  // alert (triangle)
  warning: 'M13,14H11V9H13M13,18H11V16H13M1,21H23L12,2L1,21Z',
  // close-circle
  failure: 'M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z',
  // lightning-bolt
  danger: 'M7,2V13H10V22L17,10H13L17,2H7Z',
  // flask
  example: 'M6,22A3,3 0 0,1 3,19C3,18.4 3.18,17.84 3.5,17.37L9,7.81V6A1,1 0 0,1 8,5V4A2,2 0 0,1 10,2H14A2,2 0 0,1 16,4V5A1,1 0 0,1 15,6V7.81L20.5,17.37C20.82,17.84 21,18.4 21,19A3,3 0 0,1 18,22H6M5,19A1,1 0 0,0 6,20H18A1,1 0 0,0 19,19C19,18.79 18.93,18.59 18.82,18.43L16.53,14.47L14,17L8.93,11.93L5.18,18.43C5.07,18.59 5,18.79 5,19M11,10A1,1 0 0,1 12,11A1,1 0 0,1 11,12A1,1 0 0,1 10,11A1,1 0 0,1 11,10Z',
  // alert-circle
  important: 'M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',
  // close-octagon
  error: 'M13,13H11V7H13M13,17H11V15H13M15.73,3H8.27L3,8.27V15.73L8.27,21H15.73L21,15.73V8.27L15.73,3Z',
};

// chevron-right, used as the collapsible-details caret.
export const CARET_ICON = 'M8.59,16.58L13.17,12L8.59,7.41L10,6L16,12L10,18L8.59,16.58Z';

export const VARIANTS = Object.keys(ICONS);

export const DEFAULT_TITLES = {
  note: 'Note',
  info: 'Info',
  tip: 'Tip',
  success: 'Success',
  warning: 'Warning',
  failure: 'Failure',
  danger: 'Danger',
  example: 'Example',
  important: 'Important',
  error: 'Error',
};

/** An mdast node rendered as the given HTML element. */
export function element(tagName, properties, children = []) {
  return {
    type: 'paragraph',
    data: { hName: tagName, hProperties: properties },
    children,
  };
}

export function iconHtml(variant, extraClass = 'starlight-aside__icon') {
  const path = ICONS[variant] ?? ICONS.note;
  return `<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" class="${extraClass}"><path d="${path}"/></svg>`;
}

/**
 * Build an aside (or collapsible details aside) mdast node.
 *
 * @param variant one of VARIANTS
 * @param titleNodes inline mdast nodes for the title
 * @param titleText plain-text title (for aria-label)
 * @param children block content nodes
 * @param details optional: `{ open: boolean }` renders a `<details>` block
 */
export function buildAside(variant, titleNodes, titleText, children, details = null) {
  const icon = { type: 'html', value: iconHtml(variant) };
  if (details) {
    const caret = {
      type: 'html',
      value: `<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor" class="sl-details__caret"><path d="${CARET_ICON}"/></svg>`,
    };
    const properties = {
      class: `starlight-aside starlight-aside--${variant} sl-details`,
    };
    if (details.open) properties.open = true;
    return element('details', properties, [
      element('summary', { class: 'starlight-aside__title sl-details__summary' }, [
        icon,
        ...titleNodes,
        caret,
      ]),
      element('div', { class: 'starlight-aside__content' }, children),
    ]);
  }
  return element(
    'aside',
    {
      'aria-label': titleText,
      class: `starlight-aside starlight-aside--${variant}`,
    },
    [
      element('p', { class: 'starlight-aside__title', 'aria-hidden': 'true' }, [
        icon,
        ...titleNodes,
      ]),
      element('div', { class: 'starlight-aside__content' }, children),
    ]
  );
}
