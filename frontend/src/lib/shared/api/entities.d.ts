export interface Point {
  x: number;
  y: number;
}

export interface Car {
  id: number;
  model: string;
  license_number: string;
}

export interface FreeSpace {
  id: number;
}

export interface Zone {
  id: number;
  name: string;
  start: Point;
  end: Point;
}
