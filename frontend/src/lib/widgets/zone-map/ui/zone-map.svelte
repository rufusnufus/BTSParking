<script lang="ts">
  import { zoomInToZone } from '$lib/features/booking';
  import { Zone } from '$lib/entities/zone';
  import { Gate } from '$lib/entities/gate';
  import { fixedAspectRatio } from '$lib/shared/ui';
  import type { MapDefinition } from '$lib/shared/types';

  import { colorFor } from '../lib/color-palette';
  import { placeOnGrid } from '../lib/place-on-grid';
  import { determineLabelDirection } from '../lib/determine-label-direction';

  export let width: number;
  export let height: number;
  export let objects: MapDefinition['objects'];

  $: aspectRatio = width / height;
</script>

<div class="flex-1 relative bg-gray-100 m-8" use:fixedAspectRatio={aspectRatio}>
  {#each objects as object, index}
    {#if object.type === 'zone'}
      <Zone
        name={object.name}
        bookedSpaces={object?.booked_spaces ?? 0}
        style={[
          `background-color: ${colorFor(index, 0.4)}`,
          placeOnGrid(object.start, object.end, width, height),
        ].join(';')}
        on:click={() => zoomInToZone(object.id)}
      />
    {:else if object.type === 'gate'}
      <Gate
        label={object.name}
        labelDirection={determineLabelDirection(object.start, object.end)}
        style={placeOnGrid(object.start, object.end, width, height)}
      />
    {:else}
      <div
        role="presentation"
        class="{object.type === 'divider' ? 'bg-gray-600' : 'bg-gray-300'} z-0"
        style={placeOnGrid(object.start, object.end, width, height)}
      />
    {/if}
  {/each}
</div>
