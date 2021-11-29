<script lang="ts" context="module">
  import { mockFetchZoneMap } from '$lib/pages/zone';

  export const load = mockFetchZoneMap;
</script>

<script lang="ts">
  import { ZonePage } from '$lib/pages/zone';
  import type { ZoneMapDefinition } from '$lib/shared/api';

  export let mapDefinition: ZoneMapDefinition;
</script>

<ZonePage {mapDefinition} />
