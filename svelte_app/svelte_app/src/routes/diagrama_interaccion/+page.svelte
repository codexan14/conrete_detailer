<script lang="ts">
	let base = 300;
	let height = 600;
	let fc = 28;
    let fy = 420; 
    let corner_bar_diameter = 25;
    let inner_bar_diameter = 19;
    let horizontal_rebar_number = 2;
    let vertical_rebar_number = 2;
    let rebar_areas: number[] = []
    let rebar_positions: number[] = []
    // $: rebar_position = [2, 3, 4];
    let Es = 200000;
    let n = 10;

    async function get_diagrama_interaccion() {
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

    function bar_area(diameter: number): number{
        return (1/4) * Math.PI * diameter**2;
    }

    function get_rebar_areas(){
        let rebar_areas = Array.from({ length: vertical_rebar_number + 2 }, (_, i) => 2*bar_area(inner_bar_diameter));
        rebar_areas[0] = 2*bar_area(corner_bar_diameter) + horizontal_rebar_number*bar_area(inner_bar_diameter);
        rebar_areas[vertical_rebar_number + 1] = 2*bar_area(corner_bar_diameter) + horizontal_rebar_number*bar_area(inner_bar_diameter);
        
        return rebar_areas;
    }

    function get_rebar_positions(){ 
        let initial_position: number = 40 + 10 + 12.5 
        let final_position: number = height - 40 - 10 -12.5 
        let spacing: number = (final_position - initial_position)/(vertical_rebar_number + 1)
        
        let rebar_positions = Array.from({ length: vertical_rebar_number + 2 }, (_, i) => 40 + 10 + 12.5 + spacing*i);
        
        return rebar_positions;
    }
	// async function calcularProducto() {
	// 	cargando = true;
	// 	try {
	// 		const res = await fetch('http://127.0.0.1:8000/producto', {
	// 			method: 'POST',
	// 			headers: {
	// 				'Content-Type': 'application/json',
	// 			},
	// 			body: JSON.stringify({ base, altura })
	// 		});
	// 		const data = await res.json();
	// 		resultado = data.resultado;
	// 	} catch (e) {
	// 		console.error('Error al enviar datos:', e);
	// 		resultado = 'Error';
	// 	} finally {
	// 		cargando = false;
	// 	}
	// }
</script>

<div>
	<label>
		Base:
        <input type="number" bind:value={base} />
	</label>
	<br />

	<label>
		Height:
		<input type="number" bind:value={height} />
	</label>
    <br />

    <label>
		Concrete Compression Resistance:
		<input type="number" bind:value={fc} />
	</label>
    <br />

    <label>
		Steel Yield Stress:
		<input type="number" bind:value={fy} />
	</label>
    <br />

    <label>
		Corner Rebar Diameter:
		<input type="number" bind:value={corner_bar_diameter} on:change={() => rebar_areas = get_rebar_areas()} />
	</label>
    <br />

    <label>
		Inner Rebar Diameter:
		<input type="number" bind:value={inner_bar_diameter} on:change={() => rebar_areas = get_rebar_areas()} />
	</label>
    <br />

    <label>
        Number of Horizontal Rebars Between Corner Bars (One Side):
		<input type="number" bind:value={horizontal_rebar_number} on:change={() => rebar_areas = get_rebar_areas()} />
	</label>
    <br />

    <label>
        Number of Vertical Rebars Between Corner Bars (One Side):
		<input type="number" bind:value={vertical_rebar_number} on:change={() => {rebar_areas = get_rebar_areas(); rebar_positions = get_rebar_positions()}} />
	</label>

    <br>

    <button on:click={() => {rebar_areas = get_rebar_areas(); rebar_positions = get_rebar_positions()}}>
        kk
    </button>

    {#each rebar_areas as bar, i }
        <br />{Math.round(bar*100)/100},  {Math.round(rebar_positions[i]*100)/100}
    {/each}
    
</div>


<!-- {#if resultado !== null}
	<p>Resultado: {resultado}</p>
{/if} -->