import { goto, prefetch } from '$app/navigation';
import api from '$lib/shared/api';

const checkMagicLinkURL = '/check-magic-link';

export default async function submitAuthData(email: string | undefined): Promise<void> {
  if (email === undefined) {
    return;
  }

  prefetch(checkMagicLinkURL);

  try {
    console.log(await api.getLoginCode(email));
  } catch (e) {
    console.error('Request failed, sorry', e);
    return;
  }

  await goto(checkMagicLinkURL);
}
