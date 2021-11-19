import type { MapDefinition } from '$lib/shared/types';

export function injectBoundaries(mapDefinition: MapDefinition): void {
  mapDefinition.objects.push(
    {
      type: 'divider',
      start: {
        x: 0,
        y: 0,
      },
      end: {
        x: mapDefinition.width - 1,
        y: 0,
      },
    },
    {
      type: 'divider',
      start: {
        x: 0,
        y: 0,
      },
      end: {
        x: 0,
        y: mapDefinition.height - 1,
      },
    },
    {
      type: 'divider',
      start: {
        x: 0,
        y: mapDefinition.height - 1,
      },
      end: {
        x: mapDefinition.width - 1,
        y: mapDefinition.height - 1,
      },
    },
    {
      type: 'divider',
      start: {
        x: mapDefinition.width - 1,
        y: 0,
      },
      end: {
        x: mapDefinition.width - 1,
        y: mapDefinition.height - 1,
      },
    }
  );
}
