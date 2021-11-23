<script lang="ts">
  import { ParkingLotMap } from '$lib/widgets/parking-lot-map';
  import type { MapDefinition } from '$lib/shared/types';

  import { injectBoundaries } from '../lib/inject-boundaries';

  export let mapDefinition: MapDefinition;

  $: injectBoundaries(mapDefinition);
</script>

<main class="flex-1 flex items-center justify-center">
  <ParkingLotMap {...mapDefinition} />
</main>
