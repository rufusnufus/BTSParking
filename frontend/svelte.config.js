import preprocess from 'svelte-preprocess';
import adapterNode from '@sveltejs/adapter-node';

const environment = {};
if (process.env.BACKEND_PREFIX_URL !== undefined) {
  environment['vite.define.backendPrefixURL'] = JSON.stringify(
    process.env.BACKEND_PREFIX_URL
  );
}

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],
  kit: {
    target: 'body',
    adapter: adapterNode(),
    vite: {
      define: environment,
    },
  },
};

export default config;
