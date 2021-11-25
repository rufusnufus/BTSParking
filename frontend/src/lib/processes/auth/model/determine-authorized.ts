import type { GetSession } from '@sveltejs/kit';

function parseCookieString(cookieString: string | undefined) {
  if (cookieString === undefined) {
    return new Map<string, string>();
  }

  return new Map(
    cookieString
      .split('; ')
      .map(cookiePair => cookiePair.split('=') as [string, string])
  );
}

/**
 * Determine if the incoming request is authorized to access the backend.
 *
 * Populates the `$session` store with the `authorized` field.
 */
export const determineAuthorized: GetSession = request => {
  const cookies = parseCookieString(request.headers['Cookie']);

  return {
    authorized: cookies.has('AUTH_TOKEN'),
  };
};
