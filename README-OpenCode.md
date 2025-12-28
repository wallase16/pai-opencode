# PAI OpenCode - Personal AI Infrastructure for SST OpenCode

[![OpenCode Compatible](https://img.shields.io/badge/OpenCode-Compatible-blue)](https://opencode.ai)
[![Piper TTS](https://img.shields.io/badge/Voice-Piper-green)](https://github.com/OHF-Voice/piper1-gpl)
[![ElevenLabs TTS](https://img.shields.io/badge/Voice-ElevenLabs-purple)](https://elevenlabs.io)

> **PAI (Personal AI Infrastructure) fork with integrated SST OpenCode compatibility**

PAI OpenCode brings Daniel Miessler's sophisticated personal AI infrastructure to SST OpenCode, with seamless integration and free voice notifications out-of-the-box.

## 🚀 Quick Start

### One-Click Installation

```bash
# Clone this repository
git clone https://github.com/your-org/pai-opencode.git
cd pai-opencode

# Run the one-click installer
./opencode/scripts/install.sh
```

That's it! PAI is now fully configured for OpenCode.

### Start Using PAI

```bash
# Start OpenCode with PAI
opencode

# PAI is automatically active - try these commands:
use_skill brainstorming
pai_status
pai_voice_test
```

## 🎯 What is PAI?

PAI (Personal AI Infrastructure) is a comprehensive AI assistant system featuring:

- **Skills Architecture**: Specialized AI capabilities (research, brainstorming, content creation, etc.)
- **Voice Notifications**: Audio feedback for task completions
- **History Capture**: Automatic documentation of work and learnings
- **Agent Coordination**: Multi-agent task delegation
- **Structured Responses**: Consistent, parseable AI outputs

## 🆚 PAI OpenCode vs Original PAI

| Feature | Original PAI (Claude Code) | PAI OpenCode |
|---------|---------------------------|--------------|
| **Platform** | Claude Code only | SST OpenCode |
| **Voice System** | ElevenLabs only | Piper (free) + ElevenLabs (premium) |
| **Setup** | Manual configuration | One-click installation |
| **Event System** | Native hooks | Plugin-based events |
| **Cost** | API keys required | Free voice notifications |

## 🗣️ Voice System

PAI OpenCode includes a smart voice system with multiple options:

### Free Option: Piper TTS
- **Cost**: $0 forever
- **Quality**: Very good neural voices
- **Offline**: Works without internet
- **Setup**: Automatic during installation

### Premium Option: ElevenLabs TTS
- **Cost**: $5/month minimum
- **Quality**: Studio-grade voices
- **Offline**: Requires internet
- **Setup**: Add `ELEVENLABS_API_KEY` to environment

### Smart Fallback
The system automatically chooses the best available option:
1. ElevenLabs (if API key configured and preferred)
2. Piper (free, local)
3. OpenCode toasts (text notifications)

## 🛠️ PAI Skills

Access PAI's extensive skill library:

### Core Skills
- `brainstorming` - Structured ideation and planning
- `research` - Multi-source research workflows
- `create-skill` - Templates for building new skills
- `story-explanation` - Narrative generation
- `ffuf` - Web security testing
- `fabric` - AI pattern integration

### Usage
```bash
# Load a skill
use_skill brainstorming

# Check available skills
find_skills

# Get PAI status
pai_status
```

## 📊 System Monitoring

### Health Check
```bash
# Run comprehensive health check
./opencode/scripts/health-check.sh
```

### Voice Testing
```bash
# Test voice notifications
pai_voice_test

# Test specific provider
pai_voice_test --provider piper
pai_voice_test --provider elevenlabs
```

## 🔧 Configuration

### Voice Preferences

Set your voice preference in your environment:

```bash
# Prefer premium voice (requires ElevenLabs API key)
export PAI_VOICE_PREFERENCE=premium

# Use free voice (default)
export PAI_VOICE_PREFERENCE=free
```

### ElevenLabs Setup (Optional)

For premium voice quality:

```bash
# Get API key from https://elevenlabs.io
export ELEVENLABS_API_KEY=your_api_key_here
export ELEVENLABS_VOICE_ID=s3TPKV1kjDlVtZbl4Ksh
```

## 📁 Project Structure

```
pai-opencode/
├── .claude/                    # Original PAI (Claude Code compatible)
│   ├── skills/                # All PAI skills
│   ├── hooks/                 # Claude Code hooks (compatibility)
│   └── history/               # PAI history system
├── opencode/                  # OpenCode enhancements
│   ├── plugin/
│   │   └── pai-core.ts        # Main OpenCode plugin
│   ├── voices/                # Piper configuration
│   │   ├── models/            # Voice model storage
│   │   └── config.json        # Provider settings
│   └── scripts/               # Setup utilities
│       ├── install.sh         # One-click setup
│       └── health-check.sh    # System verification
├── docs/                      # Documentation
└── README-OpenCode.md         # This file
```

## 🔄 Staying Updated

PAI OpenCode includes automated sync with the upstream PAI repository:

```bash
# Sync with latest PAI developments
./scripts/sync-from-upstream.sh
```

## 🐛 Troubleshooting

### Voice Issues
```bash
# Check voice server status
curl http://localhost:5000/voices

# Restart voice server
pkill -f piper.http_server
./opencode/scripts/install.sh  # Reinstall will restart services
```

### Plugin Issues
```bash
# Check OpenCode plugin loading
opencode  # Look for PAI initialization messages

# Verify plugin installation
ls -la ~/.config/opencode/plugin/pai-core.ts
```

### Common Issues

**"PAI commands not found"**
- Run health check: `./opencode/scripts/health-check.sh`
- Reinstall: `./opencode/scripts/install.sh`

**"Voice not working"**
- Check Piper server: `curl http://localhost:5000/voices`
- Test manually: `pai_voice_test`

**"Skills not loading"**
- Verify installation: `./opencode/scripts/health-check.sh`
- Check OpenCode logs for errors

## 📚 Documentation

- [PAI Constitution](.claude/skills/CORE/CONSTITUTION.md) - System philosophy
- [Skills Guide](.claude/skills/CORE/SKILL-STRUCTURE-AND-ROUTING.md) - Creating skills
- [Voice Guide](docs/voice-options.md) - Voice system details
- [Migration Guide](docs/migration-guide.md) - From Claude Code PAI

## 🤝 Contributing

PAI OpenCode is community-driven:

1. **Issues**: Report bugs or OpenCode-specific problems
2. **PRs**: Improve OpenCode compatibility or add features
3. **Discussions**: Share your PAI OpenCode workflows

## 📄 License

This fork maintains the same license as the original PAI repository.

## 🙏 Acknowledgments

- **Daniel Miessler** - Original PAI architecture and philosophy
- **SST Team** - OpenCode platform enabling this integration
- **OHF Voice** - Piper TTS making free voice possible
- **ElevenLabs** - Premium voice option

---

**Start clean. Start small. Build the AI infrastructure you need.**

With PAI OpenCode, that infrastructure is now available to everyone on SST OpenCode.