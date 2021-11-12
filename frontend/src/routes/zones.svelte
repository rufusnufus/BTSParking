<script lang="ts" context="module">
  import { fetchZones } from '$lib/pages/zones';

  export const load = fetchZones;
</script>

<script lang="ts">
  import { ZonesPage } from '$lib/pages/zones';
  import type { Zone } from '$lib/shared/api';

  export let zones: Zone[];
</script>

<ZonesPage {zones} />
