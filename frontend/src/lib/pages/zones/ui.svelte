<script lang="ts">
  import { ZoneMap } from '$lib/widgets/zone-map';
  import type { Zone } from '$lib/shared/api';

  export let zones: Zone[];

  const parkingLotWidth = 200;
  const parkingLotHeight = 100;
</script>

<main class="flex items-center justify-center">
  <ZoneMap aspectRatio={parkingLotWidth / parkingLotHeight} {zones} />
</main>
