<script lang="ts">
  import { ParkingLotMap } from '$lib/widgets/parking-lot-map';
  import type { ParkingLotMapDefinition } from '$lib/shared/api';

  import { injectBoundaries } from '../lib/inject-boundaries';

  export let mapDefinition: ParkingLotMapDefinition;

  $: injectBoundaries(mapDefinition);
</script>

<main class="flex-1 flex items-center justify-center">
  <ParkingLotMap {...mapDefinition} />
</main>
