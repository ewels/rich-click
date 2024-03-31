---
title: 'rich-click: Live Style Editor'
hide:
  - toc
  - navigation
---
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
const text = "Live Style Editor";
let index = 0;

type();
</script>
<style>
    #terminal-header {
      text-shadow: -4px 4px rgba(128, 128, 128, 0.1);
      overflow: hidden;
      white-space: nowrap;
      margin: 0 auto;
      padding: 10px;
      display: inline-block;
    }

    [data-termynal] {
        width: 100%;
        padding: 75px 25px 25px;
    }

    .container {
        display: flex;
        height: 100%;
    }

    .container .left-column {
        flex: 3 0 auto;
        align-content: center;
    }

    .container .right-column {
        flex: 20 7 auto;
        padding: 25px 15px;
        align-content: center;
        display: inline-block;
    }

    @media (max-width: 74em) {
        .container {
            flex-direction: column;
            align-items: center;
            width: 100%;
        }

        .container .left-column, .container .right-column {
            flex: 0 0 auto;
            padding: 0;
            width: 100%;
            display: block;
        }

        .container .left-column table {
            margin: 0;
            padding: 0;
            width: 100%;
        }
}

    .rc-element.c-black {
        color: #000000;
    }
    .rc-element.c-blue {
        color: #0088CC;
    }
    .rc-element.c-green {
        color: #338022;
    }
    .rc-element.c-yellow {
        color: #AA8800;
    }
    .rc-element.c-cyan {
        color: #009090;
    }
    .rc-element.c-white {
        color: #c0c0c0;
    }
    .rc-element.c-magenta {
        color: #9966AA;
    }
    .rc-element.c-red {
        color: #EE5555;
    }
    .rc-element.s-italic {
        font-style: italic;
    }
    .rc-element.s-bold {
        font-weight: bold;
    }
    .rc-element.s-dim {
        opacity: 50%;
    }
    .color-option[data-color="black"] {
        background-color: #000000;
    }
    .color-option[data-color="blue"] {
        background-color: #0088CC;
    }
    .color-option[data-color="green"] {
        background-color: #338022;
    }
    .color-option[data-color="yellow"] {
        background-color: #AA8800;
    }
    .color-option[data-color="cyan"] {
        background-color: #009090;
    }
    .color-option[data-color="white"] {
        background-color: #c0c0c0;
    }
    .color-option[data-color="magenta"] {
        background-color: #9966AA;
    }
    .color-option[data-color="red"] {
        background-color: #EE5555;
    }
    .color-grid {
        display: grid;
        grid-template-columns: repeat(4, 1.1em);
        grid-gap: 0.2em;
    }
    .color-option {
        width: 1.1em;
        height: 1.1em;
        cursor: pointer;
        opacity: 0.2;
        transition: opacity 0.2s ease;
    }
    .color-option:hover {
        opacity: 0.8;
    }
    .color-option.selected-color {
        opacity: 1;
    }
    .rc-button.button-selected code {
      background-color: rgba(127, 127, 127, 0.4);
    }
</style>
<h1 id="terminal-header" style="width: 35%;">Live Style Editor</h1>

This page contains a live editor for `rich-click` styles.

At the bottom of the page, there is generated code for the sample output.

The colors in this page have been calibrated to better match how typical modern terminals tend to render these colors.

