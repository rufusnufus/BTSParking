<script lang="ts">
  import IconCar from '~icons/bx/bx-car';

  import { cars, CarDisplayCard } from '$lib/entities/car';
  import { EmptyState } from '$lib/shared/ui';
  import type { Car } from '$lib/shared/api';

  import SelectCarButton from './select-car-button.svelte';

  export let selectedCar: Car | undefined;
</script>

{#if $cars.length > 0}
  <div class="text-gray-600 mb-2">Select one of your cars:</div>
  <div class="grid gap-y-10 gap-x-6 sm:grid-cols-1 lg:grid-cols-2">
    {#each $cars as car (car.id)}
      <CarDisplayCard {car}>
        <svelte:fragment slot="action">
          <SelectCarButton
            selected={car === selectedCar}
            on:click={() => (selectedCar = car)}
          />
        </svelte:fragment>
      </CarDisplayCard>
    {/each}
  </div>
{:else}
  <EmptyState icon={IconCar}>
    <p>You don't have any cars yet!</p>
    <p>
      Add your car on <a href="/cars" sveltekit:prefetch>the Cars page</a
      >.
    </p>
  </EmptyState>
{/if}

<style>
  a {
    text-decoration: underline;
    color: blue;
  }
</style>
