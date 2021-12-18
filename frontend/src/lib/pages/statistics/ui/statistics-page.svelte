<script lang="ts">
  import IconStats from '~icons/bx/bx-stats';

  import { StatisticsGrid } from '$lib/widgets/statistics-grid';
  import { EmptyState } from '$lib/shared/ui';
  import type { Statistics } from '$lib/shared/api';

  export let statistics: Statistics[];
</script>

<div class="flex-1 flex flex-col items-center justify-center">
  {#if statistics.length > 0}
    <StatisticsGrid {statistics} />
  {:else}
    <EmptyState icon={IconStats}>
      <p>Nothing to display.</p>
      <p>Book a parking space and see it here!</p>
    </EmptyState>
  {/if}
</div>
