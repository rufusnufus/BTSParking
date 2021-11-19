<script lang="ts" context="module">
  import { mockFetchGlobalMap } from '$lib/pages/zones';

  export const load = mockFetchGlobalMap;
</script>

<script lang="ts">
  import { ZonesPage } from '$lib/pages/zones';
  import type { MapDefinition } from '$lib/shared/types';

  export let mapDefinition: MapDefinition;
</script>

<ZonesPage {mapDefinition} />
