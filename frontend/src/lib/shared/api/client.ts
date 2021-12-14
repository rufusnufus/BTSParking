import ky from 'ky-universal';
import NodeFormData from 'form-data';
import type { Options as KyOptions } from 'ky';

import type {
  Booking,
  Car,
  TokenResponse,
  User,
  ParkingLotMapDefinition,
  ZoneMapDefinition,
} from './entities';

const browserPrefix =
  vite.define.clientBackendPrefix ?? 'http://localhost:8000/api/v1';
const serverPrefix = vite.define.serverBackendPrefix ?? browserPrefix;

class APIError extends Error {}

class API {
  private apiClient: typeof ky;
  private authorized: boolean;
  private prefix: string;

  constructor(
    prefixUrl: string,
    apiClientInstance: typeof ky | undefined = undefined,
    authorized = false
  ) {
    this.prefix = prefixUrl;
    this.apiClient = apiClientInstance ?? ky.create({ prefixUrl });
    this.authorized = authorized;
  }

  /** Throw an exception if this instance is not authorized. */
  private ensureAuthorized() {
    if (!this.authorized) {
      throw new APIError('An API token must be provided for this endpoint');
    }
  }

  /**
   * Use a custom `fetch` function or add an API token.
   *
   * Doesn't modify the instance, instead returns a new one.
   */
  with({ fetch, token }: { fetch?: KyOptions['fetch']; token?: string }) {
    const options: KyOptions = {};

    if (fetch !== undefined) {
      options.fetch = fetch;
    }

    if (token !== undefined) {
      options.headers = {
        Authorization: `Bearer ${token}`,
      };
    }

    return new API(
      this.prefix,
      this.apiClient.extend(options),
      token !== undefined
    );
  }

  /** Generate a one-time link that will log a user in with their e-mail. */
  requestLoginLink(email: string) {
    return this.apiClient.post('request-login-link', { json: <User>{ email } });
  }

  /** Temporary endpoint to bypass e-mail and just get a login code. */
  getLoginCode(email: string): Promise<string> {
    return this.apiClient
      .post('get-login-code', { json: <User>{ email } })
      .json();
  }

  /** Perform authorization by a given one-time login code. */
  activateLoginCode(loginCode: string): Promise<TokenResponse> {
    // The interface of FormData from 'form-data' is not compliant
    //   with the standard interface of FormData
    //     (https://developer.mozilla.org/docs/Web/API/FormData)
    //   The active issue on GitHub can be tracked here:
    //     https://github.com/form-data/form-data/issues/513
    const formData = new NodeFormData() as unknown as FormData;
    formData.append('username', 'None');
    formData.append('password', loginCode);

    return this.apiClient
      .post('activate-login-code', { body: formData })
      .json();
  }

  /** Terminate a user's session. */
  logOut() {
    this.ensureAuthorized();
    return this.apiClient.post('logout');
  }

  /** Get the properties and objects of the global map of the parking lot. */
  getGlobalMap(): Promise<ParkingLotMapDefinition> {
    this.ensureAuthorized();
    return this.apiClient.get('map').json();
  }

  /** Get the objects of the zone map and the information on occupants. */
  getFullZoneMap(zoneID: number): Promise<ZoneMapDefinition> {
    this.ensureAuthorized();
    return this.apiClient.get(`zones/${zoneID}/full-map`).json();
  }

  /** Get the objects of the zone map and information on own cars. */
  getZoneMap(zoneID: number): Promise<ZoneMapDefinition> {
    this.ensureAuthorized();
    return this.apiClient.get(`zones/${zoneID}/map`).json();
  }

  /** Book a parking space. */
  bookSpace(zoneID: number, spaceID: number, car: Car, bookedUntil: Date) {
    this.ensureAuthorized();
    return this.apiClient.post(`zones/${zoneID}/book`, {
      json: <Booking>{
        space_id: spaceID,
        occupying_car: car,
        booked_until: bookedUntil.toISOString(),
      },
    });
  }

  /** List the saved cars. */
  listCars(): Promise<Car[]> {
    this.ensureAuthorized();
    return this.apiClient.get('cars').json();
  }

  /** Create a new car. */
  createCar(model: string, licenseNumber: string): Promise<Pick<Car, 'id'>> {
    this.ensureAuthorized();
    return this.apiClient
      .post('cars', {
        json: <Car>{ model, license_number: licenseNumber },
      })
      .json();
  }

  /** Delete a saved car. */
  deleteCar(carID: number) {
    this.ensureAuthorized();
    return this.apiClient.delete(`cars/${carID}`);
  }
}

export const browserAPI = new API(browserPrefix);
export const serverAPI = new API(serverPrefix);

export function universalAPI(fromBrowser: boolean): API {
  return fromBrowser ? browserAPI : serverAPI;
}
