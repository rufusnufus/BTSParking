import cookie from 'cookie';
import type { RequestHandler } from '@sveltejs/kit';

import api from '$lib/shared/api';

export const setTokenCookie: RequestHandler = async (request) => {
  const code = request.query.get('code');
  if (code === null) {
    return {
      status: 400,
      body: 'A login code should be provided in the URL.',
    };
  }

  try {
    const { access_token: token, expires_in: maxAge } = await api
      .with({ fetch })
      .activateLoginCode(code);
    return {
      status: 302,
      headers: {
        'location': '/',
        'set-cookie': cookie.serialize('AUTH_TOKEN', token, {
          httpOnly: true,
          sameSite: 'strict',
          maxAge,
        }),
      },
    };
  } catch (e) {
    console.error(e);
    return {
      status: 500,
    }
  }
};
