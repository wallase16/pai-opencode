---
type: LEARNING
timestamp: 2025-12-07T06:35:00Z
tags: [pai, opencode, plugin, debugging, voice]
---

# PAI OpenCode Plugin: COMPLETED Trigger Fix & Architecture

## 1. The Issue
The PAI OpenCode plugin is designed to automatically announce task completion via voice when the AI generates a message containing `COMPLETED: ...`. While the manual `announce_completion` tool worked, the automatic trigger inside the `session.idle` event handler was failing silently.

## 2. Root Cause Analysis
Extensive debug logging revealed two primary issues:

### A. SDK Response Structure
The primary failure was in how the plugin retrieved session messages.
- **Code Assumption:** `client.session.messages(...)` returns an array of messages `Message[]`.
- **Actual Behavior:** The OpenCode SDK returns an object wrapper `{ data: Message[] }`.
- **Impact:** Accessing `messagesResult.length` returned `undefined`, causing the logic to assume no messages existed or to fail when checking the last message.

### B. Voice Server Reliability
The `piper-server.js` (local TTS server) was occasionally failing to start or stay running in the background, preventing the audio request even if the trigger had fired.

## 3. The Fix

### Plugin Code Update (`pai-core.ts`)
We updated the message retrieval logic to correctly access the `.data` property:
```typescript
const messagesResult = await client.session.messages({ path: { id: sessionId } });
const messages = messagesResult.data || []; // The Fix
const lastEntry = messages[messages.length - 1];
```
We also relaxed the regex trigger to be case-insensitive and not require the specific `🎯` emoji, improving robustness.

### Tool Cleanup
The `announce_completion` tool, which served as a manual retrofit/workaround, was completely removed to ensure reliance on the corrected automatic behavior.

## 4. Current Architecture: How It Runs

The automated voice notification system now operates as follows:

1.  **Event Emission:**
    - The LLM finishes a response.
    - OpenCode emits a `session.idle` event.

2.  **Plugin Handling (`pai-core.ts`):**
    - The plugin captures `session.idle`.
    - It extracts the `sessionID`.
    - It queries the OpenCode API for the full message history of that session.

3.  **Trigger Detection:**
    - The plugin inspects the text of the **last message**.
    - It looks for the pattern `COMPLETED:` (case-insensitive).
    - **Extraction:** If found, it parses the text following the marker.

4.  **Voice Notification:**
    - The plugin calls `voiceSystem.sendNotification()`.
    - **Piper Check:** It pings `http://localhost:5000/voices`.
    - **Request:** It sends a POST request with the text to `http://localhost:5000`.

5.  **Audio Playback:**
    - `piper-server.js` generates a WAV file using the local ONNX model.
    - The plugin receives the audio buffer.
    - It saves it to a temp file (e.g., `/tmp/pai-voice-....wav`).
    - It executes `aplay` (Linux) or `afplay` (macOS) to play the file immediately.

## 5. Verification
- **Debug Log:** `/tmp/pai-debug.log` now confirms successful `FOUND COMPLETED` triggers.
- **Audio:** Voice announcements play automatically upon completion.

## 6. Format Cleanup
- **Finding:** The `announce_completion` tool reference in the PAI response format was identified as a leftover from development, not part of the initial repository.
- **Correction:** Removed the redundant `⚡ TOOL: announce_completion...` line from the mandatory response format specification.
- **Rationale:** The automatic COMPLETED trigger now handles voice notifications without requiring manual tool intervention, eliminating the development workaround.
