import type { RequestHandler } from '@sveltejs/kit';

interface MapObject {
  start: [number, number];
  end: [number, number];
}

interface Zone extends MapObject {
  type: 'zone';
  name: string;
  color: string;
}

interface Divider extends MapObject {
  type: 'divider'
}

export const get: RequestHandler<
  Record<string, unknown>,
  unknown,
  Array<Record<string, string | number[]>>
> = async () => {
  const mapObjects: Array<Zone | Divider> = [
    {
      type: 'zone',
      name: 'B',
      color: 'rgba(255 0 0 / 30%)',
      start: [0, 0],
      end: [132, 30],
    },
    {
      type: 'divider',
      start: [0, 31],
      end: [50, 31],
    },
    {
      type: 'divider',
      start: [70, 31],
      end: [132, 31],
    },
    {
      type: 'zone',
      name: 'C',
      color: 'rgba(0 0 255 / 30%)',
      start: [0, 32],
      end: [132, 62],
    },
    {
      type: 'divider',
      start: [0, 63],
      end: [50, 63],
    },
    {
      type: 'divider',
      start: [70, 63],
      end: [132, 63],
    },
    {
      type: 'zone',
      name: 'D',
      color: 'rgba(255 165 0 / 30%)',
      start: [0, 64],
      end: [0, 79],
    },
    {
      type: 'divider',
      start: [70, 63],
      end: [132, 63],
    },
    {
      type: 'zone',
      name: 'A',
      color: 'rgba(238 130 238 / 30%)',
      start: [170, 15],
      end: [200, 100],
    }
  ];

  return {
    body: mapObjects as unknown as Array<Record<string, string | number[]>>
  }
}
