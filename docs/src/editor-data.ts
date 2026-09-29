// Data and HTML generation for the Live Style Editor page (pages/editor.astro).
// Kept in a TypeScript module because the generated markup strings confuse the
// Astro compiler when defined in component frontmatter.

export const COLORS = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'];

export interface StyleFlags {
  color: string | null;
  bold: boolean;
  dim: boolean;
  italic: boolean;
}

/** Default style flags for each configurable rich-click style option. */
export const DEFAULT_STYLES: Record<string, StyleFlags> = {
  style_option: { color: 'cyan', bold: true, dim: false, italic: false },
  style_argument: { color: 'cyan', bold: true, dim: false, italic: false },
  style_command: { color: 'cyan', bold: true, dim: false, italic: false },
  style_switch: { color: 'green', bold: true, dim: false, italic: false },
  style_metavar: { color: 'yellow', bold: true, dim: false, italic: false },
  style_metavar_separator: { color: null, bold: false, dim: true, italic: false },
  style_usage: { color: 'yellow', bold: true, dim: false, italic: false },
  style_usage_command: { color: null, bold: true, dim: false, italic: false },
  style_helptext_first_line: { color: null, bold: false, dim: false, italic: false },
  style_helptext: { color: null, bold: false, dim: true, italic: false },
  style_option_default: { color: null, bold: false, dim: true, italic: false },
  style_required_short: { color: 'red', bold: false, dim: false, italic: false },
  style_required_long: { color: 'red', bold: false, dim: true, italic: false },
  style_options_panel_border: { color: null, bold: false, dim: true, italic: false },
  style_commands_panel_border: { color: null, bold: false, dim: true, italic: false },
};

export const options = Object.keys(DEFAULT_STYLES);

export const cls = (option: string): string => `rccfg-${option.replaceAll('_', '-')}`;

/** Class list for a terminal element styled by `option`, from the defaults. */
const elClasses = (option: string): string => {
  const style = DEFAULT_STYLES[option]!;
  const classes = ['rc-element', cls(option)];
  if (style.color) classes.push(`c-${style.color}`);
  if (style.bold) classes.push('s-bold');
  if (style.dim) classes.push('s-dim');
  if (style.italic) classes.push('s-italic');
  return classes.join(' ');
};

const el = (option: string, text: string): string =>
  `<span class="${elClasses(option)}">${text}</span>`;

// The sample terminal output (mirrors docs/live_style_editor.py).
const liveTerminal = ` ${el('style_usage', 'Usage:')} ${el('style_usage_command', 'docs')} [${el('style_argument', 'OPTIONS')}] ${el('style_argument', 'FOO')} ${el('style_argument', 'COMMAND')} [${el('style_argument', 'ARGS')}]...

 ${el('style_helptext_first_line', 'Help text for CLI')}
 ${el('style_helptext', 'Second line of help text.')}

${el('style_options_panel_border', '╭─ Options ────────────────────────────────────────────────────────────╮')}
${el('style_options_panel_border', '│')}    ${el('style_option', '--bar')}   ${el('style_switch', '-b')}  ${el('style_metavar', 'TEXT')}     Lorem ipsum ${el('style_option_default', '[default: (someval)]')}             ${el('style_options_panel_border', '│')}
${el('style_options_panel_border', '│')} ${el('style_required_short', '*')}  ${el('style_option', '--baz')}       ${el('style_metavar', `${el('style_metavar_separator', '[')}a${el('style_metavar_separator', '|')}b${el('style_metavar_separator', '|')}c${el('style_metavar_separator', ']')}`)}  Choose wisely ${el('style_required_long', '[required]')}                     ${el('style_options_panel_border', '│')}
${el('style_options_panel_border', '│')}    ${el('style_option', '--help')}             Show this message and exit.                  ${el('style_options_panel_border', '│')}
${el('style_options_panel_border', '╰──────────────────────────────────────────────────────────────────────╯')}
${el('style_commands_panel_border', '╭─ Commands ───────────────────────────────────────────────────────────╮')}
${el('style_commands_panel_border', '│')} ${el('style_command', 'subcommand           ')} Help text for subcommand                       ${el('style_commands_panel_border', '│')}
${el('style_commands_panel_border', '╰──────────────────────────────────────────────────────────────────────╯')}`;

