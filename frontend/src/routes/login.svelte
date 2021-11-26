<script lang="ts" context="module">
  import { ignoreLoginCode } from '$lib/pages/login';

  export const load = ignoreLoginCode;
</script>

<script lang="ts">
  import { LoginPage } from '$lib/pages/login';
</script>

<LoginPage />
