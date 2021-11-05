import type { GetSession } from '@sveltejs/kit';

export const getSession: GetSession = (_request) => {
	// Inspect `request.headers: Record<string, string>`
  return {
    authenticated: true,
  };
}
