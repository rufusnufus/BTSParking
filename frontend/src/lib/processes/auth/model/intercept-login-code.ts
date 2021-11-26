import cookie from 'cookie';
import type { Handle } from '@sveltejs/kit';

import api from '$lib/shared/api';

const _24hours = 24 * 60 * 60;

export const interceptLoginCode: Handle = async ({ request, resolve }) => {
  const code = request.query.get('code');
  if (request.path !== '/login' || code === null) {
    return resolve(request);
  }

  try {
    const token = (await api.with(fetch).activateLoginLink(code)).access_token;
    const response = await resolve(request);
    return {
      ...response,
      headers: {
        ...response.headers,
        'set-cookie': cookie.serialize('AUTH_TOKEN', token, {
          httpOnly: true,
          sameSite: 'strict',
          maxAge: _24hours,
        }),
      },
    };
  } catch (e) {
    console.error(e);
    return resolve(request);
  }
};
