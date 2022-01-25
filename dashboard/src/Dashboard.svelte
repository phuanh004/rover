<script>
  import LineGraph from "./modules/LineGraph.svelte";

  const HOST_NAME = PI_HOST_NAME;
  const PORT = PI_PORT;
</script>

<main>
  <div class="container mx-auto grid grid-cols-1 md:grid-cols-2 gap-4 pt-5">
    <LineGraph
      label="Temperature (°C)"
      api_obj_name="temperature_c"
      src="ws://{HOST_NAME}:{PORT}/temperature"
      color="rgb(247,85,144)"
    />
    <LineGraph
      label="Humidity (%)"
      api_obj_name="humidity"
      src="ws://{HOST_NAME}:{PORT}/humidity"
      color="rgb(1,167,194)"
    />

    <LineGraph
      label="Radiation (cpm)"
      api_obj_name="radiation"
      src="ws://{HOST_NAME}:{PORT}/radiation"
      color="rgb(231,192,96)"
    />
  </div>
</main>
