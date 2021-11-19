import type { Load } from '@sveltejs/kit';

import mapDefinition from './global-map.json';

export const mockFetchGlobalMap: Load = async () => ({
  props: { mapDefinition },
});
