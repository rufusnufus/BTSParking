/// <reference types="@sveltejs/kit" />
/// <reference types="unplugin-icons/types/svelte" />
/* eslint-disable @typescript-eslint/no-unused-vars */

namespace viteDefine {
  interface Vite {
    define: Define;
  }

  interface Define {
    backendPrefixURL: string | undefined;
  }
}

const vite: viteDefine.Vite;
