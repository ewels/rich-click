// The site's Sätteri Markdown pipeline, shared between astro.config.mjs and
// scripts/debug-render.mjs so the debug tool always matches production.
import { satteriIncludes } from './satteri-includes.mjs';
import { satteriTabs } from './satteri-tabs.mjs';
import { satteriGithubAlerts } from './satteri-github-alerts.mjs';
import { satteriMermaid } from './satteri-mermaid.mjs';

export const features = {
  directive: true,
};

export const mdastPlugins = [
  satteriIncludes(),
  satteriMermaid(),
  satteriGithubAlerts(),
  // Passed as a factory so the tab-set id counter resets per document.
  satteriTabs,
];
