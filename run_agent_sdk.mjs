import { query } from "@anthropic-ai/claude-agent-sdk";

function emitJson(obj) {
  try { process.stdout.write(JSON.stringify(obj) + "\n"); } catch (err) {}
}

const mcpUrl = process.env.MCP_URL;
const serverName = process.env.MCP_SERVER_NAME;
const apiKey = process.env.DATAGEN_API_KEY;
const resumeSessionId = process.env.RESUME_SESSION_ID || undefined;
const forkSession = process.env.FORK_SESSION === "1";

const options = {
  allowedTools: ["mcp__" + serverName + "__*"],
  mcpServers: {
    [serverName]: {
      type: "http",
      url: mcpUrl,
      headers: apiKey ? { "x-api-key": apiKey } : undefined,
    },
  },
  permissionMode: "acceptEdits",
  stderr: (data) => emitJson({ type: "sdk_stderr", data }),
  ...(resumeSessionId ? { resume: resumeSessionId } : {}),
  ...(forkSession ? { forkSession: true } : {}),
};

let sessionId = null;
let resultText = "";

try {
  for await (const message of query({ prompt: process.env.PROMPT || "Say ok.", options })) {
    emitJson(message);
    if (message?.type === "system" && message?.subtype === "init" && message.session_id) {
      sessionId = message.session_id;
    }
    if (message?.type === "result") {
      if (message.session_id) sessionId = message.session_id;
      resultText = typeof message.result === "string" ? message.result : JSON.stringify(message.result ?? null);
    }
  }
} catch (err) {
  emitJson({ type: "error", error: err?.message ?? String(err), stack: err?.stack ?? null, phase: "query" });
  process.exit(1);
}

emitJson({ type: "sdk_summary", session_id: sessionId, result_length: resultText.length });

