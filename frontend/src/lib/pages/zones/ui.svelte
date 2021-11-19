<script lang="ts">
  import { ZoneMap } from '$lib/widgets/zone-map';
  import type { MapDefinition } from '$lib/shared/types';

  import { injectBoundaries } from './lib/inject-boundaries';

  export let mapDefinition: MapDefinition;

  $: injectBoundaries(mapDefinition);
</script>

<main class="flex-1 flex items-center justify-center">
  <ZoneMap {...mapDefinition} />
</main>
