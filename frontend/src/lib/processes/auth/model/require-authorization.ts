import type { Load } from '@sveltejs/kit';

const skipHomeForAuthorizedUsers: Load = ({ session }) => {
  if (!session.authenticated) {
    return {
      redirect: '/login',
      status: 302,
    };
  }

  return {};
}

export default skipHomeForAuthorizedUsers;
