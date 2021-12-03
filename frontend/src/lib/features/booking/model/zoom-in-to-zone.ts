import { goto } from '$app/navigation';

export async function zoomInToZone(id: number): Promise<void> {
  await goto(`/zones/${id}`);
}
