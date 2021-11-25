<script lang="ts">
  import { submitAuthDataCheat } from '../model/submit-auth-data';

  let email: string | undefined;
</script>

<form
  class="mt-8 space-y-6"
  method="POST"
  on:submit|preventDefault={() => submitAuthDataCheat(email)}
>
  <div class="rounded-md shadow-sm">
    <div>
      <label for="email-address">Email address</label>
      <input
        id="email-address"
        name="email"
        type="email"
        autocomplete="email"
        required
        class="appearance-none rounded-md relative block w-full mt-2 px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
        placeholder="user@example.com"
        bind:value={email}
      />
    </div>
  </div>
  <div>
    <button
      type="submit"
      class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-gray-800 hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      Send me the link!
    </button>
  </div>
</form>
