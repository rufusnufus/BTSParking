import type { Load, LoadOutput } from '@sveltejs/kit';

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
