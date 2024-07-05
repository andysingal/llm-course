import "./app.css";
import App from "./App.svelte";

const appElement = document.getElementById("app")!;
const chat = JSON.parse(appElement.dataset.chat) || {};

const app = new App({
  target: appElement,
  props: {
    initialChatState: chat,
  },
});

export default app;
