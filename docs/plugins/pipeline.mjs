// The site's Sätteri Markdown pipeline, shared between astro.config.mjs and
// scripts/debug-render.mjs so the debug tool always matches production.
import { satteriInlineCode } from './satteri-inline-code.mjs';
import { satteriGithubAlerts } from './satteri-github-alerts.mjs';
import { satteriMermaid } from './satteri-mermaid.mjs';

export const features = {
  directive: true,
};

export const mdastPlugins = [satteriInlineCode(), satteriMermaid(), satteriGithubAlerts()];
