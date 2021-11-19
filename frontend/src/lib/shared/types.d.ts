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

export interface Space extends Rectangle {
  type: 'space';
  id: number;
  free: boolean;
}

interface MapDefinition<ObjectType> {
  width: number;
  height: number;
  objects: ObjectType[];
}

export type ParkingLotMapDefinition = MapDefinition<Zone | Road | Divider | Gate>;

export type ZoneMapDefinition = MapDefinition<Space | Road>;
