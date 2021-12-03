<script lang="ts">
  import { getContext } from 'svelte';
  import IconX from '~icons/bx/bx-x';

  const { close } = getContext('simple-modal');
</script>

<header
  class="
    flex justify-center items-center
    p-4
    rounded-t-lg
    bg-gray-800
    text-white font-medium text-2xl
  "
>
  <slot name="header" />
</header>
<div class="p-4">
  <slot name="body" />
  <div class="flex justify-between">
    <button
      class="inline-flex items-center justify-center px-4 py-2 bg-gray-800 rounded-lg text-white font-medium"
      on:click={() => close()}
    >
      <IconX class="w-6 h-6 text-white mr-1" />
      Cancel
    </button>
    <slot name="extra-action" />
  </div>
</div>
