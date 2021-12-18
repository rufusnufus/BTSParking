<script lang="ts">
  import { StatisticsCard } from '$lib/entities/statistics';
  import type { Statistics } from '$lib/shared/api';

  export let statistics: Statistics[];
</script>

<div class="max-w-2xl mx-auto py-8 px-4 sm:py-16 sm:px-6 lg:max-w-7xl lg:px-8">
  <div
    class="grid gap-y-10 grid-cols-1 gap-x-6 sm:grid-cols-2 lg:grid-cols-3 xl:gap-x-8"
  >
    {#each statistics as statisticsObject}
      <StatisticsCard {statisticsObject} />
    {/each}
  </div>
</div>
