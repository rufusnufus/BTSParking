<script lang="ts">
  import Logo from './logo.svelte';
</script>

<header class="bg-black">
  <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
    <div class="relative flex items-center justify-between h-16">
      <Logo />

      <slot name="action" />
    </div>
  </div>
</header>
