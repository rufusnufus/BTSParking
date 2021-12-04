<script lang="ts" context="module">
  export interface CarFormEventMap {
    submit: {
      model: string;
      license_number: string;
    };
  }
</script>

<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import IconCheck from '~icons/bx/bx-check';

  let model = '';
  let license_number = '';

  const dispatch = createEventDispatcher<CarFormEventMap>();
</script>

<form
  on:submit|preventDefault={() => dispatch('submit', { model, license_number })}
  class="p-4 rounded-md shadow-md flex flex-col justify-between"
>
  <div class="flex justify-between items-center text-sm text-gray-700">
    <input
      id="model"
      name="model"
      required
      class="appearance-none rounded-md relative block w-full mt-2 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
      placeholder="Lada Vesta"
      bind:value={model}
    />
    <input
      id="license_number"
      name="license_number"
      required
      class="ml-4 w-16 text-center appearance-none rounded-md relative block mt-2 px-2 py-1 border border-gray-300 bg-gray-100 placeholder-gray-400 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 font-semibold font-mono focus:z-10 text-sm"
      placeholder="A000AA"
      bind:value={license_number}
    />
  </div>
  <div class="flex justify-end mt-4">
    <button
      class="flex items-center bg-gray-800 hover:bg-gray-700 shadow hover:shadow-lg rounded-md px-4 py-2 text-white font-medium"
    >
      <IconCheck class="w-5 h-5 mr-2" />
      Save
    </button>
  </div>
</form>
