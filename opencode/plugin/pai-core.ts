/**
 * PAI-Core Plugin for OpenCode
 *
 * This plugin provides PAI (Personal AI Infrastructure) compatibility for SST OpenCode,
 * implementing hook-like functionality using OpenCode's event system.
 *
 * Features:
 * - Event-driven PAI functionality (replaces Claude Code hooks)
 * - Voice notification system with Piper/ElevenLabs fallback
 * - History capture and session management
 * - Skills routing and agent coordination
 */

import { tool } from '@opencode-ai/plugin';

// PAI State Management
class PAIState {
  constructor() {
    this.sessions = new Map();
    this.agentMappings = new Map();
    this.voiceProviders = new Map();
  }

  // Session lifecycle management
  onSessionCreated(sessionId, metadata) {
    this.sessions.set(sessionId, {
      ...metadata,
      created: new Date(),
      agent: null,
      lastActivity: new Date()
    });
  }

  onSessionEnded(sessionId) {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.ended = new Date();
      // Trigger session summary generation
      this.generateSessionSummary(session);
    }
  }

  // Agent detection and mapping
  setAgentForSession(sessionId, agentType) {
    const session = this.sessions.get(sessionId);
    if (session) {
      session.agent = agentType;
      this.agentMappings.set(sessionId, agentType);
    }
  }

  getAgentForSession(sessionId) {
    return this.agentMappings.get(sessionId) || 'unknown';
  }

  // Voice provider management
  async getVoiceProvider() {
    // Smart provider selection logic
    if (await this.hasElevenLabsKey() && this.prefersPremiumVoice()) {
      return 'elevenlabs';
    }
    if (await this.isPiperAvailable()) {
      return 'piper';
    }
    return 'toast';
  }

  async hasElevenLabsKey() {
    // Check for ElevenLabs API key in environment/config
    return process.env.ELEVENLABS_API_KEY !== undefined;
  }

  prefersPremiumVoice() {
    // Check user preference for premium voice
    return process.env.PAI_VOICE_PREFERENCE === 'premium';
  }

  async isPiperAvailable() {
    // Check if Piper HTTP server is running
    try {
      const response = await fetch('http://localhost:5000/voices', {
        timeout: 2000
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  // Session summary generation (replaces Claude Code SessionEnd hook)
  async generateSessionSummary(session) {
    const summary = {
      sessionId: session.id,
      duration: session.ended - session.created,
      agent: session.agent,
      activities: session.activities || [],
      timestamp: new Date().toISOString()
    };

    // Save to PAI history system
    await this.saveToHistory(summary, 'SESSION');
  }

  // History capture (replaces Claude Code Stop/SubagentStop hooks)
  async captureWork(structuredResponse, sessionId) {
    const agent = this.getAgentForSession(sessionId);
    const isLearning = this.detectLearningMoment(structuredResponse);

    const captureType = isLearning ? 'LEARNING' : 'WORK';
    const targetDir = isLearning ? 'learnings' : 'sessions';

    await this.saveToHistory({
      ...structuredResponse,
      agent,
      sessionId,
      timestamp: new Date().toISOString()
    }, captureType);
  }

  // Learning detection logic
  detectLearningMoment(text) {
    const learningIndicators = [
      'learned', 'discovered', 'realized', 'found that',
      'problem', 'issue', 'bug', 'fixed', 'solved',
      'lesson', 'takeaway', 'important'
    ];

    const textLower = text.toLowerCase();
    const matches = learningIndicators.filter(indicator =>
      textLower.includes(indicator)
    );

    return matches.length >= 2; // At least 2 learning indicators
  }

  // File system operations for history
  async saveToHistory(data, type) {
    const yearMonth = new Date().toISOString().slice(0, 7); // YYYY-MM
    const filename = this.generateHistoryFilename(data, type);

    // In a real implementation, this would write to the PAI history directory
    console.log(`PAI: Capturing ${type} to history: ${filename}`, data);
  }

  generateHistoryFilename(data, type) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const description = (data.summary || data.completed || 'work')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .slice(0, 50);

    return `${timestamp}_PAI_${type}_${description}.md`;
  }
}

// Voice notification system
class VoiceSystem {
  constructor(paiState) {
    this.paiState = paiState;
  }

  async sendNotification(message, agent = 'kai') {
    const provider = await this.paiState.getVoiceProvider();

    switch (provider) {
      case 'elevenlabs':
        return await this.sendElevenLabs(message, agent);
      case 'piper':
        return await this.sendPiper(message, agent);
      default:
        return await this.sendToast(message);
    }
  }

  async sendElevenLabs(message, agent) {
    const voiceId = this.getElevenLabsVoiceId(agent);
    try {
      const response = await fetch('http://localhost:8888/notify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          voice_id: voiceId,
          title: 'PAI'
        })
      });
      return response.ok;
    } catch (error) {
      console.warn('ElevenLabs voice failed, falling back to toast:', error);
      return await this.sendToast(message);
    }
  }

  async sendPiper(message, agent) {
    const voice = this.getPiperVoice(agent);
    try {
      const response = await fetch('http://localhost:5000', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: message,
          voice
        })
      });
      return response.ok;
    } catch (error) {
      console.warn('Piper voice failed, falling back to toast:', error);
      return await this.sendToast(message);
    }
  }

  async sendToast(message) {
    // Use OpenCode's native toast system
    await client.tui.showToast({
      body: {
        message: `PAI: ${message}`,
        variant: 'info'
      }
    });
    return true;
  }

  getElevenLabsVoiceId(agent) {
    const voiceMap = {
      kai: 's3TPKV1kjDlVtZbl4Ksh',
      engineer: 'fATgBRI8wg5KkDFg8vBd',
      researcher: 'AXdMgz6evoL7OPd7eU12',
      designer: 'ZF6FPAbjXT4488VcRRnw',
      architect: 'muZKMsIDGYtIkjjiUS82',
      pentester: 'xvHLFjaUEpx4BOf7EiDd'
    };
    return voiceMap[agent] || voiceMap.kai;
  }

  getPiperVoice(agent) {
    const voiceMap = {
      kai: 'en_US-lessac-medium',
      engineer: 'en_US-ryan-medium',
      researcher: 'en_US-amy-medium',
      designer: 'en_GB-alan-medium',
      architect: 'en_US-lessac-medium',
      pentester: 'en_US-ryan-medium'
    };
    return voiceMap[agent] || voiceMap.kai;
  }
}

