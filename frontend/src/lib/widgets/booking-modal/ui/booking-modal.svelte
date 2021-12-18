<script lang="ts">
  import { getContext } from 'svelte';
  import { page, session } from '$app/stores';
  import IconCheck from '~icons/bx/bx-check';
  import IconLeftArrowAlt from '~icons/bx/bx-left-arrow-alt';
  import IconRightArrowAlt from '~icons/bx/bx-right-arrow-alt';

  import { confirmBooking, SelectCarStep } from '$lib/features/booking';
  import { Dialog } from '$lib/shared/ui';
  import type { Car, Space } from '$lib/shared/api';
  import BankCard from './bank-card.svelte';

  export let space: Space;
  export let parkingRate = 1500;

  let currentStep: 1 | 2 | 3 = 1;
  let selectedCar: Car | undefined;
  let bookedUntil: string | undefined;

  $: canNotProceed =
    (currentStep === 1 && selectedCar === undefined) ||
    (currentStep === 2 && bookedUntil === undefined);
  $: total =
    bookedUntil === undefined
      ? undefined
      : (parkingRate *
          (new Date(bookedUntil).valueOf() - Date.now().valueOf())) /
        3600 /
        1000;

  const { close } = getContext('simple-modal');
  const zoneID = parseInt($page.params.id, 10);
</script>

<Dialog>
  <svelte:fragment slot="header">Space {space.id}</svelte:fragment>
  <div class="mb-6" slot="body">
    {#if currentStep === 1}
      <SelectCarStep bind:selectedCar />
    {:else if currentStep === 2}
      <div class="text-gray-600 mb-2">
        Until when would you like to book a space?
      </div>
      <input
        class="appearance-none rounded-md relative mt-2 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
        type="datetime-local"
        bind:value={bookedUntil}
        name="booked_until"
      />
    {:else if selectedCar !== undefined && bookedUntil !== undefined && total !== undefined}
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
        <span>{Math.floor(total)} ₽</span>
      </div>

      <div class="text-gray-600 mb-2">Enter your bank card details:</div>
      <div class="flex justify-center">
        <BankCard />
      </div>
    {/if}
  </div>
  <svelte:fragment slot="actions">
    {#if currentStep === 1}
      <div />
    {:else}
      <button
        class="inline-flex items-center justify-center px-4 py-2 bg-red-800 hover:bg-red-700 rounded-lg text-white font-medium"
        on:click={() => currentStep--}
      >
        <IconLeftArrowAlt class="w-6 text-white mr-1" />
        Back
      </button>
    {/if}
    {#if currentStep === 3}
      <button
        class="inline-flex items-center justify-center px-4 py-2 bg-green-800 hover:bg-green-700 rounded-lg text-white font-medium"
        on:click={() => {
          if (selectedCar?.id !== undefined && bookedUntil !== undefined) {
            close();
            confirmBooking(
              zoneID,
              space.id,
              selectedCar,
              new Date(bookedUntil),
              $session.token
            );
          }
        }}
      >
        <IconCheck class="w-6 h-6 text-white mr-1" />
        Confirm
      </button>
    {:else}
      <button
        class="inline-flex items-center justify-center px-4 py-2 bg-red-800 hover:bg-red-700 disabled:bg-gray-500 rounded-lg text-white font-medium"
        on:click={() => currentStep++}
        disabled={canNotProceed}
      >
        Next
        <IconRightArrowAlt class="w-6 text-white ml-1" />
      </button>
    {/if}
  </svelte:fragment>
</Dialog>

<style>
  .booking-details {
    grid-template-columns: 8em auto;
  }
</style>
