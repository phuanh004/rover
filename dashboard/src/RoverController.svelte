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
        msg = "Stoping";
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

<div style="text-align: center">
  {#if key}
    <kbd>{key === " " ? "Space" : msg}</kbd>
  {:else}
    <p>Focus this window and press any key</p>
  {/if}
</div>

<style>
  div {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
  }

  kbd {
    border-radius: 4px;
    font-size: 4em;
    padding: 0.2em 0.5em;
  }
</style>
