<script lang="ts" context="module">
  import type { Load } from '@sveltejs/kit';

  export const load: Load = async ({ session }) => {
    return {
      props: {
        authenticated: session.authenticated,
      }
    };
  }
</script>

<script lang="ts">
  import Nav from '$lib/nav.svelte';
  import '../app.css';

  export let authenticated: boolean;
</script>

<Nav {authenticated} />
<slot />
