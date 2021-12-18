<script lang="ts">
  export let id: string;

  export let href: string | undefined = undefined;
  export let rel: string | undefined = undefined;
  export let active: boolean = false;
</script>

<a
  class="block px-4 py-2 text-sm text-gray-700"
  class:bg-gray-100={active}
  role="menuitem"
  tabindex="-1"
  {id}
  {href}
  {rel}
  on:click
>
  <slot />
</a>
