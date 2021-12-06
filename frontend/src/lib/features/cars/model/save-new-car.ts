import { cars } from '$lib/entities/car';
import { browserAPI } from '$lib/shared/api';
import type { Car } from '$lib/shared/api';

interface Event {
  detail: Pick<Car, 'model' | 'license_number'>;
}

export async function saveNewCar(
  { detail }: Event,
  token: string
): Promise<void> {
  const { model, license_number } = detail;
  const { id } = await browserAPI
    .with({ token })
    .createCar(model, license_number);
  cars.update($cars => {
    $cars.push({ id, model, license_number });
    return $cars;
  });
}
