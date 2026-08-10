// The site's Sätteri Markdown pipeline, shared between astro.config.mjs and
// scripts/debug-render.mjs so the debug tool always matches production.
import { satteriIncludes } from './satteri-includes.mjs';
import { satteriAdmonitions } from './satteri-admonitions.mjs';
import { satteriTabs } from './satteri-tabs.mjs';
import { satteriImageAttrs } from './satteri-image-attrs.mjs';
import { satteriGithubAlerts } from './satteri-github-alerts.mjs';
import { satteriMdLinks } from './satteri-md-links.mjs';
import { satteriMermaid } from './satteri-mermaid.mjs';

export const features = {
  directive: true,
};

// Plugins operating on the pristine tree first; the structural transforms
// (admonitions, tabs) come last.
export const mdastPlugins = [
  satteriIncludes(),
  satteriImageAttrs(),
  satteriMdLinks(),
  satteriMermaid(),
  satteriGithubAlerts(),
  satteriAdmonitions(),
  // Passed as a factory so the tab-set id counter resets per document.
  satteriTabs,
];
