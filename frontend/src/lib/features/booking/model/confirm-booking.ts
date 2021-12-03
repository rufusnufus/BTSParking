import { goto } from '$app/navigation';

export function confirmBooking(_carID: number, _bookedUntil: Date): void {
  goto('/booked-successfully');
}
