import {
  determineAuthorized,
} from '$lib/processes/auth';

export const getSession = determineAuthorized;
