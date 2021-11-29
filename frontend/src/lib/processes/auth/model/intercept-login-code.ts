import cookie from 'cookie';
import type { Handle } from '@sveltejs/kit';

import api from '$lib/shared/api';

export const interceptLoginCode: Handle = async ({ request, resolve }) => {
  const code = request.query.get('code');
  if (request.path !== '/login' || code === null) {
    return resolve(request);
  }

  try {
    const { access_token: token, expires_in: maxAge } = await api
      .with({ fetch })
      .activateLoginCode(code);
    const response = await resolve(request);
    return {
      ...response,
      headers: {
        ...response.headers,
        'set-cookie': cookie.serialize('AUTH_TOKEN', token, {
          httpOnly: true,
          sameSite: 'strict',
          maxAge,
        }),
      },
    };
  } catch (e) {
    console.error(e);
    return resolve(request);
  }
};
