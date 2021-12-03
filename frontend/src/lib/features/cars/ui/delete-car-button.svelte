<script lang="ts">
  import { session } from '$app/stores';
  import IconTrash from '~icons/bx/bx-trash';
  import { deleteCar } from '../model/delete-car';
  import type { Car } from '$lib/shared/api';

  export let car: Car;
</script>

<button
  on:click={() => car.id !== undefined && deleteCar(car.id, $session.token)}
  class="flex items-center bg-red-700 hover:bg-red-600 shadow hover:shadow-lg rounded-md px-4 py-2 text-white font-medium"
>
  <IconTrash class="w-5 h-5 mr-2" />
  Delete
</button>
