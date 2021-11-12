<script lang="ts">
  import User from '@svicons/boxicons-regular/user.svelte';

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
  <User class="w-6 text-white" />
</button>
