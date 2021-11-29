import { sequence } from '@sveltejs/kit/hooks';

import {
  determineAuthorized,
  interceptLoginCode,
  interceptLogout,
} from '$lib/processes/auth';

export const getSession = determineAuthorized;

export const handle = sequence(interceptLoginCode, interceptLogout);
