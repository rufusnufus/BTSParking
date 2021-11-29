<script lang="ts" context="module">
  import { mockFetchGlobalMap } from '$lib/pages/zones';

  export const load = mockFetchGlobalMap;
</script>

<script lang="ts">
  import { ZonesPage } from '$lib/pages/zones';
  import type { ParkingLotMapDefinition } from '$lib/shared/api';

  export let mapDefinition: ParkingLotMapDefinition;
</script>

<ZonesPage {mapDefinition} />
