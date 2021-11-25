import cookie from 'cookie';
import type { GetSession } from '@sveltejs/kit';

/**
 * Determine if the incoming request is authorized to access the backend.
 *
 * Populates the `session` object with the `token` field.
 */
export const determineAuthorized: GetSession = request => {
  const cookies = cookie.parse(request.headers['Cookie'] ?? '');

  return {
    // token: cookies['AUTH_TOKEN'],
    token: '<token>'
  };
};
