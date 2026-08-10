// Debug helper: render one Markdown file through the site's satteri pipeline.
// Usage: node scripts/debug-render.mjs src/content/docs/documentation/themes.md
import fs from 'node:fs';
import { pathToFileURL } from 'node:url';
import { createSatteriMarkdownProcessor } from '@astrojs/markdown-satteri';
import { features, mdastPlugins } from '../plugins/pipeline.mjs';

const file = process.argv[2];
const processor = await createSatteriMarkdownProcessor({ features, mdastPlugins });

const result = await processor.render(fs.readFileSync(file, 'utf8'), {
  fileURL: pathToFileURL(file),
});
console.log(result.code);
