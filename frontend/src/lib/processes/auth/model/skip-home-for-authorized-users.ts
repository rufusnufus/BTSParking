import type { Load } from '@sveltejs/kit';

export const skipHomeForAuthorizedUsers: Load = ({ session, page }) => {
  if (page.query.get('redirect') === 'false') {
    return {
      status: 302,
      redirect: '/',
    };
  }

  if (session.token !== undefined) {
    return {
      status: 302,
      redirect: '/zones',
    };
  }

  return {};
};