<div class="container">
    <div class="left-column">
        <table>
            <thead>
                <td>
                    Option
                </td>
                <td>
                    Color
                </td>
                <td>
                    Other styles
                </td>
            </thead>
            <tbody>
                <tr>
                    <td>
                        <label for="color-select">STYLE_OPTION</label>
                    </td>
                    <td>
                        <div class="rccfg-style-option color-grid" data-target="rccfg-style-option">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option selected-color" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-option rccfg-bold-button" data-target="rccfg-style-option"><code>bold</code></button>
                        <button class="rc-button rccfg-style-option rccfg-dim-button" data-target="rccfg-style-option"><code>dim</code></button>
                        <button class="rc-button rccfg-style-option rccfg-italic-button" data-target="rccfg-style-option"><code>italic</code></button>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="color-select">STYLE_ARGUMENT</label>
                    </td>
                    <td>
                        <div class="rccfg-style-argument color-grid" data-target="rccfg-style-argument">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option selected-color" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-argument rccfg-bold-button" data-target="rccfg-style-argument"><code>bold</code></button>
                        <button class="rc-button rccfg-style-argument rccfg-dim-button" data-target="rccfg-style-argument"><code>dim</code></button>
                        <button class="rc-button rccfg-style-argument rccfg-italic-button" data-target="rccfg-style-argument"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_COMMAND</label>
                    </td>
                    <td>
                        <div class="rccfg-style-command color-grid" data-target="rccfg-style-command">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option selected-color" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-command rccfg-bold-button" data-target="rccfg-style-command"><code>bold</code></button>
                        <button class="rc-button rccfg-style-command rccfg-dim-button" data-target="rccfg-style-command"><code>dim</code></button>
                        <button class="rc-button rccfg-style-command rccfg-italic-button" data-target="rccfg-style-command"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_SWITCH</label>
                    </td>
                    <td>
                        <div class="rccfg-style-switch color-grid" data-target="rccfg-style-switch">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option selected-color" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-switch rccfg-bold-button" data-target="rccfg-style-switch"><code>bold</code></button>
                        <button class="rc-button rccfg-style-switch rccfg-dim-button" data-target="rccfg-style-switch"><code>dim</code></button>
                        <button class="rc-button rccfg-style-switch rccfg-italic-button" data-target="rccfg-style-switch"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_METAVAR</label>
                    </td>
                    <td>
                        <div class="rccfg-style-metavar color-grid" data-target="rccfg-style-metavar">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option selected-color" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-metavar rccfg-bold-button" data-target="rccfg-style-metavar"><code>bold</code></button>
                        <button class="rc-button rccfg-style-metavar rccfg-dim-button" data-target="rccfg-style-metavar"><code>dim</code></button>
                        <button class="rc-button rccfg-style-metavar rccfg-italic-button" data-target="rccfg-style-metavar"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_METAVAR_SEPARATOR</label>
                    </td>
                    <td>
                        <div class="rccfg-style-metavar-separator color-grid" data-target="rccfg-style-metavar-separator">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-metavar-separator rccfg-bold-button" data-target="rccfg-style-metavar-separator"><code>bold</code></button>
                        <button class="rc-button rccfg-style-metavar-separator rccfg-dim-button" data-target="rccfg-style-metavar-separator"><code>dim</code></button>
                        <button class="rc-button rccfg-style-metavar-separator rccfg-italic-button" data-target="rccfg-style-metavar-separator"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_USAGE</label>
                    </td>
                    <td>
                        <div class="rccfg-style-usage color-grid" data-target="rccfg-style-usage">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option selected-color" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-usage rccfg-bold-button" data-target="rccfg-style-usage"><code>bold</code></button>
                        <button class="rc-button rccfg-style-usage rccfg-dim-button" data-target="rccfg-style-usage"><code>dim</code></button>
                        <button class="rc-button rccfg-style-usage rccfg-italic-button" data-target="rccfg-style-usage"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_USAGE_COMMAND</label>
                    </td>
                    <td>
                        <div class="rccfg-style-usage-command color-grid" data-target="rccfg-style-usage-command">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-usage-command rccfg-bold-button" data-target="rccfg-style-usage-command"><code>bold</code></button>
                        <button class="rc-button rccfg-style-usage-command rccfg-dim-button" data-target="rccfg-style-usage-command"><code>dim</code></button>
                        <button class="rc-button rccfg-style-usage-command rccfg-italic-button" data-target="rccfg-style-usage-command"><code>italic</code></button>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="color-select">STYLE_HELPTEXT_FIRST_LINE</label>
                    </td>
                    <td>
                        <div class="rccfg-style-helptext-first-line color-grid" data-target="rccfg-style-helptext-first-line">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-helptext-first-line rccfg-bold-button" data-target="rccfg-style-helptext-first-line"><code>bold</code></button>
                        <button class="rc-button rccfg-style-helptext-first-line rccfg-dim-button" data-target="rccfg-style-helptext-first-line"><code>dim</code></button>
                        <button class="rc-button rccfg-style-helptext-first-line rccfg-italic-button" data-target="rccfg-style-helptext-first-line"><code>italic</code></button>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="color-select">STYLE_HELPTEXT</label>
                    </td>
                    <td>
                        <div class="rccfg-style-helptext color-grid" data-target="rccfg-style-helptext">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-helptext rccfg-bold-button" data-target="rccfg-style-helptext"><code>bold</code></button>
                        <button class="rc-button rccfg-style-helptext rccfg-dim-button" data-target="rccfg-style-helptext"><code>dim</code></button>
                        <button class="rc-button rccfg-style-helptext rccfg-italic-button" data-target="rccfg-style-helptext"><code>italic</code></button>
                    </td>
                </tr>

                <tr>
                    <td>
                        <label for="color-select">STYLE_REQUIRED_SHORT</label>
                    </td>
                    <td>
                        <div class="rccfg-style-required-short color-grid" data-target="rccfg-style-required-short">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option selected-color" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-required-short rccfg-bold-button" data-target="rccfg-style-required-short"><code>bold</code></button>
                        <button class="rc-button rccfg-style-required-short rccfg-dim-button" data-target="rccfg-style-required-short"><code>dim</code></button>
                        <button class="rc-button rccfg-style-required-short rccfg-italic-button" data-target="rccfg-style-required-short"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_REQUIRED_LONG</label>
                    </td>
                    <td>
                        <div class="rccfg-style-required-long color-grid" data-target="rccfg-style-required-long">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option selected-color" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-required-long rccfg-bold-button" data-target="rccfg-style-required-long"><code>bold</code></button>
                        <button class="rc-button rccfg-style-required-long rccfg-dim-button" data-target="rccfg-style-required-long"><code>dim</code></button>
                        <button class="rc-button rccfg-style-required-long rccfg-italic-button" data-target="rccfg-style-required-long"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_OPTIONS_PANEL_BORDER</label>
                    </td>
                    <td>
                        <div class="rccfg-style-options-panel-border color-grid" data-target="rccfg-style-options-panel-border">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-options-panel-border rccfg-bold-button" data-target="rccfg-style-options-panel-border"><code>bold</code></button>
                        <button class="rc-button rccfg-style-options-panel-border rccfg-dim-button" data-target="rccfg-style-options-panel-border"><code>dim</code></button>
                        <button class="rc-button rccfg-style-options-panel-border rccfg-italic-button" data-target="rccfg-style-options-panel-border"><code>italic</code></button>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="color-select">STYLE_COMMANDS_PANEL_BORDER</label>
                    </td>
                    <td>
                        <div class="rccfg-style-commands-panel-border color-grid" data-target="rccfg-style-commands-panel-border">
                            <div class="color-option" data-color="black"></div>
                            <div class="color-option" data-color="blue"></div>
                            <div class="color-option" data-color="green"></div>
                            <div class="color-option" data-color="yellow"></div>
                            <div class="color-option" data-color="cyan"></div>
                            <div class="color-option" data-color="white"></div>
                            <div class="color-option" data-color="magenta"></div>
                            <div class="color-option" data-color="red"></div>
                        </div>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-commands-panel-border rccfg-bold-button" data-target="rccfg-style-commands-panel-border"><code>bold</code></button>
                        <button class="rc-button rccfg-style-commands-panel-border rccfg-dim-button" data-target="rccfg-style-commands-panel-border"><code>dim</code></button>
                        <button class="rc-button rccfg-style-commands-panel-border rccfg-italic-button" data-target="rccfg-style-commands-panel-border"><code>italic</code></button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="right-column">
        <div class="termy">
        ```console
         <span class="rc-element s-bold c-yellow rccfg-style-usage">Usage:</span> <span class="rc-element s-bold rccfg-style-usage-command">docs</span> [<span class="rc-element rccfg-style-argument s-bold c-cyan">OPTIONS</span>] <span class="rc-element rccfg-style-argument s-bold c-cyan">FOO</span> <span class="rc-element rccfg-style-argument s-bold c-cyan">COMMAND</span> [<span class="rc-element rccfg-style-argument s-bold c-cyan">ARGS</span>]...                             
        
         <span class="rc-element rccfg-style-helptext-first-line">Help text for CLI</span>
         <span class="rc-element s-dim rccfg-style-helptext">Second line of help text.</span>                                              

        <span class="rc-element s-dim rccfg-style-options-panel-border">╭─ Options ────────────────────────────────────────────────────────────╮</span>
        <span class="rc-element s-dim rccfg-style-options-panel-border">│</span>    <span class="rc-element s-bold c-cyan rccfg-style-option">--bar</span>   <span class="rc-element s-bold c-green rccfg-style-switch">-b</span>  <span class="rc-element s-bold c-yellow rccfg-style-metavar">TEXT</span>     Lorem ipsum <span class="rc-element s-dim rccfg-style-options-panel-border">[default: (someval)]</span>             <span class="rc-element s-dim rccfg-style-options-panel-border">│</span>
        <span class="rc-element s-dim rccfg-style-options-panel-border">│</span> <span class="rc-element c-red rccfg-style-required-short">*</span>  <span class="rc-element s-bold c-cyan rccfg-style-option">--baz</span>       <span class="rc-element s-bold c-yellow rccfg-style-metavar"><span class="rc-element s-dim rccfg-style-metavar-separator">[</span>a<span class="rc-element s-dim rccfg-style-metavar-separator">|</span>b<span class="rc-element s-dim rccfg-style-metavar-separator">|</span>c<span class="rc-element s-dim rccfg-style-metavar-separator">]</span></span>  Choose wisely <span class="rc-element s-dim c-red rccfg-style-required-long">[required]</span>                     <span class="rc-element s-dim rccfg-style-options-panel-border">│</span>
        <span class="rc-element s-dim rccfg-style-options-panel-border">│</span>    <span <span class="rc-element s-bold c-cyan rccfg-style-option">--help</span>      <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">       </span>  Show this message and exit.                  <span class="rc-element s-dim rccfg-style-options-panel-border">│</span>
        <span class="rc-element s-dim rccfg-style-options-panel-border">╰──────────────────────────────────────────────────────────────────────╯</span>
        <span class="rc-element s-dim rccfg-style-commands-panel-border">╭─ Commands ───────────────────────────────────────────────────────────╮</span>
        <span class="rc-element s-dim rccfg-style-commands-panel-border">│</span> <span class="rc-element c-cyan s-bold rccfg-style-command">subcommand           </span> Help text for subcommand                       <span class="rc-element s-dim rccfg-style-commands-panel-border">│</span>
        <span class="rc-element s-dim rccfg-style-commands-panel-border">╰──────────────────────────────────────────────────────────────────────╯</span>
        ```
        </div>
    </div>
