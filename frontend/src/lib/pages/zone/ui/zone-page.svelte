<script lang="ts">
  import { getContext } from 'svelte';
  import IconLeftArrowAlt from '~icons/bx/bx-left-arrow-alt';

  import { ZoneMap } from '$lib/widgets/zone-map';
  import { BookingModal } from '$lib/widgets/booking-modal';
  import type { ZoneMapDefinition } from '$lib/shared/api';

  const { open } = getContext('simple-modal');

  export let mapDefinition: ZoneMapDefinition;
</script>

<nav class="px-40 py-5 flex justify-center">
  <a
    class="inline-flex items-center justify-center px-4 py-2 bg-gray-800 rounded-lg text-white font-medium"
    href="/zones"
    sveltekit:prefetch
  >
    <IconLeftArrowAlt class="w-6 h-6 text-white mr-1" />
    Back
  </a>
</nav>
<main class="flex-1 flex items-center justify-center">
  <ZoneMap
    {...mapDefinition}
    on:space-requested={() =>
      open(
        BookingModal,
        {},
        { styleContent: { padding: 0 }, closeButton: false }
      )}
  />
</main>
