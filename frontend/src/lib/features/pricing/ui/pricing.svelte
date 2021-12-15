<script lang="ts">
  import IconPlus from '~icons/bx/bx-plus';
  import IconMinus from '~icons/bx/bx-minus';

  let amountOfPlaces = 50;
  const placesStep = 50;
  $: total = amountOfPlaces * 300;
</script>

<div class="mt-4 p-4 md:mt-10 rounded bg-white shadow-sm text-black text-center md:text-left">
  <div class="font-semibold">
    Find out the price for your business
  </div>

  <div class="flex flex-col md:flex-row items-center mt-2">
    <div class="mr-4 w-48 md:w-80">
      How many parking places does your business need?
    </div>

    <div class="flex items-center mt-4">
      <button
        on:click={() => amountOfPlaces -= placesStep}
        disabled={amountOfPlaces <= placesStep}
        class="
          p-2
          bg-red-800 hover:bg-red-700
          disabled:bg-gray-500
          rounded
          text-white
        "
      >
        <IconMinus class="w-6" />
      </button>
      <div class="text-xl font-semibold mx-4">{amountOfPlaces}</div>
      <button
        on:click={() => amountOfPlaces += placesStep}
        class="p-2 bg-red-800 rounded hover:bg-red-700 text-white"
      >
        <IconPlus class="w-6" />
      </button>
    </div>
  </div>

  <div class="mt-4">Total price: {total} ₽/month</div>
</div>
