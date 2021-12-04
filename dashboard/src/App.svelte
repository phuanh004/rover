<script>
  import LineGraph from "./modules/LineGraph.svelte";
</script>

<main>
  <div class="container">
    <LineGraph
      label="Temperature"
      api_obj_name="temp_c"
      src="http://anhpi.local:5001/temperature"
      color="rgb(247, 85, 144)"
    />

    <LineGraph
      label="Humidity"
      api_obj_name="humidity"
      src="http://anhpi.local:5001/humidity"
      color="rgb(1, 167, 194)"
    />
  </div>
</main>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }

  .container {
    display: flex;
    flex-wrap: wrap;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>
