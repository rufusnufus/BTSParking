<script lang="ts">
  import { LoginForm } from '$lib/features/auth';
</script>

<div class="min-h-full flex flex-1 items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
  <div class="max-w-md w-full space-y-8">
    <div>
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
        Sign in to your account
      </h2>
      <p class="mt-2 text-center text-sm text-gray-600">
        We will mail you a magic link that will log you in.
      </p>
    </div>

    <LoginForm />
  </div>
</div>
