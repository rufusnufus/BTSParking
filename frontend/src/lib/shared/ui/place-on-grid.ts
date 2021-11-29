import type { Point } from '../api';

export function placeOnGrid(
  start: Point,
  end: Point,
  width: number,
  height: number
): string {
  return [
    'position: absolute',
    `left: ${(start.x / width) * 100}%`,
    `top: ${(start.y / height) * 100}%`,
    `width: ${((end.x - start.x + 1) / width) * 100}%`,
    `height: ${((end.y - start.y + 1) / height) * 100}%`,
  ].join(';');
}
