/**
 * PAI-Adapter for OpenCode (v0.9.1 Compliant)
 * 
 * This adapter bridges OpenCode and the Personal AI Infrastructure (PAI).
 * It enables native skill discovery, history capture, and voice notifications.
 */

import { tool } from '@opencode-ai/plugin';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

// Path Configuration
const PAI_WORKSPACE = path.join(os.homedir(), 'Workspaces', 'pai-opencode');
const SETTINGS_FILE = path.join(PAI_WORKSPACE, 'settings.json');

// PAI State Management
class PAIState {
  paiDir = PAI_WORKSPACE;
  sessions = new Map();

  async initialize() {
    try {
      const settingsRaw = await fs.readFile(SETTINGS_FILE, 'utf-8');
      const settings = JSON.parse(settingsRaw);
      if (settings.PAI_DIR) {
        this.paiDir = settings.PAI_DIR;
      }
    } catch (e) {
      // Fallback
    }
  }

  async captureWork(structuredResponse, sessionId) {
    const isLearning = this.detectLearningMoment(structuredResponse.completed);
    const type = isLearning ? 'LEARNING' : 'WORK';
    await this.saveToHistory(structuredResponse, type, sessionId);
  }

  detectLearningMoment(text) {
    if (!text || typeof text !== 'string') return false;
    const indicators = ['learned', 'discovered', 'realized', 'bug', 'fixed', 'lesson'];
    const textLower = text.toLowerCase();
    const matches = indicators.filter(i => textLower.includes(i));
    return matches.length >= 2;
  }

  async saveToHistory(data, type, sessionId) {
    const historyDir = path.join(this.paiDir, 'Memories', type === 'LEARNING' ? 'learnings' : 'sessions');
    const now = new Date();
    const yearMonth = now.toISOString().slice(0, 7);
    const organizedDir = path.join(historyDir, yearMonth);

    try {
      await fs.mkdir(organizedDir, { recursive: true });
      const filename = `${now.toISOString().replace(/[:.]/g, '-')}_PAI_${type}.md`;
      const filePath = path.join(organizedDir, filename);

      const b = String.fromCharCode(96);
      const content = `---` +
`type: ${type}
` +
`timestamp: ${now.toISOString()}
` +
`sessionId: ${sessionId}
` +
`---
` +
`# ${type} Capture

` +
`## Summary
` + (data.summary || 'N/A') + `

` +
`## Completed
` + (data.completed || 'N/A') + `

` +
`## Raw
` + `${b}${b}${b}json
` + `${JSON.stringify(data, null, 2)}
` + `${b}${b}${b}`;

      await fs.writeFile(filePath, content, 'utf-8');
    } catch (err) {
      console.error(`PAI-Adapter: History capture failed: ${err.message}`);
    }
  }

  async isPiperAvailable() {
    try {
      const response = await fetch('http://localhost:5000/voices', { signal: AbortSignal.timeout(1000) });
      return response.ok;
    } catch {
      return false;
    }
  }
}

class VoiceSystem {
  constructor(paiState, client) {
    this.paiState = paiState;
    this.client = client;
  }

  async sendNotification(message) {
    if (await this.paiState.isPiperAvailable()) {
      await this.sendPiper(message);
    } else {
      await this.sendToast(message);
    }
  }

  async sendPiper(message) {
    try {
      const response = await fetch('http://localhost:5000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message, voice: 'en_US-lessac-medium' })
      });
      if (response.ok) {
        const audioBuffer = await response.arrayBuffer();
        const tempFile = path.join(os.tmpdir(), `pai-voice-${Date.now()}.wav`);
        await fs.writeFile(tempFile, Buffer.from(audioBuffer));
        const player = process.platform === 'darwin' ? 'afplay' : 'aplay';
        await execAsync(`${player} ${tempFile}`);
        await fs.unlink(tempFile);
      }
    } catch (e) {
      await this.sendToast(message);
    }
  }

  async sendToast(message) {
    if (this.client?.tui?.showToast) {
      await this.client.tui.showToast({ body: { message: `PAI: ${message}`, variant: 'info' } });
    }
  }
}

export const PAICorePlugin = async ({ client }) => {
  const state = new PAIState();
  await state.initialize();
  const voice = new VoiceSystem(state, client);

  return {
    event: async ({ event }) => {
      if (event.type === 'session.idle') {
        const sessionId = event.properties?.sessionID || (client.session && client.session.id);
        if (!sessionId) return;

        try {
          const result = await client.session.messages({ path: { id: sessionId } });
          const lastMsg = result.data?.[result.data.length - 1];
          if (lastMsg?.info?.role === 'assistant') {
            const content = lastMsg.parts.filter(p => p.type === 'text').map(p => p.text).join('');
            if (content.match(/COMPLETED:/i)) {
              const sections = extractSections(content);
              if (sections.completed) {
                await state.captureWork(sections, sessionId);
                await voice.sendNotification(sections.completed);
              }
            }
          }
        } catch (err) {}
      }
    },
    tool: {
      pai_status: tool({
        description: 'Check PAI adapter status',
        args: {},
        execute: async () => {
          const piper = await state.isPiperAvailable();
          return `PAI Adapter: Operational\nWorkspace: ${state.paiDir}\nPiper TTS: ${piper ? 'Online' : 'Offline'}`;
        }
      })
    }
  };
};

function extractSections(text) {
  const sections = {};
  const patterns = {
    summary: /📋 SUMMARY:\s*([^\n]+)/i,
    completed: /🎯 COMPLETED:\s*([\s\S]+)/i
  };
  for (const [key, pattern] of Object.entries(patterns)) {
    const match = text.match(pattern);
    if (match) sections[key] = match[1].trim();
  }
  return sections;
}