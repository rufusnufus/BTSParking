import type { Load } from '@sveltejs/kit';

export const ignoreLoginCode: Load = async ({ page }) => {
  if (page.query.has('code')) {
    return {
      redirect: '/',
      status: 302,
    }
  }

  return {};
}
