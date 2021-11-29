import cookie from 'cookie';
import type { Handle } from '@sveltejs/kit';

export const interceptLogout: Handle = async ({ request, resolve }) => {
  if (request.path !== '/logout') {
    return resolve(request);
  }

  try {
    return {
      status: 204,
      headers: {
        'set-cookie': cookie.serialize('AUTH_TOKEN', 'None', {
          httpOnly: true,
          sameSite: 'strict',
          expires: new Date(0),
        }),
      },
    };
  } catch (e) {
    console.error(e);
    return resolve(request);
  }
};

