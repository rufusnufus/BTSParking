<script lang="ts">
  import Transition from 'svelte-class-transition';
  import User from '@svicons/boxicons-regular/user.svelte';

  let dropdownShown = false;

  const menuItems = [
    {
      text: 'Your cars',
      href: '/cars',
    },
    {
      text: 'Statistics',
      href: '/statistics',
    },
    {
      text: 'Sign out',
      action: () => {},
    },
  ];
</script>

<div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
  <div class="ml-3 relative">
    <div>
    <button 
      type="button" 
      class="block text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" 
      id="user-menu-button" 
      aria-expanded={`${dropdownShown}`} 
      aria-haspopup="true"
      on:click={() => dropdownShown = !dropdownShown}
    >
      <span class="sr-only">Open user menu</span>
      <User class="w-6 text-white" />
    </button>
    </div>

    <Transition
      toggle={dropdownShown}
      transitions="transition transform"
      inTransition="ease-out duration-100"
      inState="opacity-0 scale-95"
      onState="opacity-100 scale-100"
      outState="opacity-0 scale-95"
      outTransition="ease-in duration-75"
    >
      <div 
        class="origin-top-right absolute right-0 mt-2 w-32 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none" 
        role="menu" 
        aria-orientation="vertical" 
        aria-labelledby="user-menu-button" 
        tabindex="-1"
      >
        <!-- Active: "bg-gray-100", Not Active: "" -->
        {#each menuItems as menuItem, index (menuItem.text)}
          {#if menuItem.href !== undefined}
            <a 
              class="block px-4 py-2 text-sm text-gray-700"
              class:bg-gray-100={false}
              role="menuitem" 
              tabindex="-1" 
              id="user-menu-item-{index}"
              href={menuItem.href}
            >
              {menuItem.text}
            </a>
          {:else}
            <span
              class="block px-4 py-2 text-sm text-gray-700 cursor-pointer" 
              role="menuitem" 
              tabindex="-1" 
              id="user-menu-item-{index}" 
              on:click={menuItem.action}
            >
              {menuItem.text}
            </span>
          {/if}
        {/each}
      </div>
    </Transition>
  </div>
</div>
