<script>
    let { children } = $props()
</script>

<nav>
    <a href="/"> Home </a>
    <a href="/about"> About </a>
    <a href="/test">Test</a>
    <a href="/diagrama_interaccion">Diagrama de interacción</a>
</nav>

<style>
/* Reset & base */
nav {}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-weight: 1000;
  font-family: Arial, Helvetica, sans-serif;
  /* background-color: #333; */
  padding: 2em;
  border-radius: 2em;
  text-align: center;

}

html, body{
  height: 100%;
  background: #f9f9f9;
  color: #333;
  line-height: 1.5;
  font-family: 'Courier New', Courier, monospace;
}

a {
  color: inherit;
  text-decoration: none;
}

button {
  all: unset;
  cursor: pointer;
}

/* Layout helpers */
.container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 0 1rem;
}

/* Minimal UI */
input, button, select, textarea {
  font: inherit;
  padding: 0.5rem 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
  background: white;
  transition: border-color 0.2s;
}

input:focus, textarea:focus, select:focus {
  border-color: #0077ff;
  outline: none;
}

button {
  background: #0077ff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  transition: background 0.2s;
}

button:hover {
  background: #005fcc;
}

</style>

{@render children()}