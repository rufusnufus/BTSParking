<script lang="ts">
  // import { bookSpace } from '$lib/features/booking';
  import { Space } from '$lib/entities/space';
  import { fixedAspectRatio, placeOnGrid } from '$lib/shared/ui';
  import type { ZoneMapDefinition } from '$lib/shared/types';

  export let width: number;
  export let height: number;
  export let objects: ZoneMapDefinition['objects'];

  $: aspectRatio = width / height;
</script>

<div class="flex-1 relative bg-gray-100 m-8" use:fixedAspectRatio={aspectRatio}>
  {#each objects as object}
    {#if object.type === 'space'}
      <Space
        name={object.id.toString()}
        free={object.free}
        style={placeOnGrid(object.start, object.end, width, height)}
      />
    {:else}
      <div
        role="presentation"
        class="bg-gray-300 z-0"
        style={placeOnGrid(object.start, object.end, width, height)}
      />
    {/if}
  {/each}
</div>
