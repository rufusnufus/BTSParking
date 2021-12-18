<script lang="ts">
  import { Landing } from '$lib/widgets/landing';
  import { Pricing } from '$lib/features/pricing';
</script>

<Landing>
  <a
    href="tel:+7 (123) 456-78-90"
    class="py-2 px-12 lg:px-24 bg-red-800 rounded hover:bg-red-700"
  >
    Call us: +7 (123) 456-78-90
  </a>
  <Pricing />
</Landing>