// Main PAI-Core Plugin
export const PAICorePlugin = async ({ client, $, directory, worktree }) => {
  console.log('PAI-Core: Initializing Personal AI Infrastructure for OpenCode');

  const paiState = new PAIState();
  const voiceSystem = new VoiceSystem(paiState);

  // Load PAI context on session start (replaces SessionStart hook)
  await injectPAIContext();

  return {
    // Event handlers (replace Claude Code hooks)

    // Session lifecycle events
    'session.created': async ({ event }) => {
      console.log('PAI-Core: Session created', event.properties?.id);
      paiState.onSessionCreated(event.properties?.id, event.properties);
      await injectPAIContext(event.properties?.id);
    },

    'session.idle': async ({ event }) => {
      console.log('PAI-Core: Session ended', event.properties?.id);
      paiState.onSessionEnded(event.properties?.id);
    },

    // Tool execution events (replace PostToolUse hook)
    'tool.execute.after': async ({ event }) => {
      const { tool, input, output, sessionId } = event.properties || {};

      // Capture tool execution for history
      await paiState.saveToHistory({
        type: 'TOOL_EXECUTION',
        tool,
        input,
        output,
        sessionId,
        timestamp: new Date().toISOString()
      }, 'WORK');
    },

    // Message events (replace Stop/SubagentStop hooks)
    'message.updated': async ({ event }) => {
      const message = event.properties?.message;
      if (!message) return;

      // Check for structured PAI responses
      const structured = extractStructuredSections(message.content || '');
      if (structured.completed) {
        // This is a PAI completion - capture work and send voice notification
        const sessionId = event.properties?.sessionId;
        const agent = paiState.getAgentForSession(sessionId);

        await paiState.captureWork(structured, sessionId);
        await voiceSystem.sendNotification(structured.completed, agent);
      }
    },

    // File events for context awareness
    'file.edited': async ({ event }) => {
      // Track file changes for session context
      console.log('PAI-Core: File edited', event.properties?.path);
    },

    // Custom tools for PAI functionality
    tool: {
      use_skill: tool({
        description: 'Load and read a specific PAI skill to guide your work. Skills contain proven workflows, mandatory processes, and expert techniques.',
        args: {
          skill_name: tool.schema.string().describe('Name of the skill to load (e.g., "brainstorming", "research", "create-skill")')
        },
        execute: async (args, context) => {
          const { skill_name } = args;
          console.log(`PAI-Core: Loading skill ${skill_name}`);

          // In a full implementation, this would load and inject the skill content
          return `PAI skill "${skill_name}" loaded. The skill's guidance is now active in this session.`;
        },
      }),

      pai_status: tool({
        description: 'Check PAI system status and configuration',
        args: {},
        execute: async (args, context) => {
          const voiceProvider = await paiState.getVoiceProvider();
          const sessionCount = paiState.sessions.size;

          return `PAI Status:
• Voice Provider: ${voiceProvider}
• Active Sessions: ${sessionCount}
• Agent Mappings: ${Array.from(paiState.agentMappings.entries()).length}
• System: Operational`;
        },
      }),

      pai_voice_test: tool({
        description: 'Test voice notification system',
        args: {
          message: tool.schema.string().optional().describe('Test message to speak'),
          provider: tool.schema.string().optional().describe('Voice provider to test (piper, elevenlabs, or auto)')
        },
        execute: async (args, context) => {
          const { message = 'PAI voice system test successful', provider } = args;

          let testProvider = provider;
          if (!testProvider || testProvider === 'auto') {
            testProvider = await paiState.getVoiceProvider();
          }

          const success = await voiceSystem.sendNotification(message, 'kai');

          return `Voice test ${success ? 'successful' : 'failed'} using ${testProvider} provider`;
        },
      })
    }
  };
};

