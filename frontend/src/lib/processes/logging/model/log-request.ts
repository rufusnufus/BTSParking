import cookie from 'cookie';
import type { Handle } from '@sveltejs/kit';
import type { ServerRequest } from '@sveltejs/kit/types/hooks';

import { logger } from './logger';

export interface LogRequestOptions {
  failed?: boolean;
}

export function logRequest(
  request: ServerRequest,
  options: LogRequestOptions = {}
): void {
  const cookies =
    typeof request.headers['cookie'] === 'string'
      ? cookie.parse(request.headers['cookie'])
      : undefined;
  const meCookie =
    cookies !== undefined && 'ME' in cookies
      ? JSON.parse(cookies['ME'])
      : undefined;

  logger.info(
    {
      method: request.method,
      path: request.path,
      query: request.query,
      user:
        meCookie !== undefined
          ? { email: meCookie.email, is_admin: meCookie.is_admin }
          : undefined,
    },
    options.failed ? 'Failed request' : 'Incoming request'
  );
  logger.debug(
    request.headers,
    options.failed ? 'Failed request headers' : 'Request headers'
  );
  if (request.body) {
    logger.debug(
      request.rawBody,
      options.failed ? 'Failed request body' : 'Request body'
    );
  }
}

export const logRequestsHook: Handle = ({ request, resolve }) => {
  logRequest(request);
  return resolve(request);
};
