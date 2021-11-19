<script lang="ts">
  export let label: string;
  export let labelDirection: 'top' | 'right' | 'bottom' | 'left';
  export let style: string;
</script>

<div
  data-label={label}
  role="presentation"
  class="gate {labelDirection} bg-red-700 z-30 after:font-semibold after:relative"
  {style}
/>

<style>
  .gate::after {
    content: attr(data-label);
  }

  .gate.top::after {
    top: -1.5em;
    left: 40%;
  }

  .gate.left::after {
    left: -1em;
    top: 20%;
  }

  .gate.right::after {
    right: -1em;
    top: 20%;
  }
</style>
