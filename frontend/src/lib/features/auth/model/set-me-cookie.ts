import cookie from 'cookie';
import type { RequestHandler } from '@sveltejs/kit';

import { serverAPI } from '$lib/shared/api';

export const setMeCookie: RequestHandler = async request => {
  const code = request.query.get('code');
  if (code === null) {
    return {
      status: 400,
      body: 'A login code should be provided in the URL.',
    };
  }

  const {
    access_token: token,
    expires_in: maxAge,
    user_info: userInfo,
  } = await serverAPI.activateLoginCode(code);

  const cookieValue = JSON.stringify({ token, ...userInfo });
  return {
    status: 302,
    headers: {
      location: '/',
      'set-cookie': cookie.serialize('ME', cookieValue, {
        httpOnly: true,
        sameSite: 'strict',
        maxAge,
      }),
    },
  };
};
