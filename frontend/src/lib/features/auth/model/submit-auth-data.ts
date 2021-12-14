import { goto, prefetch } from '$app/navigation';
import { browserAPI } from '$lib/shared/api';

const checkMagicLinkURL = '/check-magic-link';

export async function submitAuthData(email: string | undefined): Promise<void> {
  if (email === undefined) {
    return;
  }

  prefetch(checkMagicLinkURL);

  await browserAPI.requestLoginLink(email);
  await goto(checkMagicLinkURL);
}

export async function submitAuthDataCheat(
  email: string | undefined
): Promise<void> {
  if (email === undefined) {
    return;
  }

  const loginCode = await browserAPI.getLoginCode(email);
  window.location.href = `/activate?code=${loginCode}`;
}
