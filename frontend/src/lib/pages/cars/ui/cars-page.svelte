<script lang="ts">
  import { CarGrid } from '$lib/widgets/car-grid';
  import { AddCarButton } from '$lib/features/cars';
  import { cars } from '$lib/entities/car';
  import { EmptyState } from '$lib/shared/ui';
  import IconCar from '~icons/bx/bx-car';

  let addingCar = false;
</script>

<div class="flex-1 flex flex-col items-center justify-center">
  {#if $cars.length > 0 || addingCar}
    <CarGrid withNewCarForm={addingCar} />
  {:else}
    <EmptyState icon={IconCar}>
      <p>You don't have any cars yet!</p>
      <p>Create one using the button below:</p>
    </EmptyState>
  {/if}

  <div class="flex justify-center mt-2">
    <AddCarButton disabled={addingCar} on:click={() => addingCar = !addingCar} />
  </div>
</div>

