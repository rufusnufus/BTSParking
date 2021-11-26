import { writable } from "svelte/store";
import type { Car } from "$lib/shared/api";

export const cars = writable<Car[]>([]);
