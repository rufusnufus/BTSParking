<script lang="ts">
  import { getContext } from 'svelte';
  import IconX from '~icons/bx/bx-x';

  const { close } = getContext('simple-modal');
</script>

<header
  class="
    grid justify-center items-center
    p-4
    rounded-t-lg
    bg-gray-800
    text-white
  "
>
  <div />
  <div class="text-2xl font-medium text-center">
    <slot name="header" />
  </div>
  <button
    class="inline-flex items-center justify-center px-4 py-2 rounded-lg font-medium hover:bg-white hover:bg-opacity-10"
    on:click={() => close()}
  >
    <IconX class="w-6 h-6 text-white mr-1" />
    Close
  </button>
</header>
<div class="p-4">
  <slot name="body" />
  <div class="flex justify-between">
    <slot name="actions" />
  </div>
</div>

<style>
  header {
    grid-template-columns: 1fr 4fr 1fr;
  }
</style>
