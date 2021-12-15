<script lang="ts" context="module">
  import { requireAuthorization } from '$lib/processes/auth';
  import { fetchGlobalMap } from '$lib/pages/zones';
  import { composeLoaders } from '$lib/shared/compose-loaders';

  export const load = composeLoaders(requireAuthorization, fetchGlobalMap);
</script>

<script lang="ts">
  import { ZonesPage } from '$lib/pages/zones';
  import type { ParkingLotMapDefinition } from '$lib/shared/api';

  export let mapDefinition: ParkingLotMapDefinition;
</script>

<ZonesPage {mapDefinition} />
