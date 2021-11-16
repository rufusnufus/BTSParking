<script lang="ts">
  import { CarDisplayCard } from '$lib/entities/car';
  import type { Car } from '$lib/shared/api';

  export let cars: Car[];
</script>

<div class="bg-white">
  <div class="max-w-2xl mx-auto py-16 px-4 sm:py-24 sm:px-6 lg:max-w-7xl lg:px-8">
    <div class="mt-6 grid grid-cols-1 gap-y-10 gap-x-6 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
      <div class="group relative">
        {#each cars as car (car.id)}
          <CarDisplayCard {car} />
        {/each}
      </div>
    </div>
  </div>
</div>
