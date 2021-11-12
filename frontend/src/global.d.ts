/// <reference types="@sveltejs/kit" />
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
