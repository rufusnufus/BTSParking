import type { Load } from '@sveltejs/kit';

export const requireAuthorization: Load = ({ session }) => {
  if (session.token === undefined) {
    return {
      status: 302,
      redirect: '/login',
    };
  }

  return {};
};
