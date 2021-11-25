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
      loadingResult = Object.assign(loadingResult, await loader(options));

      if (loadingResult.status !== undefined) {
        break;
      }
    }

    return loadingResult;
  };
}
