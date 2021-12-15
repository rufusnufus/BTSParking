import { browser } from '$app/env';
import type { Load } from '@sveltejs/kit';

import { universalAPI } from '$lib/shared/api';

export const fetchGlobalMap: Load = async ({ fetch, session }) => {
  const { token } = session;
  return {
    props: {
      mapDefinition: await universalAPI(browser)
        .with({ fetch, token })
        .getGlobalMap(),
    },
  };
};
