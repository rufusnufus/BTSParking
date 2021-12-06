/// <reference types="@sveltejs/kit" />
/// <reference types="unplugin-icons/types/svelte" />
/* eslint-disable @typescript-eslint/no-unused-vars */

declare namespace viteDefine {
  interface Vite {
    define: Define;
  }

  interface Define {
    clientBackendPrefix: string | undefined;
    serverBackendPrefix: string | undefined;
  }
}

declare const vite: viteDefine.Vite;
