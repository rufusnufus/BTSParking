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
 * Populates the `session` object with the `token` field.
 */
export const determineAuthorized: GetSession = request => {
  const cookies = parseCookieString(request.headers['Cookie']);

  return {
    token: cookies.get('AUTH_TOKEN'),
  };
};
