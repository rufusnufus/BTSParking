<script lang="ts">
  import type { Statistics } from '$lib/shared/api';

  export let statisticsObject: Statistics;
  $: car = statisticsObject.booking.occupying_car;
  $: totalTime =
    statisticsObject.booking.booked_from === undefined
      ? undefined
      : (new Date(statisticsObject.booking.booked_until).valueOf() -
          new Date(statisticsObject.booking.booked_from).valueOf()) /
        3600 /
        1000;

  function s(amount: number) {
    return amount !== 1 ? 's' : '';
  }
</script>

<div class="rounded-md shadow-md flex flex-col justify-between">
  {#if statisticsObject.booking.booked_from !== undefined}
    <div class="py-1 text-center bg-red-900 text-white font-semibold rounded-t">
      {new Date(statisticsObject.booking.booked_from).toLocaleDateString()}
    </div>
  {/if}
  <div class="p-4 booking-details grid mb-4">
    <span class="font-semibold">Car:</span>
    <div class="flex align-center">
      {car.model}
      <div
        class="ml-4 px-2 py-1 text-sm font-semibold font-mono text-gray-900 border border-gray-300 rounded-md bg-gray-100"
      >
        {car.license_number}
      </div>
    </div>

    {#if totalTime !== undefined}
      <span class="font-semibold">Booking time:</span>
      <span>
        {Math.floor(totalTime)} hour{s(Math.floor(totalTime))}
      </span>

      <span class="font-semibold">Total:</span>
      <span>{Math.floor(totalTime * statisticsObject.hourly_rate * 100)} ₽</span
      >
    {/if}
  </div>
</div>

<style>
  .booking-details {
    grid-template-columns: 8em auto;
  }
</style>
