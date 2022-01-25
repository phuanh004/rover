<script>
  import Camera from "./Camera.svelte";

  import Dashboard from "./Dashboard.svelte";
  import RoverController from "./RoverController.svelte";

  export let menu = 1;

  let controller_appeard = false;

  const trigger_controller = () => {
    // menu = 2;
    controller_appeard = !controller_appeard;
  };
</script>

<nav class="bg-white shadow dark:bg-gray-800">
  <div
    class="container flex items-center p-6 text-gray-600 capitalize dark:text-gray-300"
  >
    <a
      href="/"
      on:click|preventDefault={() => (menu = 1)}
      class="nav-inactive"
      class:nav-active={menu === 1}>Dashboard</a
    >
    <a
      href="/"
      on:click|preventDefault={() => (menu = 2)}
      class="nav-inactive"
      class:nav-active={menu === 2}>Spectra</a
    >
    <a
      href="/"
      on:click|preventDefault={trigger_controller}
      class="nav-inactive">Rover Controller</a
    >
  </div>
</nav>

{#if menu === 1}
  <Dashboard />
{:else if menu === 2}
  <Camera />
  <!-- <RoverController /> -->
{:else}
  <h1>Page Not Found</h1>
{/if}

{#if controller_appeard}
  <div
    id="defaultModal"
    aria-hidden="true"
    class="overflow-y-auto overflow-x-hidden fixed right-0 left-0 top-4 z-50 justify-center items-center h-modal md:h-full md:inset-0"
  >
    <div class="relative top-32 mx-auto px-4 w-full max-w-2xl h-full md:h-auto">
      <!-- Modal content -->
      <div class="relative bg-white rounded-lg shadow dark:bg-gray-800">
        <!-- Modal header -->
        <div
          class="flex justify-between items-start p-5 rounded-t border-b dark:border-gray-600"
        >
          <h3
            class="text-xl font-semibold text-gray-900 lg:text-2xl dark:text-white"
          >
            Rover Controller Instruction
          </h3>
          <button
            type="button"
            class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white"
            on:click={trigger_controller}
          >
            <svg
              class="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 20 20"
              xmlns="http://www.w3.org/2000/svg"
              ><path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              /></svg
            >
          </button>
        </div>
        <!-- Modal body -->
        <div class="p-6 space-y-6">
          <p class="text-base leading-relaxed text-gray-500 dark:text-gray-400">
            <RoverController />
          </p>
        </div>
      </div>
    </div>
  </div>
{/if}

<style lang="postcss" global>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  .nav-active {
    @apply text-gray-800 dark:text-gray-200 border-b-2 mx-1.5 sm:mx-6;
  }

  .nav-inactive {
    @apply hover:text-gray-800 dark:hover:text-gray-200 mx-1.5 sm:mx-6;
  }
</style>
