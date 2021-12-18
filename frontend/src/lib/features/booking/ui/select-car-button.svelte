<script lang="ts">
  import IconCheck from '~icons/bx/bx-check';

  export let selected: boolean;
</script>

<button
  on:click
  class="
    flex items-center
    border border-green-700 hover:border-green-600
    rounded-md
    px-4 py-2
    {selected
    ? 'bg-green-700 hover:bg-green-600 text-white border-0 shadow hover:shadow-lg'
    : 'text-green-700 hover:text-green-600 hover:bg-green-50'}
    font-medium"
>
  <IconCheck class="w-5 h-5 mr-2" />
  {#if selected}
    Selected
  {:else}
    Select
  {/if}
</button>
