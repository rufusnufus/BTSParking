import preprocess from 'svelte-preprocess';
import adapterNode from '@sveltejs/adapter-node';
import Icons from 'unplugin-icons/vite';

const environment = {
  'vite.define.backendPrefixURL': process.env.BACKEND_PREFIX_URL,
};

for (const key in environment) {
  if (typeof environment[key] === 'string') {
    environment[key] = JSON.stringify(environment[key]);
  }
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
      plugins: [
        Icons({
          compiler: 'svelte',
        }),
      ],
    },
  },
};

export default config;
