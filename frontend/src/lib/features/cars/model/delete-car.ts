import { cars } from '$lib/entities/car';
import { browserAPI } from '$lib/shared/api';

export async function deleteCar(
  thatCarID: number,
  token: string
): Promise<void> {
  await browserAPI.with({ token }).deleteCar(thatCarID);
  cars.update($cars => $cars.filter(thisCar => thisCar.id !== thatCarID));
}
