export type ColorRGB = [number, number, number];

export interface Point {
  x: number;
  y: number;
}

interface Rectangle {
  start: Point;
  end: Point;
}

export interface Zone extends Rectangle {
  type: 'zone';
  id: number;
  name: string;
  booked_spaces?: number;
}

export interface Road extends Rectangle {
  type: 'road';
}

export interface Divider extends Rectangle {
  type: 'divider';
}

export interface Gate extends Rectangle {
  type: 'gate';
  name: string;
}

export interface MapDefinition {
  width: number;
  height: number;
  objects: Array<Zone | Road | Divider | Gate>;
}
