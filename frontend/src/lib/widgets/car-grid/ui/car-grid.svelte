<script lang="ts">
  import { session } from '$app/stores';
  import { saveNewCar } from '$lib/features/cars';
  import { CarDisplayCard, CarForm, cars } from '$lib/entities/car';

  export let withNewCarForm = false;
</script>

<div class="max-w-2xl mx-auto py-8 px-4 sm:py-16 sm:px-6 lg:max-w-7xl lg:px-8">
  <div
    class="grid gap-y-10 grid-cols-1 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-x-8"
  >
    {#each $cars as car (car.id)}
      <CarDisplayCard {car} />
    {/each}
    {#if withNewCarForm}
      <CarForm on:submit={e => saveNewCar(e, $session.token)} />
    {/if}
  </div>
</div>
