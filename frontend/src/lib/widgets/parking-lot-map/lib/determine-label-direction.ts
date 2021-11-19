import type { Point } from '$lib/shared/types';

export function determineLabelDirection(
  start: Point,
  end: Point
): 'left' | 'top' | 'right' | 'bottom' {
  if (start.x <= 1 && end.x <= 1) {
    return 'left';
  } else if (start.y <= 1 && end.y <= 1) {
    return 'top';
  } else if (end.y - start.y > end.x - start.x) {
    return 'right';
  } else {
    return 'bottom';
  }
}
