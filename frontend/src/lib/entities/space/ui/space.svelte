<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let name: string;
  export let free: boolean;
  export let style: string;
  export let disabled = false;

  const dispatch = createEventDispatcher();
</script>

<div
  role="button"
  tabindex="0"
  class="
    space
    p-2
    flex flex-col items-center justify-between
    rounded-lg
    {disabled ? 'cursor-default' : 'hover:scale-105 hover:shadow-lg'}
    transition-transform
    shadow-md
    before:block
    font-medium
    text-sm md:text-base
    text-white
  "
  class:free
  on:click={() => !disabled && dispatch('click')}
  {style}
>
  <span class="text-lg lg:text-3xl">{name}</span>
  <span>
    {#if free}
      Free
    {:else}
      Taken
    {/if}
  </span>
</div>

<style>
  .space {
    background: #848484;
  }

  .space.free {
    background: #80c477;
  }
</style>
