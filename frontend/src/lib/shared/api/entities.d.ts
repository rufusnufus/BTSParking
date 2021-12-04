export interface Car {
  readonly id?: number;
  model: string;
  license_number: string;
}

export interface User {
  email: string;
  readonly is_admin?: boolean;
}

export interface TokenResponse {
  token_type: 'bearer';
  access_token: string;
  expires_in: number;
  user_info: User;
}

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
  free_spaces: number;
  own_booked_spaces?: number;
  hourly_rate: number;
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
  booking?: Booking;
}

export interface Booking {
  occupying_car: Car;
  space_id: Space['id'];
  readonly booked_from?: string;
  booked_until: string;
}

export interface MapDefinition<ObjectType> {
  width: number;
  height: number;
  objects: ObjectType[];
}

export type ParkingLotMapDefinition = MapDefinition<
  Zone | Road | Divider | Gate
>;

export type ZoneMapDefinition = MapDefinition<Space | Road>;
