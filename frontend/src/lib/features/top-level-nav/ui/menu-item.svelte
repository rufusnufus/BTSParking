<script lang="ts">
  export let id: string;

  export let href: string | undefined = undefined;
  export let action: (() => void) | undefined = undefined;
</script>

{#if href !== undefined}
  <a
    class="block px-4 py-2 text-sm text-gray-700"
    class:bg-gray-100={false}
    role="menuitem"
    tabindex="-1"
    {id}
    {href}
  >
    <slot />
  </a>
{:else}
  <span
    class="block px-4 py-2 text-sm text-gray-700 cursor-pointer"
    role="menuitem"
    tabindex="-1"
    {id}
    on:click={action}
  >
    <slot />
  </span>
{/if}
