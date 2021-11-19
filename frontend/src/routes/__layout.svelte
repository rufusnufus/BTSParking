<script lang="ts">
  import Modal from 'svelte-simple-modal';
  import { headerAction } from '$lib/processes/auth';
  import { Header } from '$lib/widgets/header';

  import '$lib/app/global.css';
</script>

<Modal>
  <Header>
    <svelte:component slot="action" this={$headerAction} />
  </Header>

  <slot />
</Modal>
