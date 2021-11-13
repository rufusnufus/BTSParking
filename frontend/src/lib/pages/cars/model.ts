import type { Load } from '@sveltejs/kit';

import api from '$lib/shared/api';

const fetchCars: Load = async ({ fetch }) => {
  try {
    return {
      props: {
        cars: await api.with(fetch).listCars(),
      }
    };
  } catch (e) {
    console.log(e);
    return {
      props: {
        cars: [],
      }
    };
  }
}

export default fetchCars;