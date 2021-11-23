import type { Load } from '@sveltejs/kit';

export const skipHomeForAuthorizedUsers: Load = ({ session }) => {
  if (session.authorized) {
    return {
      status: 302,
      redirect: '/zones',
    }
  }

  return {};
}

