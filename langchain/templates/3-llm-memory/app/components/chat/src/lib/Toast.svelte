<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let title = "";
  export let body = "";
  export let state = "danger";

  const dispatch = createEventDispatcher();

  function onClose(): void {
    dispatch("toastOnClose");
  }
</script>

<div class="toast show" role="alert">
  <div class="toast-header text-bg-{state}">
    <strong class="me-auto">{title}</strong>
    <button type="button" class="btn-close" aria-label="Close" on:click={onClose}>
    </button>
  </div>

  <div class="toast-body">
    {body}
  </div>
</div>

<style>
  .toast {
    position: fixed;
    top: 2vh;
    right: 2vh;
    z-index: 9999;
    background-color: rgba(255, 255, 255, 0.95);
  }
</style>
