## Overview

**rich-click** comes with a CLI tool that allows you to format the Click help output for any CLI that uses Click.

To use, simply prefix `rich-click` to the command:

<div class="termy">

```console
$ rich-click flask --help

 <span style="color: #808000; text-decoration-color: #808000">Usage:</span> <span style="font-weight: bold">flask</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">OPTIONS</span>] <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">COMMAND</span> [<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">ARGS</span>]...

 A general utility script for Flask applications.
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">An application to load must be given with the &#x27;</span><span style="color: #7fbfbf; text-decoration-color: #7fbfbf; font-weight: bold">--app</span><span style="color: #7f7f7f; text-decoration-color: #7f7f7f">&#x27; option, </span>
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">&#x27;FLASK_APP&#x27; environment variable, or with a &#x27;wsgi.py&#x27; or &#x27;app.py&#x27; file</span>
 <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">in the current directory.</span>

<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Options ────────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--env-file</span>          <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-e</span>  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">FILE  </span>  Load environment variables from this <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 file. python-dotenv must be          <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 installed.                           <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--app</span>               <span style="color: #008000; text-decoration-color: #008000; font-weight: bold">-A</span>  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">IMPORT</span>  The Flask application or factory     <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 function to load, in the form        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 &#x27;module:name&#x27;. Module can be a       <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 dotted import or file path. Name is  <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 not required if it is &#x27;app&#x27;,         <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 &#x27;application&#x27;, &#x27;create_app&#x27;, or      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 &#x27;make_app&#x27;, and can be &#x27;name(args)&#x27;  <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>                                 to pass arguments.                   <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--debug</span>/<span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--no-debug</span>      <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">      </span>  Set debug mode.                      <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--version</span>               <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">      </span>  Show the Flask version.              <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">--help</span>                  <span style="color: #808000; text-decoration-color: #808000; font-weight: bold">      </span>  Show this message and exit.          <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╭─ Commands ───────────────────────────────────────────────────────────╮</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">routes       </span> Show the routes for the app.                           <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">run          </span> Run a development server.                              <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span> <span style="color: #008080; text-decoration-color: #008080; font-weight: bold">shell        </span> Run a shell in the app context.                        <span style="color: #7f7f7f; text-decoration-color: #7f7f7f">│</span>
<span style="color: #7f7f7f; text-decoration-color: #7f7f7f">╰──────────────────────────────────────────────────────────────────────╯</span>
```

</div>

## Render help text as HTML or SVG

You can also use `rich-click --output=html [command]` to render rich HTML for help text, or `rich-click --output=svg [command]` to generate an SVG.

This works for RichCommands as well as normal click Commands.

<div class="termy">
```console
$ rich-click --html flask --help

&lt;span style=&quot;color: #808000; text-decoration-color: #808000&quot;&gt;Usage:&lt;/span&gt; &lt;span style=&quot;font-weight: bold&quot;&gt;flask&lt;/span&gt; [&lt;span style=&quot;color: #008080; text-decoration-color: #008080; font-weight: bold&quot;&gt;OPTIONS&lt;/span&gt;] &lt;span style=&quot;color: #008080; text-decoration-color: #008080; font-weight: bold&quot;&gt;COMMAND&lt;/span&gt; [&lt;span style=&quot;color: #008080; text-decoration-color: #008080; font-weight: bold&quot;&gt;ARGS&lt;/span&gt;]...

A general utility script for Flask applications.  
 &lt;span style=&quot;color: #7f7f7f; text-decoration-color: #7f7f7f&quot;&gt;An application to load must be given with the &amp;#x27;&lt;/span&gt;&lt;span style=&quot;color: #7fbfbf; text-decoration-color: #7fbfbf; font-weight: bold&quot;&gt;--app&lt;/span&gt;&lt;span style=&quot;color: #7f7f7f; text-decoration-color: #7f7f7f&quot;&gt;&amp;#x27; option, &lt;/span&gt;  
 &lt;span style=&quot;color: #7f7f7f; text-decoration-color: #7f7f7f&quot;&gt;&amp;#x27;FLASK_APP&amp;#x27; environment variable, or with a &amp;#x27;wsgi.py&amp;#x27; or &amp;#x27;app.py&amp;#x27; file&lt;/span&gt;
&lt;span style=&quot;color: #7f7f7f; text-decoration-color: #7f7f7f&quot;&gt;in the current directory.&lt;/span&gt;

// The rest of the output is omitted

```
</div>
```