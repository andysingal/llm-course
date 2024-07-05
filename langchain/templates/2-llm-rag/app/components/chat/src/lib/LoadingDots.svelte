<script lang="ts">
  // https://css-loaders.com/dots/
</script>

<div class="loader-wrapper">
  <div class="loader"></div>
</div>

<style>
  .loader-wrapper {
    padding-left: 12px;
  }

  .loader {
    width: 7px;
    aspect-ratio: 1;
    border-radius: 50%;
    animation: l5 1s infinite linear alternate;
  }
  @keyframes l5 {
    0% {
      box-shadow:
        10px 0 #000,
        -10px 0 #0002;
      background: #000;
    }
    33% {
      box-shadow:
        10px 0 #000,
        -10px 0 #0002;
      background: #0002;
    }
    66% {
      box-shadow:
        10px 0 #0002,
        -10px 0 #000;
      background: #0002;
    }
    100% {
      box-shadow:
        10px 0 #0002,
        -10px 0 #000;
      background: #000;
    }
  }
</style>
