import { goto, prefetch } from '$app/navigation';
import api from '$lib/shared/api';

const checkMagicLinkURL = '/check-magic-link';

export async function submitAuthData(email: string | undefined): Promise<void> {
  if (email === undefined) {
    return;
  }

  prefetch(checkMagicLinkURL);

  try {
    console.log(await api.getLoginCode(email));
  } catch (e) {
    // TODO: add proper error handling
    console.error('Request failed, sorry', e);
    return;
  }

  await goto(checkMagicLinkURL);
}
