<script lang="ts">
  import { getContext } from 'svelte';
  import IconX from '~icons/bx/bx-x';

  import { CarDisplayCard } from '$lib/entities/car';
  import type { Car } from '$lib/shared/api';

  const cars = <Car[]>[
    {
      id: 1,
      model: 'Volkswagen Touareg',
      license_number: 'A001BC',
    }
  ];

  const { close } = getContext('simple-modal');
</script>

<header class="flex justify-center items-center p-4 rounded-t-lg bg-gray-800 text-white font-medium text-2xl">
  A3
</header>
<div class="p-4">
  <div class="text-center text-lg text-gray-600">Select car</div>
  <div class="flex py-8">
    {#each cars as car (car.id)}
      <CarDisplayCard {car} />
    {/each}
  </div>
  <div>
    <button
      class="inline-flex items-center justify-center px-4 py-2 bg-gray-800 rounded-lg text-white font-medium"
      on:click={() => close()}
    >
      <IconX class="w-6 h-6 text-white mr-1" />
      Cancel
    </button>
  </div>
</div>
