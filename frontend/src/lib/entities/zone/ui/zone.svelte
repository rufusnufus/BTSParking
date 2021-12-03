<script lang="ts">
  export let name: string;
  export let bookedSpaces: number;
  export let hasFreeSpaces: boolean;
  export let style: string | undefined = undefined;

  function s(amount: number) {
    if (amount !== 1) {
      return 's';
    }
    return '';
  }
</script>

<div
  class="cursor-pointer flex flex-col items-center justify-center rounded hover:scale-105 transition-transform shadow-md hover:shadow-lg z-10 backdrop-blur-sm"
  role="button"
  tabindex="0"
  on:click
  {style}
>
  <span class="text-2xl font-medium">{name}</span>
  {#if !hasFreeSpaces}
    <span>No more free spaces</span>
  {/if}
  {#if bookedSpaces !== undefined && bookedSpaces > 0}
    <span>{bookedSpaces} space{s(bookedSpaces)} booked</span>
  {/if}
</div>
