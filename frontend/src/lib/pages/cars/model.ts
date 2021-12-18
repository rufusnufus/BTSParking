import { browser } from '$app/env';
import type { Load } from '@sveltejs/kit';

import { universalAPI } from '$lib/shared/api';

export const fetchCars: Load = async ({ fetch, session }) => {
  const { token } = session;
  return {
    props: {
      cars: await universalAPI(browser).with({ fetch, token }).listCars(),
    },
  };
};
