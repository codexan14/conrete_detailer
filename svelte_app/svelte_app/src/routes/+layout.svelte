<script>
  let { children } = $props();
</script>

<svelte:head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css" />
</svelte:head>

<nav class="navbar" role="navigation" aria-label="main navigation">
  <div id="navbarBasicExample" class="navbar-menu">
    <div class="navbar-start">
      <a class="navbar-item" href="/"> Home </a>

      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link"> Beam </a>

        <div class="navbar-dropdown">
          <a class="navbar-item" href="/beam_flexural_analysis"> Flexural Analysis </a>
        </div>
      </div>

      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link"> More </a>

        <div class="navbar-dropdown">
          <a class="navbar-item"> About </a>
          <a class="navbar-item is-selected"> Jobs </a>
          <a class="navbar-item"> Contact </a>
          <hr class="navbar-divider" />
          <a class="navbar-item"> Report an issue </a>
        </div>
      </div>
    </div>
  </div>
</nav>

<!-- <nav class="navbar" role="navigation" aria-label="main navigation">
  <a href="/"> Home </a>
  <a href="/about"> About </a>
  <a href="/test">Test</a>
  <a href="/beam_analizer">Beam Section Analyzer</a>
  <a href="/diagrama_interaccion">Diagrama de interacción</a>
</nav> -->

{@render children()}

<footer class="footer">
  <div class="content has-text-centered">
    <p>
      <strong>Mini Sala App for Structural Engineers</strong> by
      <a href="https://jgthms.com">A.S.</a>. The source code is licensed
      <a href="https://opensource.org/license/mit">MIT</a>. The website content
      is licensed
      <a href="https://creativecommons.org/licenses/by-nc-sa/4.0//"
        >CC BY NC SA 4.0</a
      >
    </p>
  </div>
</footer>
