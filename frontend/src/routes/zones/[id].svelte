<script lang="ts" context="module">
  import { requireAuthorization } from '$lib/processes/auth';
  import { mockFetchZoneMap as fetchZoneMap } from '$lib/pages/zone';
  import { fetchCars } from '$lib/pages/cars';
  import { composeLoaders } from '$lib/shared/compose-loaders';

  export const load = composeLoaders(
    requireAuthorization,
    fetchCars,
    fetchZoneMap
  );
</script>

<script lang="ts">
  import { ZonePage } from '$lib/pages/zone';
  import { cars as carStore } from '$lib/entities/car';
  import type { Car, ZoneMapDefinition } from '$lib/shared/api';

  export let cars: Car[];
  $: carStore.set(cars);

  export let mapDefinition: ZoneMapDefinition;
</script>

<ZonePage {mapDefinition} />
