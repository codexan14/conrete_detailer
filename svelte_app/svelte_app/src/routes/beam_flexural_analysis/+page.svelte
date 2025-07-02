<script lang="ts">
	
    let variable_names = [
        'Base',
        'Steel area', 
        'Rebar centroid', 
        'Concrete compression strength', 
        'Steel yield stress'];

	let variable_values = Array(variable_names.length).fill(100)
    variable_values[0] = 300


    let processing = false
    let result = null

    async function submit() {
		
		processing = true;
		try {
			const res = await fetch('http://127.0.0.1:8000/get_reduced_nominal_moment_beam_no_compression_reinforcement', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ 
                    "base": variable_values[0], 
                    "steel_area": variable_values[1],
                    "rebar_centroid": variable_values[2],
                    "concrete_compression_strength": variable_values[3],
                    'steel_yield_stress': variable_values[4]})
			});
			const data = await res.json();
			result = data.result;
		} catch (e) {
			console.error('Error al enviar datos:', e);
			result = 'Error';
		} finally {
			processing = false;
		}
	}
</script>

<h1 class="title">Beam Flexural Analysis</h1>

<div class="columns is-1-mobile is-0-tablet is-3-desktop is-8-widescreen is-2-fullhd">
  <div class="column" >

		<h2 class="title">Inputs</h2>
		{#each variable_names as name, i}
			{name} : <input class="input" type="number" bind:value={variable_values[i]} /> <br />
		{/each}

		<button class="button is-primary" on:click={submit} disabled = {processing}> Submit </button> <br>

		<p>{processing ? "Calculando" : "Resultado: "}</p>

		{#if result != null}
			<strong>{result} N-mm </strong>
		{/if}
	
  </div>


  <div class="column">Second column</div>
</div>


