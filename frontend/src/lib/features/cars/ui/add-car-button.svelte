<script lang="ts">
  import IconPlus from '~icons/bx/bx-plus';

  export let disabled = false;
</script>

<button
  class="bg-gray-800 hover:bg-gray-700 disabled:bg-gray-400 text-white py-2 px-4 rounded font-semibold shadow-sm hover:shadow-md disabled:shadow-none disabled:cursor-not-allowed disabled:hover:shadow-none mt-3 flex items-center"
  {disabled}
  on:click
>
  <IconPlus class="w-6 h-6 mr-2" />
  Add a new car
</button>
