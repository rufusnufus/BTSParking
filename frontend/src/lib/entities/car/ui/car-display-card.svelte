<script lang="ts">
  import type { Car } from '$lib/shared/api';

  export let car: Car;
</script>

<div class="p-4 rounded-md shadow-md flex flex-col justify-between">
  <div class="flex justify-between items-center text-sm text-gray-700">
    {car.model}
    <div
      class="ml-4 px-2 py-1 text-sm font-semibold font-mono text-gray-900 border border-gray-300 rounded-md bg-gray-100"
    >
      {car.license_number}
    </div>
  </div>
  <div class="flex justify-end mt-4">
    <slot name="action" {car} />
  </div>
</div>
