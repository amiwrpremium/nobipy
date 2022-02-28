<h1>Nobitex SDK</h1>
<p>
    This is a simple SDK for Nobitex.
</p>

<h1>Installation</h1>
<code class="language-bash">
    pip3 install nobipy
</code>


<h1>Usage</h1>

<h3>Import package</h3>
<pre>
<code class="language-python">from nobipy import Nobitex
from nobipy import get_token</code>
</pre>

<h3>Get token</h3>
<pre><code class="language-python">token = get_token('username', 'password')</code></pre>

<h3>Create a new client</h3>
<pre>
<code class="language-python">nobitex = Nobitex(token='token')</code>
</pre>

<p>Note that token is optional. You can set it later using:</p>
<pre><code class="language-python">nobitex.set_token('token')</code></pre>

