import fetch from 'node-fetch';
import type { Handle } from '@sveltejs/kit';
import type { Options as KyOptions } from 'ky';

import api from '$lib/shared/api';

function buildTokenCookie(token: string) {
  return [
    `AUTH_TOKEN=${token}`,
    'HttpOnly',
    'SameSite=Strict',
    `MaxAge=${24 * 60 * 60}`,
  ].join('; ');
}

export const interceptLoginCode: Handle = async ({ request, resolve }) => {
  if (request.path !== '/login') {
    return resolve(request);
  }

  const code = request.query.get('code');
  if (code === null) {
    return resolve(request);
  }

  try {
    const token = (
      await api.with(fetch as KyOptions['fetch']).activateLoginLink(code)
    ).access_token;
    const response = await resolve(request);
    return {
      ...response,
      headers: {
        ...response.headers,
        'Set-Cookie': buildTokenCookie(token),
      },
    };
  } catch (e) {
    console.error(e);
    return resolve(request);
  }
};
