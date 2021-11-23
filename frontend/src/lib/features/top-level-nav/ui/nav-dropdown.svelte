<script lang="ts">
  import Transition from 'svelte-class-transition';

  import { ProfileDropdownToggle } from '$lib/entities/user';
  import MenuItem from './menu-item.svelte';
  import { menuItems } from '../model/menu-items';

  let dropdownShown = false;

  const toggleID = 'user-menu-button';
</script>

<div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
  <div class="ml-3 relative">
    <div>
      <ProfileDropdownToggle id={toggleID} bind:dropdownShown />
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
        aria-labelledby={toggleID}
        tabindex="-1"
      >
        <!-- Active: "bg-gray-100", Not Active: "" -->
        {#each menuItems as menuItem, index (menuItem.text)}
          <MenuItem
            id="user-menu-item-{index}"
            href={menuItem.href}
            action={menuItem.action}
          >
            {menuItem.text}
          </MenuItem>
        {/each}
      </div>
    </Transition>
  </div>
</div>
