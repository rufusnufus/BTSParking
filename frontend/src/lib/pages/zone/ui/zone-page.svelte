<script lang="ts">
  import LeftArrowAlt from '@svicons/boxicons-regular/left-arrow-alt.svelte';

  import { ZoneMap } from '$lib/widgets/zone-map';
  import type { ZoneMapDefinition } from '$lib/shared/types';

  export let mapDefinition: ZoneMapDefinition;
</script>

<nav class="px-40 py-5 flex justify-center">
  <a
    class="inline-flex items-center justify-center px-4 py-2 bg-gray-800 rounded-lg text-white font-medium"
    href="/zones"
    sveltekit:prefetch
  >
    <LeftArrowAlt class="w-6 text-white mr-1" />
    Back
  </a>
</nav>
<main class="flex-1 flex items-center justify-center">
  <ZoneMap {...mapDefinition} />
</main>
