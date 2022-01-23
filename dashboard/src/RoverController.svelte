<script>
  import { onMount } from "svelte";

  const HOST_NAME = PI_HOST_NAME;
  const PORT = PI_PORT;

  $: msg = "";

  let ws_fwd,
    ws_bwd = null;
  let key;

  function handleKeydown(event) {
    key = event.key;

    switch (event.key) {
      case "ArrowUp":
        msg = "Going straight";
        ws_fwd?.send("fwd");
        break;

      case "ArrowLeft":
        msg = "Turning Left";
        ws_fwd?.send("left");
        break;

      case "ArrowRight":
        msg = "Turning Right";
        ws_fwd?.send("right");
        break;

      case "ArrowDown":
        msg = "Backing Up";
        ws_bwd?.send("bwd");
        break;

      case "s":
        msg = "Stopping";
        ws_bwd?.send("stop");
        break;
    }
  }

  onMount(async () => {
    ws_fwd = new WebSocket(`ws://${HOST_NAME}:${PORT}/rover/move/forward`);
    ws_bwd = new WebSocket(`ws://${HOST_NAME}:${PORT}/rover/move/backward`);
  });
</script>

<svelte:window on:keydown={handleKeydown} />

<div>
  <div class="text-center text-3xl font-bold p-2">
    {#if key}
      <kbd>{key === " " ? "Space" : msg}</kbd>
    {/if}
  </div>
  <p><span class="font-bold">Arrows keys</span>: rover directions</p>
  <p><span class="font-bold">S</span>: stop</p>
</div>
