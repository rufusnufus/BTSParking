<script lang="ts">
  import type { SvelteComponent } from 'svelte';

  export let icon: typeof SvelteComponent;
</script>

<div class="flex flex-col items-center justify-center text-center">
  <div
    class="bg-red-100 text-red-900 rounded-full mb-6 w-40 h-40 flex items-center justify-center"
  >
    <svelte:component this={icon} class="w-16 h-16" />
  </div>
  <div class="max-w-xs">
    <slot />
  </div>
</div>
