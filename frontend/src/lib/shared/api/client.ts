import ky from 'ky';
import type { Options as KyOptions } from 'ky';

import type { Car, FreeSpace } from './entities';


export const prefix = vite.define.backendPrefixURL ?? 'http://localhost:8000';

class API {
  private apiClient: typeof ky;

  constructor(apiClientInstance: typeof ky | undefined = undefined) {
    this.apiClient = apiClientInstance ?? ky.create({ prefixUrl: prefix });
  }

  with(customFetch: KyOptions['fetch']) {
    return new API(this.apiClient.extend({ fetch: customFetch }));
  }

  /** Generate a one-time link that will log a user in with their e-mail. */
  requestLoginLink(email: string) {
    return this.apiClient.post('request-login-link', { json: { email } });
  }

  getLoginCode(email: string): Promise<string> {
    return this.apiClient.post('get-login-code', { json: { email } }).json();
  }

  /** Perform authorization by a given one-time login code. */
  activateLoginLink(loginCode: string) {
    return this.apiClient.post('activate-login-link', { json: { code: loginCode } });
  }

  /** Terminate a user's session. */
  logOut() {
    return this.apiClient.post('logout');
  }

  /** List the spaces that are available for parking. */
  listFreeSpaces(zoneID: number): Promise<FreeSpace[]> {
    return this.apiClient.get(`zones/${zoneID}/free-spaces`).json();
  }

  /** Book a parking space. */
  bookSpace(zoneID: number, spaceID: number, carID: number) {
    return this.apiClient.post(`zones/${zoneID}/book`, {
      json: { space_id: spaceID, car_id: carID },
    });
  }

  /** Stop occupying a parking space. */
  releaseSpace(zoneID: number, spaceID: number) {
    return this.apiClient.post(`zones/${zoneID}/release`, {
      json: { space_id: spaceID },
    });
  }

  /** List the saved cars. */
  listCars(): Promise<Car[]> {
    return this.apiClient.get('cars').json();
  }

  /** Create a new car. */
  createCar(model: string, licenseNumber: string) {
    return this.apiClient.post('cars', { json: { model, license_number: licenseNumber } });
  }

  /** Delete a saved car. */
  deleteCar(carID: number) {
    return this.apiClient.delete(`cars/${carID}`);
  }
}

export default new API();
