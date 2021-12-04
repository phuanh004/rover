<script>
  import { onMount } from "svelte";
  import Line from "svelte-chartjs/src/Line.svelte";

  export let src;
  export let label;
  export let api_obj_name;
  export let color;

  let labels = [];
  let data = {
    labels: labels,
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

  onMount(async () => {
    async function fetchData() {
      src,
        {
          mode: "cors",
        };
      const req = await fetch(src, { mode: "cors" });
      const res = await req.json();

      addPointTempToGraph(res[api_obj_name]);
    }

    const interval = setInterval(fetchData, 1000);
    fetchData();

    return () => clearInterval(interval);
  });

  const addPointTempToGraph = (point) => {
    data.labels = [...data.labels, ""];
    data.datasets[0].data = [...data.datasets[0].data, point];
  };
</script>

<div class="graph">
  <Line {data} />
</div>

<style scoped>
  .graph {
    flex: 50%;
    width: 100%;
  }
</style>
