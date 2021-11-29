<script lang="ts" context="module">
  import { requireAuthorization } from '$lib/processes/auth';
  import { mockFetchGlobalMap } from '$lib/pages/zones';
  import { composeLoaders } from '$lib/shared/compose-loaders';

  export const load = composeLoaders(
    requireAuthorization,
    mockFetchGlobalMap,
  );
</script>

<script lang="ts">
  import { ZonesPage } from '$lib/pages/zones';
  import type { ParkingLotMapDefinition } from '$lib/shared/api';

  export let mapDefinition: ParkingLotMapDefinition;
</script>

<ZonesPage {mapDefinition} />
