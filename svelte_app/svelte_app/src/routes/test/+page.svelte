<script>
	let base = 0;
	let altura = 0;
	let resultado = null;
	let cargando = false;

	async function calcularProducto() {
		cargando = true;
		try {
			const res = await fetch('http://127.0.0.1:8000/producto', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ base, altura })
			});
			const data = await res.json();
			resultado = data.resultado;
		} catch (e) {
			console.error('Error al enviar datos:', e);
			resultado = 'Error';
		} finally {
			cargando = false;
		}
	}
</script>

<div>
	<label>
		Base:
        <input type="number" bind:value={base} />
	</label>
	<br />
	<label>
		Altura:
		<input type="number" bind:value={altura} />
	</label>
	<br />
	<button on:click={calcularProducto} disabled={cargando}>
		{cargando ? 'Calculando...' : 'Calcular producto'}
	</button>
</div>

{#if resultado !== null}
	<p>Resultado: {resultado}</p>
{/if}