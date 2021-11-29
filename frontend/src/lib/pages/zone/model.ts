import type { Load } from '@sveltejs/kit';

import zoneA from './zone-a.json';

export const mockFetchZoneMap: Load = () => ({
  props: { mapDefinition: zoneA },
});
