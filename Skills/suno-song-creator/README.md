# Suno Song Creator - PAI Skill

AI-powered music generation using Suno's platform with Chrome MCP browser automation.

## Quick Start

### Generate a Single Song
```bash
# Via AI assistant
"Generate a song with lyrics about summer nights in upbeat pop style"
```

### Process Multiple Songs
```bash
# Prepare CSV file (see assets/csv-template.csv)
# Via AI assistant
"Process this CSV file for batch song generation: songs.csv"
```

### Manage Downloads
```bash
# Via AI assistant
"Download and organize my generated songs"
```

## Architecture

This skill follows PAI v1.2.0's Skills-as-Containers pattern:

- **`workflows/`**: Task-specific implementations
  - `generate-song.md` - Single song creation
  - `batch-process.md` - CSV bulk processing
  - `manage-downloads.md` - File organization

- **`assets/`**: Templates and examples
  - `lyrics-templates.md` - Songwriting templates
  - `style-examples.md` - Genre/style guides
  - `csv-template.csv` - Batch processing format

- **`scripts/`**: Implementation files
  - `suno_chrome_creator.py` - Python utilities
  - `download_script.sh` - File handling

## Requirements

- **Chrome Browser**: Running with chrome-mcp tools
- **Suno Account**: Active with available credits
- **Internet Connection**: For AI generation
- **PAI Environment**: With chrome-mcp integration

## Usage Examples

### Basic Song Generation
```
User: "Create a pop song about falling in love"
AI: Activates generate-song workflow
Result: Share links and download options
```

### Batch Processing
```
User: "Generate songs from this CSV file"
AI: Activates batch-process workflow
Result: Updated CSV with all share links
```

### File Management
```
User: "Organize my downloaded songs"
AI: Activates manage-downloads workflow
Result: Structured music library
```

## Features

- ✅ **Single Song Creation**: Custom lyrics and styles
- ✅ **Batch Processing**: CSV-driven bulk generation
- ✅ **Download Management**: Automatic file organization
- ✅ **Chrome MCP Integration**: No puppeteer dependencies
- ✅ **Error Handling**: Robust failure recovery
- ✅ **Progress Monitoring**: Real-time status updates

## File Structure

```
suno-song-creator/
├── SKILL.md              # Core skill definition
├── CLAUDE.md             # Comprehensive documentation
├── workflows/            # Task workflows
├── assets/               # Templates & examples
├── scripts/              # Implementation files
└── README.md             # This file
```

## Integration

### PAI Ecosystem
- **Natural Language**: Activates via conversational triggers
- **Multi-Agent**: Coordinates with research/creative agents
- **Hooks**: Automates post-generation tasks
- **Voice**: Optional audio notifications

### Chrome MCP Tools
- **Navigation**: Direct browser control
- **Form Interaction**: Precise element manipulation
- **Content Monitoring**: Real-time progress tracking
- **Download Handling**: Automated file retrieval

## Support

### Documentation
- `SKILL.md` - Quick reference and routing
- `CLAUDE.md` - Technical implementation details
- `workflows/` - Step-by-step task guides
- `assets/` - Templates and examples

### Troubleshooting
- Check Chrome browser status
- Verify Suno account and credits
- Review network connectivity
- Consult CLAUDE.md for detailed debugging

## Contributing

This skill follows PAI's Skills-as-Containers architecture. To extend:

1. Add new workflows in `workflows/`
2. Create supporting assets in `assets/`
3. Update SKILL.md with new triggers
4. Document in CLAUDE.md

---

**Built with PAI v1.2.0 Skills-as-Containers architecture**