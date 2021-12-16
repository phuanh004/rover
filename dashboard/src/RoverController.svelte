<script>
    import {onMount} from "svelte";

    const HOST_NAME = PI_HOST_NAME;
    const PORT = PI_PORT;

    let key;
    let keyCode;
    $:msg = "";

    let ws = null;

    function handleKeydown(event) {
        key = event.key;
        keyCode = event.keyCode;

        switch (event.key) {
            case "ArrowUp":
                msg = "Going straight"
                ws?.send("fwd")
                break
            
            case "ArrowLeft":
                msg = "Turning Left"
                ws?.send("left")
                break
        }
    }

    onMount(async () => {
        ws = new WebSocket(`ws://${HOST_NAME}:${PORT}/rover/move/forward`)
    });
</script>

<svelte:window on:keydown={handleKeydown}/>

<div style="text-align: center">
    {#if key}
        <kbd>{key === ' ' ? 'Space' : msg}</kbd>
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