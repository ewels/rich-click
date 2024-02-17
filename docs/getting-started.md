<div class="termy">

<div class="highlight"><pre><span></span><code><span class="gp">$ </span>python<span class="w"> </span>main.py

<span class="go">// If you run it without the argument, it shows a nice error</span>
<span class="go">&lt;font color=&quot;#F4BF75&quot;&gt;Usage: &lt;/font&gt;main.py [OPTIONS] NAME</span>
<span class="go">&lt;font color=&quot;#A5A5A1&quot;&gt;Try &lt;/font&gt;&lt;font color=&quot;#44919F&quot;&gt;&amp;apos;main.py &lt;/font&gt;&lt;font color=&quot;#44919F&quot;&gt;&lt;b&gt;--help&lt;/b&gt;&lt;/font&gt;&lt;font color=&quot;#44919F&quot;&gt;&amp;apos;&lt;/font&gt;&lt;font color=&quot;#A5A5A1&quot;&gt; for help.&lt;/font&gt;</span>
<span class="go">&lt;font color=&quot;#F92672&quot;&gt;╭─ Error ───────────────────────────────────────────╮&lt;/font&gt;</span>
<span class="go">&lt;font color=&quot;#F92672&quot;&gt;│&lt;/font&gt; Missing argument &amp;apos;NAME&amp;apos;. &lt;font color=&quot;#F92672&quot;&gt;│&lt;/font&gt;</span>
<span class="go">&lt;font color=&quot;#F92672&quot;&gt;╰───────────────────────────────────────────────────╯&lt;/font&gt;</span>

<span class="go">// Now pass that NAME CLI argument</span>
<span class="gp">$ </span>python<span class="w"> </span>main.py<span class="w"> </span>Camila

<span class="go">Hello Camila</span>

<span class="go">// Here &quot;Camila&quot; is the CLI argument</span>

<span class="go">// To pass a name with spaces for the same CLI argument, use quotes</span>
<span class="gp">$ </span>python<span class="w"> </span>main.py<span class="w"> </span><span class="s2">&quot;Camila Gutiérrez&quot;</span>

<span class="go">Hello Camila Gutiérrez</span>
</code></pre></div>

</div>
