---
title: live editor
hide:
  - toc
  - navigation
---
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<style>
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

    .rc-button.button-selected code {
        background-color: rgba(223, 200, 128, 0.4);
    }
    .rc-element.c-black {
        color: #000000;
    }
    .rc-element.c-blue {
        color: #000080;
    }
    .rc-element.c-green {
        color: #008000;
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
        color: #800080;
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
        opacity: 75%;
    }
</style>
# Live Style Editor

This page contains a live editor for `rich-click` styles.

At the bottom of the page, there is generated code for the sample output.

Unlike the rest of the documentation,
the colors in this page have been calibrated to better match how typical modern terminals tend to render these colors.

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
                        <select class="rccfg-style-option rccfg-selector" data-target="rccfg-style-option">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan" selected>cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-option rccfg-dim-button" data-target="rccfg-style-option"><code>dim</code></button>
                        <button class="rc-button rccfg-style-option rccfg-bold-button" data-target="rccfg-style-option"><code>bold</code></button>
                        <button class="rc-button rccfg-style-option rccfg-italic-button" data-target="rccfg-style-option"><code>italic</code></button>
                    </td>
                </tr>
                <tr>
                    <td>
                        <label for="color-select">STYLE_ARGUMENT</label>
                    </td>
                    <td>
                        <select class="rccfg-style-argument rccfg-selector" data-target="rccfg-style-argument">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan" selected>cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-argument rccfg-dim-button" data-target="rccfg-style-argument"><code>dim</code></button>
                        <button class="rc-button rccfg-style-argument rccfg-bold-button" data-target="rccfg-style-argument"><code>bold</code></button>
                        <button class="rc-button rccfg-style-argument rccfg-italic-button" data-target="rccfg-style-argument"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_COMMAND</label>
                    </td>
                    <td>
                        <select class="rccfg-style-command rccfg-selector" data-target="rccfg-style-command">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan" selected>cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-command rccfg-dim-button" data-target="rccfg-style-command"><code>dim</code></button>
                        <button class="rc-button rccfg-style-command rccfg-bold-button" data-target="rccfg-style-command"><code>bold</code></button>
                        <button class="rc-button rccfg-style-command rccfg-italic-button" data-target="rccfg-style-command"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_SWITCH</label>
                    </td>
                    <td>
                        <select class="rccfg-style-switch rccfg-selector" data-target="rccfg-style-switch">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan" selected>cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-switch rccfg-dim-button" data-target="rccfg-style-switch"><code>dim</code></button>
                        <button class="rc-button rccfg-style-switch rccfg-bold-button" data-target="rccfg-style-switch"><code>bold</code></button>
                        <button class="rc-button rccfg-style-switch rccfg-italic-button" data-target="rccfg-style-switch"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_METAVAR</label>
                    </td>
                    <td>
                        <select class="rccfg-style-metavar rccfg-selector" data-target="rccfg-style-metavar">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow" selected>yellow</option>
                            <option value="cyan">cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-metavar rccfg-dim-button" data-target="rccfg-style-metavar"><code>dim</code></button>
                        <button class="rc-button rccfg-style-metavar rccfg-bold-button" data-target="rccfg-style-metavar"><code>bold</code></button>
                        <button class="rc-button rccfg-style-metavar rccfg-italic-button" data-target="rccfg-style-metavar"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_METAVAR_SEPARATOR</label>
                    </td>
                    <td>
                        <select class="rccfg-style-metavar-separator rccfg-selector" data-target="rccfg-style-metavar-separator">
                            <option value="" selected>(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan">cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-metavar-separator rccfg-dim-button" data-target="rccfg-style-metavar-separator"><code>dim</code></button>
                        <button class="rc-button rccfg-style-metavar-separator rccfg-bold-button" data-target="rccfg-style-metavar-separator"><code>bold</code></button>
                        <button class="rc-button rccfg-style-metavar-separator rccfg-italic-button" data-target="rccfg-style-metavar-separator"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_USAGE</label>
                    </td>
                    <td>
                        <select class="rccfg-style-usage rccfg-selector" data-target="rccfg-style-usage">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow" selected>yellow</option>
                            <option value="cyan">cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-usage rccfg-dim-button" data-target="rccfg-style-usage"><code>dim</code></button>
                        <button class="rc-button rccfg-style-usage rccfg-bold-button" data-target="rccfg-style-usage"><code>bold</code></button>
                        <button class="rc-button rccfg-style-usage rccfg-italic-button" data-target="rccfg-style-usage"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_USAGE_COMMAND</label>
                    </td>
                    <td>
                        <select class="rccfg-style-usage-command rccfg-selector" data-target="rccfg-style-usage-command">
                            <option value="" selected>(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan">cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-usage-command rccfg-dim-button" data-target="rccfg-style-usage-command"><code>dim</code></button>
                        <button class="rc-button rccfg-style-usage-command rccfg-bold-button" data-target="rccfg-style-usage-command"><code>bold</code></button>
                        <button class="rc-button rccfg-style-usage-command rccfg-italic-button" data-target="rccfg-style-usage-command"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_REQUIRED_SHORT</label>
                    </td>
                    <td>
                        <select class="rccfg-style-required-short rccfg-selector" data-target="rccfg-style-required-short">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan">cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red" selected>red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-required-short rccfg-dim-button" data-target="rccfg-style-required-short"><code>dim</code></button>
                        <button class="rc-button rccfg-style-required-short rccfg-bold-button" data-target="rccfg-style-required-short"><code>bold</code></button>
                        <button class="rc-button rccfg-style-required-short rccfg-italic-button" data-target="rccfg-style-required-short"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_REQUIRED_LONG</label>
                    </td>
                    <td>
                        <select class="rccfg-style-required-long rccfg-selector" data-target="rccfg-style-required-long">
                            <option value="">(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan">cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red" selected>red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-required-long rccfg-dim-button" data-target="rccfg-style-required-long"><code>dim</code></button>
                        <button class="rc-button rccfg-style-required-long rccfg-bold-button" data-target="rccfg-style-required-long"><code>bold</code></button>
                        <button class="rc-button rccfg-style-required-long rccfg-italic-button" data-target="rccfg-style-required-long"><code>italic</code></button>
                    </td>
                </tr>
        
                <tr>
                    <td>
                        <label for="color-select">STYLE_PANEL_BORDER</label>
                    </td>
                    <td>
                        <select class="rccfg-style-panel-border rccfg-selector" data-target="rccfg-style-panel-border">
                            <option value="" selected>(none)</option>
                            <option value="black">black</option>
                            <option value="blue">blue</option>
                            <option value="green">green</option>
                            <option value="yellow">yellow</option>
                            <option value="cyan">cyan</option>
                            <option value="white">white</option>
                            <option value="magenta">magenta</option>
                            <option value="red">red</option>
                        </select>
                    </td>
                    <td>
                        <button class="rc-button rccfg-style-panel-border rccfg-dim-button" data-target="rccfg-style-panel-border"><code>dim</code></button>
                        <button class="rc-button rccfg-style-panel-border rccfg-bold-button" data-target="rccfg-style-panel-border"><code>bold</code></button>
                        <button class="rc-button rccfg-style-panel-border rccfg-italic-button" data-target="rccfg-style-panel-border"><code>italic</code></button>
                    </td>
                </tr>
        
            </tbody>
        </table>
    </div>
    <div class="right-column">
        <div class="termy">
        ```console
         <span class="rc-element s-bold c-yellow rccfg-style-usage">Usage:</span> <span class="rc-element s-bold rccfg-style-usage-command">docs</span> [<span class="rc-element rccfg-style-argument s-bold c-cyan">OPTIONS</span>] <span class="rc-element rccfg-style-argument s-bold c-cyan">FOO</span> <span class="rc-element rccfg-style-argument s-bold c-cyan">COMMAND</span> [<span class="rc-element rccfg-style-argument s-bold c-cyan">ARGS</span>]...                             
        
         Help text for CLI
        
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────╮</span>
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span class="rc-element s-bold c-cyan rccfg-style-option">--bar</span>   <span class="rc-element s-bold c-green rccfg-style-switch">-b</span>  <span class="rc-element s-bold c-yellow rccfg-style-metavar">TEXT</span>     Lorem ipsum <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">[default: (someval)]</span>             <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span class="rc-element c-red rccfg-style-required-short">*</span>  <span class="rc-element s-bold c-cyan rccfg-style-option">--baz</span>       <span class="rc-element s-bold c-yellow rccfg-style-metavar"><span class="rc-element s-dim rccfg-style-metavar-separator">[</span>a<span class="rc-element s-dim rccfg-style-metavar-separator">|</span>b<span class="rc-element s-dim rccfg-style-metavar-separator">|</span>c<span class="rc-element s-dim rccfg-style-metavar-separator">]</span></span>  Choose wisely <span class="rc-element s-dim c-red rccfg-style-required-long">[required]</span>                     <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>    <span <span class="rc-element s-bold c-cyan rccfg-style-option">--help</span>      <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">       </span>  Show this message and exit.                  <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Commands ───────────────────────────────────────────────────────────╮</span>
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span class="rc-element c-cyan s-bold rccfg-style-command">subcommand           </span> Help text for subcommand                       <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
        ```
        </div>
    </div>
</div>

=== "`RichHelpConfiguration()`"
    Work in progress

=== "Global config"
    <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">rich_click</span> <span class="k">as</span> <span class="nn">click</span><br>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_OPTION</span> <span class="o">=</span> <span class="s2">&quot;&quot;</span>
    <span class="n">click</span><span class="o">.</span><span class="n">rich_click</span><span class="o">.</span><span class="n">STYLE_ARGUMENT</span> <span class="o">=</span> <span class="s2">&quot;&quot;</span><br>
    <span class="nd">@click</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="s2">&quot;my-command&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">argument</span><span class="p">(</span><span class="s2">&quot;foo&quot;</span><span class="p">)</span>
    <span class="nd">@click</span><span class="o">.</span><span class="n">option</span><span class="p">(</span><span class="s2">&quot;--bar&quot;</span><span class="p">,</span> <span class="s2">&quot;-b&quot;</span><span class="p">,</span> <span class="n">help</span><span class="o">=</span><span class="s2">&quot;Lorem ipsum&quot;</span><span class="p">,</span> <span class="n">show_default</span><span class="o">=</span><span class="s2">&quot;someval&quot;</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">cli</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
    <span class="w">    </span><span class="sd">&quot;&quot;&quot;Help text for CLI&quot;&quot;&quot;</span><br>
    <span class="nd">@cli</span><span class="o">.</span><span class="n">command</span><span class="p">(</span><span class="s2">&quot;subcommand&quot;</span><span class="p">)</span>
    <span class="k">def</span> <span class="nf">subcommand</span><span class="p">(</span><span class="n">foo</span><span class="p">,</span> <span class="n">bar</span><span class="p">):</span>
    <span class="w">    </span><span class="sd">&quot;&quot;&quot;Help text for subcommand&quot;&quot;&quot;</span><br>
    <span class="k">if</span> <span class="vm">__name__</span> <span class="o">==</span> <span class="s2">&quot;__main__&quot;</span><span class="p">:</span>
        <span class="c1"># TERMINAL_WIDTH=72 rich-click docs.live_style_editor:cli --help/span>
        <span class="n">cli</span><span class="p">()</span><br>
    </code></pre></div>

<script>
    $(document).ready(function() {

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
        $(".rc-button.rccfg-style-required-long.rccfg-dim-button").each(function() {
            $(this).click();
        });

    });
</script>

<script>
    $(".rccfg-selector").change(function() {
        $("." + $(this).data("target")).removeClass(function(index, className) {
            return (className.match(/(^|\s)c-\S+/g) || []).join(' ');
        });
        if ($(this).val() != "") {
            $("span ." + $(this).data("target")).toggleClass("c-" + $(this).val());
        }
    }).change();

    $(".rccfg-bold-button").click(function() {
        $("." + $(this).data("target")).toggleClass("s-bold");
        $(this).toggleClass("button-selected");
    });

    $(".rccfg-dim-button").click(function() {
        $("." + $(this).data("target")).toggleClass("s-dim");
        $(this).toggleClass("button-selected");
    });

    $(".rccfg-italic-button").click(function() {
        $("." + $(this).data("target")).toggleClass("s-italic");
        $(this).toggleClass("button-selected");
    });
</script>
