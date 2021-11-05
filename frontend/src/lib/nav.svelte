<script lang="ts">
  import ProfileDropdown from '$lib/profile-dropdown.svelte';
  import LoginButton from '$lib/login-button.svelte';

  export let authenticated: boolean;
</script>

<nav class="bg-gray-800">
  <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
    <div class="relative flex items-center justify-between h-16">
      <div class="flex-1 flex items-center justify-center sm:justify-start">
        <img class="h-10" src="/bts-logo.svg" alt="A chicken">
        <div class="text-white text-xl ml-4 hidden sm:block">
          <span class="font-righteous">BTS.</span><span>Parking</span>
        </div>
      </div>

      {#if authenticated}
        <ProfileDropdown />
      {:else}
        <LoginButton />
      {/if}
    </div>
  </div>
</nav>

<style>
  .font-righteous {
    font-family: 'Righteous', sans-serif;
  }
</style>
