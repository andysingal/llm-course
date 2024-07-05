<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import showdown from "showdown";

  import ChatMessageSources from "./ChatMessageSources.svelte";
  import LoadingDots from "./LoadingDots.svelte";

  export let isLoading = false;
  export let isUserMessage = false;
  export let author;
  export let message;
  export let date;

  const dispatch = createEventDispatcher();
  const showDownConverter = new showdown.Converter();

  let alertCssClass = "alert-primary";
  let messageCssClass = "message--user";

  if (!isUserMessage) {
    alertCssClass = "alert-light";
    messageCssClass = "message--app";
  }

  let processedMessage = "";
  let sources = [];

  $: if (message) {
    const [rawMessage, rawSources] = message.split("SOURCES:");

    message = rawMessage.replace("Response:", "");
    processedMessage = showDownConverter.makeHtml(message);

    if (rawSources) {
      sources = rawSources.split(",");
    }
  }

  function onSourceClick(event) {
    dispatch("chatMessageOnSourceClick", event.detail);
  }
</script>

<div class="message-wrapper d-inline-block">
  <div class="alert {alertCssClass} message {messageCssClass}">
    <h6 class="alert-heading">
      {author}
      <small class="text-body-secondary float-end">
        {new Date(date).toLocaleTimeString()}
      </small>
    </h6>

    {#if isLoading}
      <LoadingDots />
    {:else}
      {@html processedMessage}
    {/if}

    {#if sources?.length}
      <div class="mt-3">
        <ChatMessageSources
          {sources}
          on:chatMessageSourcesOnSourceClick={onSourceClick}
        />
      </div>
    {/if}
  </div>
</div>

<style>
  .message-wrapper {
    width: 100%;
  }

  .message {
    width: 50%;
  }

  .message--user {
    float: right;
  }

  .message--app {
    float: left;
  }

  /* https://stackoverflow.com/a/59670838 */
  .message :global(p) {
    margin-bottom: 0;
  }
</style>
