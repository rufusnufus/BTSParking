import type { HandleError } from '@sveltejs/kit';

import { logger } from './logger';
import { logRequest } from './log-request';

export const logRenderErrorsHook: HandleError = ({ request, error }) => {
  logger.error(error, 'Rendering failed');
  logRequest(request, { failed: true });
};
