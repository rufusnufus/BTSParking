export interface Car {
  id: number;
  model: string;
  license_number: string;
}

export interface FreeSpace {
  id: number;
}

export interface Space extends FreeSpace {
  occupying_car_id: number;
}
