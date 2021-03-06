import cookie from 'cookie';
import type { RequestHandler } from '@sveltejs/kit';

export const removeMeCookie: RequestHandler = async _request => {
  return {
    status: 302,
    headers: {
      location: '/?redirect=false',
      'set-cookie': cookie.serialize('ME', '', {
        httpOnly: true,
        sameSite: 'strict',
        expires: new Date(0),
      }),
    },
  };
};
