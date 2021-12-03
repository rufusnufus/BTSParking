<script lang="ts">
  import { getContext } from 'svelte';
  import IconCar from '~icons/bx/bx-car';
  import IconCheck from '~icons/bx/bx-check';

  import { confirmBooking } from '$lib/features/booking';
  import { cars, CarDisplayCard } from '$lib/entities/car';
  import { EmptyState, Dialog } from '$lib/shared/ui';
  import type { Car } from '$lib/shared/api';
  import SelectCarButton from './select-car-button.svelte';
  import BankCard from './bank-card.svelte';

  let selectedCar: Car | undefined;
  let bookedUntil: string | undefined;

  const { close } = getContext('simple-modal');
</script>

<Dialog>
  <svelte:fragment slot="header">
    A3
  </svelte:fragment>
  <div class="mb-6" slot="body">
    {#if selectedCar === undefined}
      {#if $cars.length > 0}
        <div class="text-gray-600 mb-2">Select one of your cars:</div>
        <div class="grid gap-y-10 gap-x-6 sm:grid-cols-1 lg:grid-cols-2">
          {#each $cars as car (car.id)}
            <CarDisplayCard {car}>
              <svelte:fragment slot="action">
                <SelectCarButton
                  {car}
                  selected={car === selectedCar}
                  on:click={() => selectedCar = car}
                />
              </svelte:fragment>
            </CarDisplayCard>
          {/each}
        </div>
      {:else}
        <EmptyState icon={IconCar}>
          <p>You don't have any cars yet!</p>
          <p>Add your car on <a href="/cars" sveltekit:prefetch>the Cars page</a>.</p>
        </EmptyState>
      {/if}
    {:else if bookedUntil === undefined}
      <div class="text-gray-600 mb-2">Until when would you like to book a space?</div>
      <input
        class="appearance-none rounded-md relative mt-2 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
        type="datetime-local"
        bind:value={bookedUntil}
        name="booked_until"
      />
    {:else}
      <div class="text-gray-600 mb-2">Confirm your booking details:</div>
      <div class="booking-details grid mb-4">
        <span class="font-semibold">Car:</span>
        <div class="flex align-center">
          {selectedCar?.model}
          <div
            class="ml-4 px-2 py-1 text-sm font-semibold font-mono text-gray-900 border border-gray-300 rounded-md bg-gray-100"
          >
            {selectedCar?.license_number}
          </div>
        </div>
        <span class="font-semibold">Booked until:</span>
        <span>{new Date(bookedUntil).toLocaleString()}</span>
        <span class="font-semibold">Total:</span>
        <span>9999$</span>
      </div>

      <div class="text-gray-600 mb-2">Enter your bank card details:</div>
      <div class="flex justify-center">
        <BankCard />
      </div>
    {/if}
  </div>
  <svelte:fragment slot="extra-action">
    {#if selectedCar !== undefined && bookedUntil !== undefined}
      <button
        class="inline-flex items-center justify-center px-4 py-2 bg-green-800 hover:bg-green-700 rounded-lg text-white font-medium"
        on:click={() => {
          if (selectedCar?.id !== undefined && bookedUntil !== undefined) {
            close();
            confirmBooking(selectedCar.id, new Date(bookedUntil));
          }
        }}
      >
        <IconCheck class="w-6 h-6 text-white mr-1" />
        Confirm
      </button>
    {/if}
  </svelte:fragment>
</Dialog>

<style>
  a {
    text-decoration: underline;
    color: blue;
  }

  .booking-details {
    grid-template-columns: 8em auto;
  }
</style>
