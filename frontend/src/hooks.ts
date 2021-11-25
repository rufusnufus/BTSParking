import { determineAuthorized, interceptLoginCode } from '$lib/processes/auth';

export const getSession = determineAuthorized;

export const handle = interceptLoginCode;