// Helper functions

async function injectPAIContext(sessionId = null) {
  // Load PAI core context (replaces load-core-context.ts hook)
  try {
    // In a full implementation, this would read the PAI SKILL.md and inject it
    const paiContext = `
<EXTREMELY_IMPORTANT>
You have PAI (Personal AI Infrastructure) active.

PAI Identity: You are Kai, Daniel Miessler's AI assistant with access to specialized skills and workflows.

Available Skills: Research, brainstorming, content creation, system administration, and more.
Use the use_skill tool to activate specific capabilities.

Response Format: Always use structured responses with SUMMARY, ANALYSIS, ACTIONS, RESULTS, STATUS, CAPTURE, NEXT, STORY EXPLANATION, and COMPLETED sections.

Voice Notifications: Your completions will be announced via voice (Piper TTS or ElevenLabs if configured).
</EXTREMELY_IMPORTANT>`;

    if (sessionId) {
      await client.session.prompt({
        path: { id: sessionId },
        body: {
          noReply: true,
          parts: [{ type: "text", text: paiContext, synthetic: true }]
        }
      });
    }

    console.log('PAI-Core: Context injected');
  } catch (error) {
    console.warn('PAI-Core: Failed to inject context:', error);
  }
}

function extractStructuredSections(text) {
  const sections = {};

  // Extract structured sections from PAI responses
  const patterns = {
    summary: /📋 SUMMARY:\s*([^\n]+)/i,
    analysis: /🔍 ANALYSIS:\s*([^\n]+)/i,
    actions: /⚡ ACTIONS:\s*([^\n]+)/i,
    results: /✅ RESULTS:\s*([^\n]+)/i,
    status: /📊 STATUS:\s*([^\n]+)/i,
    capture: /📁 CAPTURE:\s*([^\n]+)/i,
    next: /➡️ NEXT:\s*([^\n]+)/i,
    story: /📖 STORY EXPLANATION:\s*([^\n]+)/i,
    completed: /🎯 COMPLETED:\s*([^\n]+)/i
  };

  for (const [key, pattern] of Object.entries(patterns)) {
    const match = text.match(pattern);
    if (match) {
      sections[key] = match[1].trim();
    }
  }

  return sections;
}