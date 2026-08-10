// Debug helper: render one Markdown file through the same satteri pipeline.
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
import { createSatteriMarkdownProcessor } from '@astrojs/markdown-satteri';
import { satteriIncludes } from '../plugins/satteri-includes.mjs';
import { satteriAdmonitions } from '../plugins/satteri-admonitions.mjs';
import { satteriTabs } from '../plugins/satteri-tabs.mjs';
import { satteriImageAttrs } from '../plugins/satteri-image-attrs.mjs';
import { satteriGithubAlerts } from '../plugins/satteri-github-alerts.mjs';
import { satteriMdLinks } from '../plugins/satteri-md-links.mjs';
import { satteriMermaid } from '../plugins/satteri-mermaid.mjs';

const file = process.argv[2];
const processor = await createSatteriMarkdownProcessor({
  features: { directive: true },
  mdastPlugins: [
    satteriIncludes(),
    satteriImageAttrs(),
    satteriMdLinks(),
    satteriMermaid(),
    satteriGithubAlerts(),
    satteriAdmonitions(),
    satteriTabs,
  ],
});

try {
  const result = await processor.render(fs.readFileSync(file, 'utf8'), {
    fileURL: pathToFileURL(file),
  });
  console.log(result.code.slice(0, 2000));
} catch (error) {
  console.error(error);
}
