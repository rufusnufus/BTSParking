import merge from 'lodash.merge';
import type { Load, LoadOutput } from '@sveltejs/kit';

/**
 * Combine the responses of several loaders, stopping early.
 *
 * Will call each loader one by one, merging in whatever it
 * returned to the result unless it returns an HTTP response
 * status code, in which case the subsequent loaders are skipped.
 */
export function composeLoaders(...loaders: Load[]): Load {
  return async function composedLoad(options) {
    let loadingResult: LoadOutput = {};

    for (const loader of loaders) {
      const loadOutput = await loader(options);
      if (loadOutput === undefined) {
        return loadOutput;
      }

      loadingResult = merge(loadingResult, loadOutput);

      if (loadingResult.status !== undefined) {
        break;
      }
    }

    return loadingResult;
  };
}
