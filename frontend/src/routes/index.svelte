<script lang="ts" context="module">
  import { skipHomeForAuthorizedUsers } from '$lib/processes/auth';

  export const load = skipHomeForAuthorizedUsers;
</script>

<script lang="ts">
  import { HomePage } from '$lib/pages/home';
</script>

<HomePage />
