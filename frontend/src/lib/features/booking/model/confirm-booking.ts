import { browserAPI, type Car } from '$lib/shared/api';
import { goto } from '$app/navigation';

export async function confirmBooking(
  zoneID: number,
  spaceID: number,
  car: Car,
  bookedUntil: Date,
  token: string
): Promise<void> {
  await browserAPI.with({ token }).bookSpace(zoneID, spaceID, car, bookedUntil);
  goto('/booked-successfully');
}
