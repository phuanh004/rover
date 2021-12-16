<script>

  import Dashboard from "./Dashboard.svelte";
  import RoverController from "./RoverController.svelte";

  export let menu = 1;
</script>

<nav class="bg-white shadow dark:bg-gray-800">
  <div class="container flex items-center p-6 text-gray-600 capitalize dark:text-gray-300">
    <a href="/" on:click|preventDefault={() => (menu = 1)} class="text-gray-800 dark:text-gray-200 border-b-2 border-black-500 mx-1.5 sm:mx-6">Dashboard</a>
    <a href="/" on:click|preventDefault={() => (menu = 2)} class="hover:text-gray-800 dark:hover:text-gray-200 hover:border-black-500 mx-1.5 sm:mx-6">Rover Controller</a>
  </div>
</nav>

{#if menu === 1}
  <Dashboard />
{:else if menu === 2}
  <RoverController />
{:else}
  <h1>
    Page Not Found
  </h1>
{/if}

<style lang="postcss" global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;
</style>