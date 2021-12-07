import { goto, prefetch } from '$app/navigation';
import { browserAPI } from '$lib/shared/api';

const checkMagicLinkURL = '/check-magic-link';

export async function submitAuthData(email: string | undefined): Promise<void> {
  if (email === undefined) {
    return;
  }

  prefetch(checkMagicLinkURL);

  try {
    await api.requestLoginLink(email);
    await goto(checkMagicLinkURL);
  } catch (e) {
    // TODO: add proper error handling
    console.error('Request failed, sorry', e);
    return;
  }
}

export async function submitAuthDataCheat(
  email: string | undefined
): Promise<void> {
  if (email === undefined) {
    return;
  }

  try {
    const loginCode = await browserAPI.getLoginCode(email);
    window.location.href = `/activate?code=${loginCode}`;
  } catch (e) {
    // TODO: add proper error handling
    console.error('Request failed, sorry', e);
    return;
  }
}
