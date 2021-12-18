<script lang="ts">
  import { session } from '$app/stores';
  import { createEventDispatcher } from 'svelte';
  import { Space } from '$lib/entities/space';
  import { fixedAspectRatio, placeOnGrid } from '$lib/shared/ui';
  import type { ZoneMapDefinition } from '$lib/shared/api';

  export let width: number;
  export let height: number;
  export let objects: ZoneMapDefinition['objects'];

  $: aspectRatio = width / height;

  const dispatch = createEventDispatcher();
</script>

<div class="flex-1 relative bg-gray-100 m-8" use:fixedAspectRatio={aspectRatio}>
  {#each objects as object}
    {#if object.type === 'space'}
      <Space
        name={object.id.toString()}
        free={object.free}
        disabled={$session.is_admin === object.free}
        style={placeOnGrid(object.start, object.end, width, height)}
        on:click={() => {
          if ($session.is_admin) {
            dispatch('space-queried', object);
          } else if (object.free) {
            dispatch('space-requested', object);
          }
        }}
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
