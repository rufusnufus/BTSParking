import type { Load } from '@sveltejs/kit';

export const requireAuthorization: Load = ({ session }) => {
  if (session.token === undefined) {
    return {
      redirect: '/login',
      status: 302,
    };
  }

  return {};
}

