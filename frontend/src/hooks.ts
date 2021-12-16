import { collectDefaultMetrics } from 'prom-client';

import { identifySelf } from '$lib/processes/auth';
import { logRequestsHook, logRenderErrorsHook } from '$lib/processes/logging';

try {
  collectDefaultMetrics();
} catch (e) {
  // metrics are already registered, do nothing
}

export const getSession = identifySelf;

export const handle = logRequestsHook;

export const handleError = logRenderErrorsHook;
