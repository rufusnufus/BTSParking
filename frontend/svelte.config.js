import preprocess from 'svelte-preprocess';

const environment = {
  'vite.define.backendPrefixURL': process.env.BACKEND_PREFIX_URL,
};

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],
  kit: {
    target: 'body',
    vite: {
      define: environment,
    },
  },
};

export default config;
