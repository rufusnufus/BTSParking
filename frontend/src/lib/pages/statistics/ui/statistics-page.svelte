<script lang="ts">
  import { StatisticsGrid } from '$lib/widgets/statistics-grid';
  import type { Statistics } from '$lib/shared/api';

  export let statistics: Statistics[];
</script>

<StatisticsGrid {statistics} />
