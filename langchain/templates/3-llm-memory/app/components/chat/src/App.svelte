<script lang="ts">
  import { onMount } from "svelte";

  import {
    doRequest,
    getFileNameWithoutExtensionAndTimeStamp,
    scrollToBottom,
  } from "./lib/utils";

  import AddDocumentForm from "./lib/AddDocumentForm.svelte";
  import ChatForm from "./lib/ChatForm.svelte";
  import ChatMessage from "./lib/ChatMessage.svelte";
  import MessageSourceModal from "./lib/MessageSourceModal.svelte";
  import Toast from "./lib/Toast.svelte";

  export let initialChatState = {};

  let aborter = new AbortController();

  let isLoading = false;
  let showAddDocumentForm = false;
  let showMessageSourceModal = false;
  let showToast = false;

  const defaultPrompt = "";
  const defaultMessages: Array<object> = [];

  let currentPrompt = defaultPrompt;
  let messages = structuredClone(defaultMessages);

  const userAuthor = "You";
  const defaultChatMessage = {
    body: "",
    author: "🤖 MattGPT",
    date: null,
    isUserMessage: false,
  };

  const defaultToastMessage = {
    title: "",
    body: "",
    state: "danger",
  };

  let toastMessage = structuredClone(defaultToastMessage);

  let defaultSource = {
    source: "",
    page_content: "",
  };

  let currentSource = structuredClone(defaultSource);

  onMount(() => {
    setChatMessageFromInitialState();
  });

  function setChatMessageFromInitialState(): void {
    initialChatState?.chat_messages.forEach((message) => {
      let newMessage = structuredClone(defaultChatMessage);
      newMessage.body = message.body;
      newMessage.date = new Date(message.created_at);

      if (message.role === "user") {
        newMessage.author = userAuthor;
        newMessage.isUserMessage = true;
      }

      messages.push(newMessage);
    });

    refreshMessages();
  }

  function refreshMessages(): void {
    // force svelte re-render
    // https://svelte.dev/tutorial/updating-arrays-and-objects
    messages = messages;

    scrollToBottom();
  }

  async function onClearChat(event: Event): Promise<void> {
    if (!window.confirm("Are you sure you want to clear the chat?")) {
      return;
    }

    const endpointUrl = `/chats/${initialChatState.id}/chat-messages`;
    await doRequest(endpointUrl, {}, aborter, "DELETE");

    flashToast("Success!", "Chat cleared!", "danger");

    currentPrompt = defaultPrompt;
    messages = structuredClone(defaultMessages);

    refreshMessages();
  }

  async function flashToast(
    title = "There was an error.",
    body = "Please try again later.",
    state = "danger",
  ): Promise<void> {
    toastMessage.title = title;
    toastMessage.body = body;
    toastMessage.state = state;

    showToast = true;

    await new Promise((resolve) => setTimeout(resolve, 5000));

    showToast = false;
  }

  function onToastClose(): void {
    showToast = false;
    toastMessage = structuredClone(defaultToastMessage);
  }

  async function onChatFormSubmit(event: Event): Promise<void> {
    isLoading = true;

    aborter.abort();
    aborter = new AbortController();

    messages.push({
      body: currentPrompt,
      author: userAuthor,
      date: Date.now(),
      isUserMessage: true,
    });

    const requestBody = {
      prompt: currentPrompt,
    };

    currentPrompt = defaultPrompt;

    refreshMessages();

    messages.push(structuredClone(defaultChatMessage));

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
          messages[messages.length - 1].body += text;
        } else {
          messages[messages.length - 1].body = text;
          messages[messages.length - 1].date = Date.now();

          firstTokenLoadedAlreadyLoaded = true;
        }

        refreshMessages();
      }
    } else {
      flashToast();
    }

    isLoading = false;
  }

  function onChatAddDocumentClick(): void {
    showAddDocumentForm = true;
  }

  async function addDocumentFormSubmit(event: Event): Promise<void> {
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

  function onAddDocumentFormClose(): void {
    showAddDocumentForm = false;
  }

  async function onSourceClick(event: Event): Promise<void> {
    isLoading = true;

    let sourceName = getFileNameWithoutExtensionAndTimeStamp(event.detail).trim();

    currentSource = await getSource(sourceName);
    showMessageSourceModal = true;

    isLoading = false;
  }

  async function getSource(sourceName: string): Promise<object> {
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

  function onMessageSourceModalClose(): void {
    showMessageSourceModal = false;
    currentSource = structuredClone(defaultSource);
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

  <div class="border-bottom border-dark-subtle mb-4 pb-3">
    <h5 class="d-inline-block mr-2">
      {initialChatState.title}
    </h5>
    <button
      type="button"
      class="btn btn-sm btn-outline-danger float-end"
      on:click={onClearChat}
    >
      Clear Chat
    </button>
  </div>

  <ul class="list-unstyled">
    {#each messages as message, i}
      <li>
        {#if message.isUserMessage}
          <ChatMessage
            isUserMessage={message.isUserMessage}
            author={message.author}
            message={message.body}
            date={message.date}
          />
        {:else if message.body}
          <ChatMessage
            isUserMessage={message.isUserMessage}
            author={message.author}
            message={message.body}
            date={message.date}
            on:chatMessageOnSourceClick={onSourceClick}
          />
        {:else}
          <ChatMessage
            isUserMessage={false}
            author={message.author}
            message={message.body}
            date={message.date}
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
