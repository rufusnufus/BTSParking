import { browser } from '$app/env';
import type { Load } from '@sveltejs/kit';

import { universalAPI } from '$lib/shared/api';

export const fetchStatistics: Load = async ({ fetch, session }) => {
  const { token } = session;
  return {
    props: {
      statistics: await universalAPI(browser)
        .with({ fetch, token })
        .getUserStatistics(),
    },
  };
};
