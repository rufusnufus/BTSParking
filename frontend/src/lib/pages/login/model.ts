import { HTTPError } from 'ky';
import type { Load } from '@sveltejs/kit';

import api from '$lib/shared/api';

const interceptLoginCode: Load = async ({ page, fetch }) => {
  const loginCode = page.query.get('code');

  if (loginCode !== null) {
    try {
      await api.with(fetch).activateLoginLink(loginCode);
      return {
        redirect: '/cars',
        status: 302,
      }
    } catch (error) {
      return {
        status: 500,
        error: (error instanceof HTTPError ? error : String(error)),
      };
    }
  }

  return {};
}

export default interceptLoginCode;
