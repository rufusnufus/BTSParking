<script lang="ts">
  import { headerAction } from '$lib/processes/auth';
  import { Header } from '$lib/widgets/header';

  import '$lib/app/global.css';
</script>

<Header>
  <svelte:component slot="action" this={$headerAction} />
</Header>

<slot />
