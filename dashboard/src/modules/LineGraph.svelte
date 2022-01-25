<script>
  import { onMount } from "svelte";
  import Line from "svelte-chartjs/src/Line.svelte";

  export let src;
  export let label;
  export let api_obj_name;
  export let color;

  // Data for the graph
  let data = {
    labels: [],
    datasets: [
      {
        label: label,
        data: [],
        fill: false,
        borderColor: color,
        tension: 0.1,
      },
    ],
  };

  // Interactive values
  $: average = getDataAverage(data);
  const getDataAverage = (data) => {
    let avg = 0;
    if (data.datasets[0].data.length > 0) {
      avg =
        data.datasets[0].data.reduce((a, b) => a + b) /
        data.datasets[0].data.length;
    }

    return Math.round(avg);
  };

  // Web socket running
  function startWebsocket() {
    const ws = new WebSocket(src);

    ws.onmessage = function (event) {
      let res = JSON.parse(event.data);
      let data_point = res.result ?? null;

      if (data_point) {
        addPointTempToGraph(data_point[api_obj_name]);
      }
    };

    ws.onclose = function () {
      setTimeout(startWebsocket, 5000);
    };
  }

  onMount(async () => {
    startWebsocket();
  });

  const addPointTempToGraph = (point) => {
    data.labels = [...data.labels, ""];
    data.datasets[0].data = [...data.datasets[0].data, point];
  };
</script>

<div class="graph">
  <Line {data} />
  <div class="info">
    <p class="average text-center">Avg: {average ?? 0}</p>
  </div>
</div>

<style scoped>
  .graph {
    width: 100%;
    flex: 1;
  }
</style>
