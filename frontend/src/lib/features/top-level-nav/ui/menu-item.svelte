<script lang="ts">
  export let id: string;

  export let href: string | undefined = undefined;
  export let rel: string | undefined = undefined;
</script>

<a
  class="block px-4 py-2 text-sm text-gray-700"
  class:bg-gray-100={false}
  role="menuitem"
  tabindex="-1"
  {id}
  {href}
  {rel}
>
  <slot />
</a>
