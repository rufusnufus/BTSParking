<script lang="ts" context="module">
  import { requireAuthorization } from '$lib/processes/auth';
  import { fetchStatistics } from '$lib/pages/statistics';
  import { composeLoaders } from '$lib/shared/compose-loaders';

  export const load = composeLoaders(requireAuthorization, fetchStatistics);
</script>

<script lang="ts">
  import { StatisticsPage } from '$lib/pages/statistics';
  import type { Statistics } from '$lib/shared/api';

  export let statistics: Statistics[];
</script>

<StatisticsPage {statistics} />
