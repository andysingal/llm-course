<script lang="ts">
  import { createEventDispatcher } from "svelte";

  let title = "";
  let body = "";

  const dispatch = createEventDispatcher();

  function onSubmit(): void {
    dispatch("addDocumentFormOnSubmit", {
      title: title,
      body: body,
    });
  }

  function onClose(): void {
    dispatch("addDocumentFormOnClose");
  }
</script>

<div class="modal d-inline-block">
  <form class="modal-dialog modal-dialog-centered" on:submit|preventDefault={onSubmit}>
    <div class="modal-content">
      <div class="modal-header text-bg-dark">
        <h5 class="modal-title">Add a document to the model</h5>
        <button type="button" class="btn btn-dark fw-bolder" on:click={onClose}>
          ✕
        </button>
      </div>

      <div class="modal-body">
        <div class="mb-4">
          <label for="newDocumentTitle" class="form-label">
            <small>Title</small>
          </label>
          <input
            type="text"
            id="newDocumentTitle"
            class="form-control"
            placeholder="Enter a title, such as 'Cloud Computing'"
            required
            bind:value={title}
          />
        </div>

        <div class="mb-4">
          <label for="newDocumentBody" class="form-label">
            <small>Body</small>
          </label>
          <textarea
            class="form-control"
            id="newDocumentBody"
            placeholder="Enter body content, such as 'Cloud computing refers to...'"
            required
            rows="4"
            bind:value={body}
          />
        </div>
      </div>

      <div class="modal-footer text-bg-light">
        <button type="submit" class="btn btn-success">Save Document</button>

        <button type="button" class="btn btn-secondary" on:click={onClose}>
          Cancel
        </button>
      </div>
    </div>
  </form>
</div>

<style>
  .modal {
    background: rgba(0, 0, 0, 0.5);
  }
</style>
