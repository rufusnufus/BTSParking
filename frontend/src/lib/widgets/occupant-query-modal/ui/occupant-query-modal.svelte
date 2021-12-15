<script lang="ts">
  import { Dialog } from '$lib/shared/ui';
  import type { Space } from '$lib/shared/api';

  export let space: Space;
</script>

<Dialog>
  <svelte:fragment slot="header">Space {space.id}</svelte:fragment>
  <div class="mb-6" slot="body">
    {#if space.booking !== undefined && space.booking.booked_from !== undefined}
      <div class="booking-details grid mb-4">
        <span class="font-semibold">Car:</span>
        <div class="flex align-center">
          {space.booking.occupying_car.model}
          <div
            class="ml-4 px-2 py-1 text-sm font-semibold font-mono text-gray-900 border border-gray-300 rounded-md bg-gray-100"
          >
            {space.booking.occupying_car?.license_number}
          </div>
        </div>
        <span class="font-semibold">Booked from:</span>
        <span>{new Date(space.booking.booked_from).toLocaleString()}</span>
        <span class="font-semibold">Booked until:</span>
        <span>{new Date(space.booking.booked_until).toLocaleString()}</span>
      </div>
    {/if}
  </div>
</Dialog>

<style>
  .booking-details {
    grid-template-columns: 8em auto;
  }
</style>
