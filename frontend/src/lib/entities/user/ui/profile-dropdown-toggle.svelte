<script lang="ts">
  import IconUser from '~icons/bx/bx-user';

  export let id: string;
  export let dropdownShown = false;
</script>

<button
  type="button"
  class="block text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white"
  {id}
  aria-expanded={`${dropdownShown}`}
  aria-haspopup="true"
  on:click={() => dropdownShown = !dropdownShown}
>
  <span class="sr-only">Open user menu</span>
  <IconUser class="w-6 h-6 text-white" />
</button>
