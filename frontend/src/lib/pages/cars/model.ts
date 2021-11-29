import type { Load } from '@sveltejs/kit';

import api from '$lib/shared/api';

export const fetchCars: Load = async ({ fetch, session }) => {
  const { token } = session;
  try {
    return {
      props: {
        cars: await api.with({ fetch, token }).listCars(),
      },
    };
  } catch (e) {
    console.log(e);
    return {
      props: {
        cars: [],
      },
    };
  }
};
