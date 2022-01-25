<script>
  import { onMount } from "svelte";

  const HOST_NAME = PI_HOST_NAME;
  const PORT = PI_PORT;

  let ws = null;
  let res_status;

  const capture = () => {
    ws?.send("capture");
  };

  const delete_capture = () => {
    ws?.send("delete");
    res_status = null;
  };

  onMount(async () => {
    ws = new WebSocket(`ws://${HOST_NAME}:${PORT}/rover/camera`);

    ws.onmessage = function (event) {
      let res = JSON.parse(event.data);
      res_status = res?.result?.status ?? null;
    };
  });
</script>

<div class="container mx-auto pt-5 flex flex-row flex-wrap">
  <div class="instruction basis-6/12 ">
    <h3
      class="mb-3 text-xl font-semibold text-gray-900 lg:text-2xl dark:text-white"
    >
      Spectra Instruction
    </h3>
    <p>1. Turn on legacy camera in setting if needed</p>
    <p>2. Disable The Red LED On The Pi Camera</p>
  </div>
  <div class="actions basis-6/12">
    <h3
      class="mb-3 text-xl font-semibold text-gray-900 lg:text-2xl dark:text-white"
    >
      Actions
    </h3>
    <button
      type="button"
      on:click={capture}
      class="text-gray-900 bg-white hover:bg-gray-100 border border-gray-200 focus:ring-4 focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-600 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:bg-gray-700 mr-2 mb-2"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
        />
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
        />
      </svg>
      <span class="ml-1">Capture</span>
    </button>
    <button
      type="button"
      on:click={delete_capture}
      class="text-gray-900 bg-white hover:bg-gray-100 border border-gray-200 focus:ring-4 focus:ring-gray-100 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-gray-600 dark:bg-gray-800 dark:border-gray-700 dark:text-white dark:hover:bg-gray-700 mr-2 mb-2"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
        />
      </svg>
      <span class="ml-1">Delete Capture</span>
    </button>
  </div>
  {#if res_status == 200}
    <div class="basis-12/12">
      <img
        width="100%"
        class="object-cover mt-2"
        src={`http://${HOST_NAME}:${PORT}/static/images/capture.jpg`}
        alt=""
      />
    </div>
  {/if}
</div>
