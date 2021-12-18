import { register } from 'prom-client';
import type { RequestHandler } from '@sveltejs/kit';

export const exposeMetrics: RequestHandler = async _request => {
  return {
    status: 200,
    body: await register.metrics(),
    headers: {
      'content-type': register.contentType,
    },
  };
};
