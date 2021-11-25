import { derived } from 'svelte/store';
import type { SvelteComponent } from 'svelte';
import type { Readable } from 'svelte/store';

import { page, session } from '$app/stores';
import { LoginButton } from '$lib/features/auth';
import { NavDropdown } from '$lib/features/top-level-nav'

type HeaderActionComponent = typeof SvelteComponent;

export const headerAction: Readable<HeaderActionComponent | null> = derived(
  [page, session],
  ([$page, $session]) => {
    if ($page.path === '/check-magic-link') {
      return null;
    }

    if ($session.token !== undefined) {
      return NavDropdown;
    } else {
      return LoginButton;
    }
  }
)
