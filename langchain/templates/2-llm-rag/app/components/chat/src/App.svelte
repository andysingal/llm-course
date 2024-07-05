<script lang="ts">
  import {
    doRequest,
    getFileNameWithoutExtensionAndTimeStamp,
    throttle,
  } from "./lib/utils";

  import AddDocumentForm from "./lib/AddDocumentForm.svelte";
  import ChatForm from "./lib/ChatForm.svelte";
  import ChatMessage from "./lib/ChatMessage.svelte";
  import MessageSourceModal from "./lib/MessageSourceModal.svelte";
  import Toast from "./lib/Toast.svelte";

  let aborter = new AbortController();

  const defaultChatMessage = {
    body: "",
    author: "🤖 MattGPT",
    date: Date.now(),
  };

  let showAddDocumentForm = false;

  const defaultToastMessage = {
    title: "",
    body: "",
    state: "danger",
  };

  let toastMessage = structuredClone(defaultToastMessage);

  let showMessageSourceModal = false;

  let defaultSource = {
    source: "",
    page_content: "",
  };

  let currentSource = structuredClone(defaultSource);

  let isLoading = false;
  let showToast = false;
  let currentPrompt = "";
  let messages = [];

  async function onChatFormSubmit(event) {
    isLoading = true;

    aborter.abort();
    aborter = new AbortController();

    messages.push({
      prompt: { body: currentPrompt, author: "You", date: Date.now() },
    });

    const requestBody = {
      prompt: currentPrompt,
    };

    currentPrompt = "";

    refreshMessages();

    messages[messages.length - 1].output = structuredClone(defaultChatMessage);

    const response = await doRequest("/prompt-stream", requestBody, aborter);

    if (response?.ok) {
      let firstTokenLoadedAlreadyLoaded = false;
      const reader = response.body.getReader();

      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        const text = new TextDecoder().decode(value);

        if (firstTokenLoadedAlreadyLoaded) {
          messages[messages.length - 1].output.body += text;
        } else {
          messages[messages.length - 1].output.body = text;
          messages[messages.length - 1].output.date = Date.now();

          firstTokenLoadedAlreadyLoaded = true;
        }

        refreshMessages();
      }
    } else {
      flashToast();
    }

    isLoading = false;
  }

  function refreshMessages() {
    // force svelte re-render
    // https://svelte.dev/tutorial/updating-arrays-and-objects
    messages = messages;

    scrollToBottom();
  }

  function scrollToBottom() {
    const throttleMs = 200;
    const timeoutMs = 10;

    throttle(
      setTimeout(function () {
        window.scrollTo({
          top: document.body.scrollHeight,
          behavior: "smooth",
        });
      }, timeoutMs),
      throttleMs,
    );
  }

  async function onChatAddDocumentClick() {
    showAddDocumentForm = true;
  }

  async function addDocumentFormSubmit(event) {
    showAddDocumentForm = false;
    isLoading = true;

    const endpointUrl = "/document";
    const newDocument = event.detail;

    aborter.abort();
    aborter = new AbortController();

    let response = await doRequest(endpointUrl, newDocument, aborter);

    if (response?.ok) {
      flashToast("Success!", "Document added successfully", "success");
    } else {
      flashToast();
    }

    isLoading = false;
  }

  function onAddDocumentFormClose() {
    hideAddDocumentForm();
  }

  function hideAddDocumentForm() {
    showAddDocumentForm = false;
  }

  async function flashToast(
    title = "There was an error.",
    body = "Please try again later.",
    state = "danger",
  ) {
    toastMessage.title = title;
    toastMessage.body = body;
    toastMessage.state = state;

    showToast = true;

    await new Promise((resolve) => setTimeout(resolve, 5000));

    showToast = false;
  }

  function hideToast() {
    showToast = false;
    toastMessage = structuredClone(defaultToastMessage);
  }

  function onToastClose() {
    hideToast();
  }

  async function onSourceClick(event) {
    isLoading = true;

    let sourceName = getFileNameWithoutExtensionAndTimeStamp(event.detail).trim();

    currentSource = await getSource(sourceName);
    showMessageSourceModal = true;

    isLoading = false;
  }

  async function getSource(sourceName: string) {
    let source = null;

    const endpointUrl = "/document/find";

    aborter.abort();
    aborter = new AbortController();

    let response = await doRequest(`${endpointUrl}/${sourceName}`, {}, aborter, "GET");

    if (response?.ok) {
      source = await response.json();
    }

    return source;
  }

  function onMessageSourceModalClose() {
    hideMessageSourceModal();
  }

  function resetCurrenSource() {
    currentSource = structuredClone(defaultSource);
  }

  function hideMessageSourceModal() {
    showMessageSourceModal = false;
  }
</script>

<main class="pb-5">
  {#if showToast}
    <Toast
      bind:title={toastMessage.title}
      bind:body={toastMessage.body}
      bind:state={toastMessage.state}
      on:toastOnClose={onToastClose}
    />
  {/if}

  {#if showAddDocumentForm}
    <AddDocumentForm
      on:addDocumentFormOnSubmit={addDocumentFormSubmit}
      on:addDocumentFormOnClose={onAddDocumentFormClose}
    />
  {/if}

  {#if showMessageSourceModal}
    <MessageSourceModal
      title={currentSource.source}
      body={currentSource.page_content}
      on:messageSourceModalOnClose={onMessageSourceModalClose}
    />
  {/if}

  <ul class="list-unstyled">
    {#each messages as message, i}
      <li>
        {#if message.prompt}
          <ChatMessage
            isUserMessage={true}
            author={message.prompt.author}
            message={message.prompt.body}
            date={message.prompt.date}
          />
        {/if}

        {#if message.output.body}
          <ChatMessage
            isUserMessage={false}
            author={message.output.author}
            message={message.output.body}
            date={message.output.date}
            on:chatMessageOnSourceClick={onSourceClick}
          />
        {:else}
          <ChatMessage
            isUserMessage={false}
            author={message.output.author}
            message={message.output.body}
            date={message.output.date}
            isLoading={true}
            on:chatMessageOnSourceClick={onSourceClick}
          />
        {/if}
      </li>
    {/each}
  </ul>

  <div class="fixed-bottom">
    <div class="container">
      <ChatForm
        bind:currentPrompt
        bind:isLoading
        on:chatFormOnSubmit={onChatFormSubmit}
        on:chatFormOnAddDocumentClick={onChatAddDocumentClick}
      />
    </div>
  </div>
</main>