</div>

=== "`RichHelpConfiguration()`"
    <div class="copy highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">rich_click</span> <span class="k">as</span> <span class="nn">click</span><br>
    <span class="n">help_config</span> <span class="o">=</span> <span class="n">click</span><span class="o">.</span><span class="n">RichHelpConfiguration</span><span class="p">(</span>
        <span class="n">style_option</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-option">bold </span><span class="rccfg-code-dim rccfg-style-option"></span><span class="rccfg-code-italic rccfg-style-option"></span><span class="rccfg-code-color rccfg-style-option">cyan</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_argument</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-argument">bold </span><span class="rccfg-code-dim rccfg-style-argument"></span><span class="rccfg-code-italic rccfg-style-argument"></span><span class="rccfg-code-color rccfg-style-argument">cyan</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_command</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-command">bold </span><span class="rccfg-code-dim rccfg-style-command"></span><span class="rccfg-code-italic rccfg-style-command"></span><span class="rccfg-code-color rccfg-style-command">cyan</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_switch</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-switch">bold </span><span class="rccfg-code-dim rccfg-style-switch"></span><span class="rccfg-code-italic rccfg-style-switch"></span><span class="rccfg-code-color rccfg-style-switch">green</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_metavar</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-metavar">bold </span><span class="rccfg-code-dim rccfg-style-metavar"></span><span class="rccfg-code-italic rccfg-style-metavar"></span><span class="rccfg-code-color rccfg-style-metavar">yellow</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_metavar_separator</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-metavar-separator"></span><span class="rccfg-code-dim rccfg-style-metavar-separator">dim</span><span class="rccfg-code-italic rccfg-style-metavar-separator"></span><span class="rccfg-code-color rccfg-style-metavar-separator"></span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_usage</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-usage">bold </span><span class="rccfg-code-dim rccfg-style-usage"></span><span class="rccfg-code-italic rccfg-style-usage"></span><span class="rccfg-code-color rccfg-style-usage">yellow</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_usage_command</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-usage-command">bold </span><span class="rccfg-code-dim rccfg-style-usage-command"></span><span class="rccfg-code-italic rccfg-style-usage-command"></span><span class="rccfg-code-color rccfg-style-usage-command"></span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_helptext_first_line</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-helptext-first-line"></span><span class="rccfg-code-dim rccfg-style-helptext-first-line"></span><span class="rccfg-code-italic rccfg-style-helptext-first-line"></span><span class="rccfg-code-color rccfg-style-helptext-first-line"></span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_helptext</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-helptext"></span><span class="rccfg-code-dim rccfg-style-helptext">dim</span><span class="rccfg-code-italic rccfg-style-helptext"></span><span class="rccfg-code-color rccfg-style-helptext"></span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_required_short</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-required-short"></span><span class="rccfg-code-dim rccfg-style-required-short"></span><span class="rccfg-code-italic rccfg-style-required-short"></span><span class="rccfg-code-color rccfg-style-required-short">red</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_required_long</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-required-long"></span><span class="rccfg-code-dim rccfg-style-required-long">dim </span><span class="rccfg-code-italic rccfg-style-required-long"></span><span class="rccfg-code-color rccfg-style-required-long">red</span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_options_panel_border</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-options-panel-border"></span><span class="rccfg-code-dim rccfg-style-options-panel-border">dim</span><span class="rccfg-code-italic rccfg-style-options-panel-border"></span><span class="rccfg-code-color rccfg-style-options-panel-border"></span></span>&quot;</span><span class="p">,</span>
        <span class="n">style_commands_panel_border</span><span class="o">=</span><span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-commands-panel-border"></span><span class="rccfg-code-dim rccfg-style-commands-panel-border">dim</span><span class="rccfg-code-italic rccfg-style-commands-panel-border"></span><span class="rccfg-code-color rccfg-style-commands-panel-border"></span></span>&quot;</span>
    <span class="p">)</span><br>
    <span class="nd">@click</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="s2">&quot;my-command&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">argument</span><span class="p">(</span><span class="s2">&quot;foo&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">option</span><span class="p">(</span><span class="s2">&quot;--bar&quot;</span><span class="p">,</span> <span class="s2">&quot;-b&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s2">&quot;Lorem ipsum&quot;</span><span class="p">,</span> <span class="n">show_default</span><span class="o">=</span><span class="s2">&quot;someval&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">option</span><span class="p">(</span><span class="s2">&quot;--baz&quot;</span><span class="p">,</span> <span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s2">&quot;Choose wisely&quot;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="n">click</span><span class="o">.</span><span class="n">Choice</span><span class="p">([</span><span class="s2">&quot;a&quot;</span><span class="p">,</span> <span class="s2">&quot;b&quot;</span><span class="p">,</span> <span class="s2">&quot;c&quot;</span><span class="p">]))</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">rich_config</span><span class="p">(</span><span class="n">help_config</span><span class="o">=</span><span class="n">help_config</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">cli</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
    <span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
    <span class="sd">    Help text for CLI</span><br>
    <span class="sd">    Second line of help text.</span>
    <span class="sd">    &quot;&quot;&quot;</span><br>
    <span class="nd">@cli</span><span class="o">.</span><span class="n">command</span><span class="p">(</span><span class="s2">&quot;subcommand&quot;</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">subcommand</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
    <span class="w">    </span><span class="sd">&quot;&quot;&quot;Help text for subcommand&quot;&quot;&quot;</span><br>
    <span class="k">if</span> <span class="vm">\_\_name\_\_</span> <span class="o">==</span> <span class="s2">&quot;\_\_main\_\_&quot;</span><span class="p">:</span>
        <span class="c1"># TERMINAL_WIDTH=72 rich-click docs.live_style_editor:cli --help</span>
        <span class="n">cli</span><span class="p">()</span><br>
    </code></pre></div>

=== "Global config"
    <div class="copy highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">rich_click</span> <span class="k">as</span> <span class="nn">click</span><br>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_OPTION</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-option">bold </span><span class="rccfg-code-dim rccfg-style-option"></span><span class="rccfg-code-italic rccfg-style-option"></span><span class="rccfg-code-color rccfg-style-option">cyan</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_ARGUMENT</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-argument">bold </span><span class="rccfg-code-dim rccfg-style-argument"></span><span class="rccfg-code-italic rccfg-style-argument"></span><span class="rccfg-code-color rccfg-style-argument">cyan</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_COMMAND</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-command">bold </span><span class="rccfg-code-dim rccfg-style-command"></span><span class="rccfg-code-italic rccfg-style-command"></span><span class="rccfg-code-color rccfg-style-command">cyan</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_SWITCH</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-switch">bold </span><span class="rccfg-code-dim rccfg-style-switch"></span><span class="rccfg-code-italic rccfg-style-switch"></span><span class="rccfg-code-color rccfg-style-switch">green</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_METAVAR</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-metavar">bold </span><span class="rccfg-code-dim rccfg-style-metavar"></span><span class="rccfg-code-italic rccfg-style-metavar"></span><span class="rccfg-code-color rccfg-style-metavar">yellow</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_METAVAR_SEPARATOR</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-metavar-separator"></span><span class="rccfg-code-dim rccfg-style-metavar-separator">dim</span><span class="rccfg-code-italic rccfg-style-metavar-separator"></span><span class="rccfg-code-color rccfg-style-metavar-separator"></span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_USAGE</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-usage">bold </span><span class="rccfg-code-dim rccfg-style-usage"></span><span class="rccfg-code-italic rccfg-style-usage"></span><span class="rccfg-code-color rccfg-style-usage">yellow</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_USAGE_COMMAND</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-usage-command">bold</span><span class="rccfg-code-dim rccfg-style-usage-command"></span><span class="rccfg-code-italic rccfg-style-usage-command"></span><span class="rccfg-code-color rccfg-style-usage-command"></span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_HELPTEXT_FIRST_LINE</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-helptext-first-line"></span><span class="rccfg-code-dim rccfg-style-helptext-first-line"></span><span class="rccfg-code-italic rccfg-style-helptext-first-line"></span><span class="rccfg-code-color rccfg-style-helptext-first-line"></span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_HELPTEXT</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-helptext"></span><span class="rccfg-code-dim rccfg-style-helptext">dim</span><span class="rccfg-code-italic rccfg-style-helptext"></span><span class="rccfg-code-color rccfg-style-helptext"></span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_REQUIRED_SHORT</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-required-short"></span><span class="rccfg-code-dim rccfg-style-required-short"></span><span class="rccfg-code-italic rccfg-style-required-short"></span><span class="rccfg-code-color rccfg-style-required-short">red</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_REQUIRED_LONG</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-required-long"></span><span class="rccfg-code-dim rccfg-style-required-long">dim </span><span class="rccfg-code-italic rccfg-style-required-long"></span><span class="rccfg-code-color rccfg-style-required-long">red</span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_OPTIONS_PANEL_BORDER</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-options-panel-border"></span><span class="rccfg-code-dim rccfg-style-options-panel-border">dim</span><span class="rccfg-code-italic rccfg-style-options-panel-border"></span><span class="rccfg-code-color rccfg-style-options-panel-border"></span></span>&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_COMMANDS_PANEL_BORDER</span> <span class="o">=</span> <span class="s2">&quot;<span class="rccfg-code-outer"><span class="rccfg-code-bold rccfg-style-commands-panel-border"></span><span class="rccfg-code-dim rccfg-style-commands-panel-border">dim</span><span class="rccfg-code-italic rccfg-style-commands-panel-border"></span><span class="rccfg-code-color rccfg-style-commands-panel-border"></span></span>&quot;</span><br>
    <span class="nd">@click</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="s2">&quot;my-command&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">argument</span><span class="p">(</span><span class="s2">&quot;foo&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">option</span><span class="p">(</span><span class="s2">&quot;--bar&quot;</span><span class="p">,</span> <span class="s2">&quot;-b&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s2">&quot;Lorem ipsum&quot;</span><span class="p">,</span> <span class="n">show_default</span><span class="o">=</span><span class="s2">&quot;someval&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">option</span><span class="p">(</span><span class="s2">&quot;--baz&quot;</span><span class="p">,</span> <span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s2">&quot;Choose wisely&quot;</span><span class="p">,</span> <span class="nb">type</span><span class="o">=</span><span class="n">click</span><span class="o">.</span><span class="n">Choice</span><span class="p">([</span><span class="s2">&quot;a&quot;</span><span class="p">,</span> <span class="s2">&quot;b&quot;</span><span class="p">,</span> <span class="s2">&quot;c&quot;</span><span class="p">]))</span>
    <span class="k">def</span> <span class="nf">cli</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
    <span class="w">    </span><span class="sd">&quot;&quot;&quot;</span>
    <span class="sd">    Help text for CLI</span><br>
    <span class="sd">    Second line of help text.</span>
    <span class="sd">    &quot;&quot;&quot;</span><br>
    <span class="nd">@cli</span><span class="o">.</span><span class="n">command</span><span class="p">(</span><span class="s2">&quot;subcommand&quot;</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">subcommand</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
    <span class="w">    </span><span class="sd">&quot;&quot;&quot;Help text for subcommand&quot;&quot;&quot;</span><br>
    <span class="k">if</span> <span class="vm">\_\_name\_\_</span> <span class="o">==</span> <span class="s2">&quot;\_\_main\_\_&quot;</span><span class="p">:</span>
        <span class="c1"># TERMINAL_WIDTH=72 rich-click docs.live_style_editor:cli --help</span>
        <span class="n">cli</span><span class="p">()</span><br>
    </code></pre></div>

<script>

    $(document).ready(function() {

        $(".color-option.selected-color").addClass("selected");

        $(".rccfg-selector").each(function() {
            var defaultIndex = $(this).data("default-index");
            if (!isNaN(defaultIndex) && defaultIndex >= 0 && defaultIndex < this.options.length) {
                this.selectedIndex = parseInt(defaultIndex);
            }
        });

        $(".rc-button.rccfg-style-argument.rccfg-bold-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-option.rccfg-bold-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-command.rccfg-bold-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-switch.rccfg-bold-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-metavar.rccfg-bold-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-metavar-separator.rccfg-dim-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-usage.rccfg-bold-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-usage-command.rccfg-bold-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-helptext.rccfg-dim-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-required-long.rccfg-dim-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-options-panel-border.rccfg-dim-button").each(function() {
            $(this).click();
        });
        $(".rc-button.rccfg-style-commands-panel-border.rccfg-dim-button").each(function() {
            $(this).click();
        });

    });
</script>

<script>
    function trimText() {
        $('.rccfg-code-outer').each(function() {
            var boldFlagText = $(this).find(".rccfg-code-bold");
            if ($(this).text().slice(-5) === "bold ") {
                boldFlagText.text("bold");
            }
            else if ((boldFlagText.text() === "bold") && $(this).text().slice(-4) !== "bold") {
                boldFlagText.text("bold ");
            }
            var dimFlagText = $(this).find(".rccfg-code-dim");
            if ($(this).text().slice(-4) === "dim ") {
                dimFlagText.text("dim");
            }
            else if (dimFlagText.text() === "dim" && $(this).text().slice(-3) !== "dim") {
                dimFlagText.text("dim ");
            }
            var italicFlagText = $(this).find(".rccfg-code-italic");
            if ($(this).text().slice(-7) === "italic ") {
                italicFlagText.text("italic");
            }
            else if (italicFlagText.text() === "italic" && $(this).text().slice(-6) !== "italic") {
                italicFlagText.text("italic ");
            }
        });
    }

    $(".color-grid .color-option").click(function() {
        var colorGrid = $(this).closest(".color-grid");
        var targetClass = colorGrid.data("target");

        colorGrid.find(".color-option").not(this).removeClass("selected-color");

        $("." + targetClass).removeClass(function(index, className) {
            return (className.match(/(^|\s)c-\S+/g) || []).join(' ');
        });
        var isSelected = $(this).hasClass("selected-color");
        var selectedColor = $(this).data("color");
        $("span .rc-element." + targetClass).toggleClass("c-" + selectedColor, !isSelected);
        $(this).toggleClass("selected-color");

        if (!isSelected) {
            $("span .rccfg-code-color." + targetClass).text(selectedColor);
        }
        else {
            $("span .rccfg-code-color." + targetClass).text("");
        }
        trimText()
    }).change();

    $(".rccfg-bold-button").click(function() {
        var targetClass = $(this).data("target");
        var loc = $("." + targetClass);
        loc.toggleClass("s-bold");
        $(this).toggleClass("button-selected");
        if (loc.hasClass("s-bold")) {
            $("span .rccfg-code-bold." + targetClass).text("bold ")
        }
        else {
            $("span .rccfg-code-bold." + targetClass).text("")
        }
        trimText()
    });

    $(".rccfg-dim-button").click(function() {
        var targetClass = $(this).data("target");
        var loc = $("." + targetClass);
        loc.toggleClass("s-dim");
        $(this).toggleClass("button-selected");
        if (loc.hasClass("s-dim")) {
            $("span .rccfg-code-dim." + targetClass).text("dim ")
        }
        else {
            $("span .rccfg-code-dim." + targetClass).text("")
        }
        trimText()
    });

    $(".rccfg-italic-button").click(function() {
        var targetClass = $(this).data("target");
        var loc = $("." + targetClass);
        loc.toggleClass("s-italic");
        $(this).toggleClass("button-selected");
        if (loc.hasClass("s-italic")) {
            $("span .rccfg-code-italic." + targetClass).text("italic ")
        }
        else {
            $("span .rccfg-code-italic." + targetClass).text("")
        }
        trimText()
    });
</script>
