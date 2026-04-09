// KDrama IA - Vue 3 Chat App with streaming thinking
const { createApp, ref, reactive, nextTick } = Vue;

createApp({
  setup() {
    const messages = reactive([]);
    const input = ref("");
    const loading = ref(false);
    const chatContainer = ref(null);
    const inputEl = ref(null);
    const provider = ref("ollama");
    const providers = reactive([]);
    const tokens = reactive({ input: 0, output: 0, thinking: 0 });

    fetch("/api/providers").then((r) => r.json()).then((d) => {
      providers.push(...d.providers);
      if (d.providers.length) provider.value = d.providers[0].id;
    });

    function scrollBottom() {
      nextTick(() => {
        if (chatContainer.value) chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
      });
    }

    function formatArgs(args) {
      if (!args) return "";
      return Object.entries(args).map(([k, v]) => `${k}="${v}"`).join(", ");
    }

    function renderMd(text) {
      if (!text) return "";
      return marked.parse(text);
    }

    function getCurrentCycle(msg, cycleNum) {
      let cycle = msg.cycles.find((c) => c.number === cycleNum);
      if (!cycle) {
        cycle = reactive({
          number: cycleNum,
          thinking: "",
          thinkingDone: false,
          contentChunks: "",
          toolName: "",
          toolArgs: null,
          collapsed: false,
        });
        msg.cycles.push(cycle);
      }
      return cycle;
    }

    async function send() {
      const text = input.value.trim();
      if (!text || loading.value) return;

      messages.push({ role: "user", text });
      input.value = "";
      loading.value = true;

      const msg = reactive({
        role: "assistant",
        text: "",
        cycles: [],
        cards: [],
        streaming: true,
      });
      messages.push(msg);
      scrollBottom();

      const history = messages
        .filter((m) => m.text && (m.role === "user" || (m.role === "assistant" && !m.streaming)))
        .slice(0, -1)
        .map((m) => ({ role: m.role === "user" ? "user" : "assistant", content: m.text }));

      try {
        const res = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text, history, provider: provider.value }),
        });

        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          const lines = buffer.split("\n");
          buffer = lines.pop();

          let evtName = "";
          for (const line of lines) {
            if (line.startsWith("event: ")) {
              evtName = line.slice(7).trim();
            } else if (line.startsWith("data: ") && evtName) {
              try {
                const data = JSON.parse(line.slice(6));
                handleEvent(msg, evtName, data);
              } catch {}
              evtName = "";
            }
          }
          scrollBottom();
        }
      } catch (err) {
        msg.text = `Erro: ${err.message}`;
      }

      msg.streaming = false;
      loading.value = false;
      for (const c of msg.cycles) c.collapsed = true;
      nextTick(() => inputEl.value?.focus());
      scrollBottom();
    }

    function handleEvent(msg, event, data) {
      switch (event) {
        case "cycle_start": {
          getCurrentCycle(msg, data.cycle);
          break;
        }
        case "thinking_token": {
          const cycle = getCurrentCycle(msg, data.cycle);
          cycle.thinking += data.token;
          break;
        }
        case "thinking_done": {
          const cycle = getCurrentCycle(msg, data.cycle);
          cycle.thinking = data.text;
          cycle.thinkingDone = true;
          break;
        }
        case "content_token": {
          msg.text += data.token;
          break;
        }
        case "tool_call": {
          const cycle = getCurrentCycle(msg, data.cycle);
          cycle.toolName = data.name;
          cycle.toolArgs = data.args;
          break;
        }
        case "drama_cards": {
          msg.cards.push(...data.cards);
          break;
        }
        case "response": {
          if (!msg.text) msg.text = data.text;
          break;
        }
        case "tokens": {
          tokens.input = data.input || 0;
          tokens.output = data.output || 0;
          tokens.thinking = data.thinking || 0;
          break;
        }
        case "error": {
          msg.text = `Erro: ${data.message}`;
          break;
        }
      }
    }

    return { messages, input, loading, chatContainer, inputEl, provider, providers, tokens, send, formatArgs, renderMd };
  },
}).mount("#app");
