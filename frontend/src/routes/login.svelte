<script lang="ts" context="module">
  import { interceptLoginCode } from '$lib/pages/login';

  export const load = interceptLoginCode;
</script>

<script lang="ts">
  import { LoginPage } from '$lib/pages/login';
</script>

<LoginPage />
