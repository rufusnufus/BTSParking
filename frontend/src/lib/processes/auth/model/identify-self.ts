import cookie from 'cookie';
import type { GetSession } from '@sveltejs/kit';

/**
 * Determine if the incoming request is authorized to access the backend.
 *
 * Populates the `session` object with the following fields:
 *   - `email`
 *   - `token`
 *   - `is_admin`
 */
export const identifySelf: GetSession = request => {
  const cookies = cookie.parse(request.headers['cookie'] ?? '');

  if ('ME' in cookies) {
    return JSON.parse(cookies['ME']);
  } else {
    return {};
  }
};