export const terminalHtml = liveTerminal
  .split('\n')
  .map((row) => `<span class="go">${row}</span>`)
  .join('\n');

/** Render style flags as a rich style string, e.g. `bold dim cyan`. */
export const styleString = (style: StyleFlags): string =>
  [style.bold && 'bold', style.dim && 'dim', style.italic && 'italic', style.color]
    .filter(Boolean)
    .join(' ');

/** The editable style string span inside generated code. */
const styleSpans = (option: string): string =>
  `<span class="rccfg-code ${cls(option)}">${styleString(DEFAULT_STYLES[option]!)}</span>`;

// Pygments-style highlighted Python for the generated-code tabs.
const cliBody = (withRichConfig: boolean): string => `<span class="nd">@click</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="s2">&quot;my-command&quot;</span><span class="p">)</span>
<span class="nd">@click</span><span class="o">.</span><span class="n">argument</span><span class="p">(</span><span class="s2">&quot;foo&quot;</span><span class="p">)</span>
<span class="nd">@click</span><span class="o">.</span><span class="n">option</span><span class="p">(</span><span class="s2">&quot;--bar&quot;</span><span class="p">,</span> <span class="s2">&quot;-b&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s2">&quot;Lorem ipsum&quot;</span><span class="p">,</span> <span class="n">show_default</span><span class="o">=</span><span class="s2">&quot;someval&quot;</span><span class="p">)</span>
<span class="nd">@click</span><span class="o">.</span><span class="n">option</span><span class="p">(</span><span class="s2">&quot;--baz&quot;</span><span class="p">,</span> <span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s2">&quot;Choose wisely&quot;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="n">click</span><span class="o">.</span><span class="n">Choice</span><span class="p">([</span><span class="s2">&quot;a&quot;</span><span class="p">,</span> <span class="s2">&quot;b&quot;</span><span class="p">,</span> <span class="s2">&quot;c&quot;</span><span class="p">]))</span>
${withRichConfig ? '<span class="nd">@click</span><span class="o">.</span><span class="n">rich_config</span><span class="p">(</span><span class="n">help_config</span><span class="o">=</span><span class="n">help_config</span><span class="p">)</span>\n' : ''}<span class="k">def</span> <span class="nf">cli</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
<span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
<span class="sd">    Help text for CLI</span>

<span class="sd">    Second line of help text.</span>
<span class="sd">    &quot;&quot;&quot;</span>

<span class="nd">@cli</span><span class="o">.</span><span class="n">command</span><span class="p">(</span><span class="s2">&quot;subcommand&quot;</span><span class="p">)</span>
<span class="k">def</span> <span class="nf">subcommand</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
<span class="w">    </span><span class="sd">&quot;&quot;&quot;Help text for subcommand&quot;&quot;&quot;</span>

<span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
    <span class="n">cli</span><span class="p">()</span>`;

export const configCode = `<span class="kn">import</span> <span class="nn">rich_click</span> <span class="k">as</span> <span class="nn">click</span>

<span class="n">help_config</span> <span class="o">=</span> <span class="n">click</span><span class="o">.</span><span class="n">RichHelpConfiguration</span><span class="p">(</span>
${options
  .map(
    (option, i) =>
      `    <span class="n">${option}</span><span class="o">=</span><span class="s2">&quot;${styleSpans(option)}&quot;</span>${i < options.length - 1 ? '<span class="p">,</span>' : ''}`
  )
  .join('\n')}
<span class="p">)</span>

${cliBody(true)}`;

export const globalCode = `<span class="kn">import</span> <span class="nn">rich_click</span> <span class="k">as</span> <span class="nn">click</span>

${options
  .map(
    (option) =>
      `<span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">${option.toUpperCase()}</span> <span class="o">=</span> <span class="s2">&quot;${styleSpans(option)}&quot;</span>`
  )
  .join('\n')}

${cliBody(false)}`;
