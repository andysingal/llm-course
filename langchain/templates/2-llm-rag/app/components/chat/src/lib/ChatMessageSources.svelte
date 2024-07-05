<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let sources = [];

  const dispatch = createEventDispatcher();

  function onSourceClick(sourceName: string) {
    dispatch("chatMessageSourcesOnSourceClick", sourceName);
  }
</script>

<h6 class="mb-0">Sourced from:</h6>
<ul>
  {#each sources as source}
    <li class="list-inline-item">
      <button type="button" class="btn btn-link py-0" on:click={onSourceClick(source)}>
        {source}
      </button>
    </li>
  {/each}
</ul>
