import pino from 'pino';
import { dev } from '$app/env';

export const logger = pino({
  level: dev ? 'debug' : 'info',
});
