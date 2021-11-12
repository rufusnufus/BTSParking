<script lang="ts" context="module">
  import { requireAuthorization } from '$lib/processes/auth';
  import { fetchCars } from '$lib/pages/cars';
  import { composeLoaders } from '$lib/shared/compose-loaders';

  export const load = composeLoaders(
    requireAuthorization,
    fetchCars,
  );
</script>

<script lang="ts">
  import { CarsPage } from '$lib/pages/cars';
  import type { Car } from '$lib/shared/api';

  export let cars: Car[];
</script>

<CarsPage {cars} />
