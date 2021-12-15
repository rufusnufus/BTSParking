import { browser } from '$app/env';
import type { Load } from '@sveltejs/kit';

import { universalAPI } from '$lib/shared/api';

export const fetchZoneMap: Load = async ({ fetch, session, page }) => {
  const { token, is_admin } = session;
  const zoneID = parseInt(page.params.id, 10);
  const api = universalAPI(browser).with({ fetch, token });

  const mapDefinition = await (is_admin
    ? api.getFullZoneMap(zoneID)
    : api.getZoneMap(zoneID));

  return {
    props: { mapDefinition },
  };
};
