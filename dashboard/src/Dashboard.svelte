<script>
    import LineGraph from "./modules/LineGraph.svelte";

    const HOST_NAME = PI_HOST_NAME;
    const PORT = PI_PORT;
</script>

<main>
    <div class="container mx-auto">
        <div class='row'>
            <div class='column'>
                <LineGraph
                    label="Temperature (°C)"
                    api_obj_name="temperature_c"
                    src="ws://{HOST_NAME}:{PORT}/temperature"
                    color="rgb(247,85,144)"
                />
            </div>
            <div class='column'>
                <LineGraph
                    label="Humidity"
                    api_obj_name="humidity"
                    src="ws://{HOST_NAME}:{PORT}/humidity"
                    color="rgb(1,167,194)"
                />
            </div>
        </div>
        <div class="row">
            <div class='column'>
                <LineGraph
                    label="Radiation"
                    api_obj_name="radiation"
                    src="ws://{HOST_NAME}:{PORT}/radiation"
                    color="rgb(231,192,96)"
                />
            </div>
            <div class='column'></div>
        </div>
    </div>
</main>

<style>
    .row {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        width: 100%;
        gap: 2em;
        margin-bottom: 2em;
    }

    .column {
        display: flex;
        flex-direction: column;
        flex: 1;
    }
</style>
