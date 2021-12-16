import { collectDefaultMetrics } from 'prom-client';

import { identifySelf } from '$lib/processes/auth';
import { logRequestsHook, logRenderErrorsHook } from '$lib/processes/logging';

collectDefaultMetrics();

export const getSession = identifySelf;

export const handle = logRequestsHook;

export const handleError = logRenderErrorsHook;
