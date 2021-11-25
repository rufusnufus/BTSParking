import type { Load } from '@sveltejs/kit';

export const skipHomeForAuthorizedUsers: Load = ({ session }) => {
  if (session.token !== undefined) {
    return {
      status: 302,
      redirect: '/zones',
    }
  }

  return {};
}

