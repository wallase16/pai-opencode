# Suno Song Creator - Comprehensive Implementation Guide

## Overview

This skill provides complete AI-powered music generation using Suno's platform through Chrome MCP browser automation. It follows PAI v1.2.0's Skills-as-Containers architecture with specialized workflows for different use cases.

## Architecture

### Skills-as-Containers Structure
```
suno-song-creator/
├── SKILL.md              # Core definition and routing
├── CLAUDE.md             # This comprehensive guide
├── workflows/            # Task-specific workflows
│   ├── generate-song.md
│   ├── batch-process.md
│   └── manage-downloads.md
├── assets/               # Templates and examples
│   ├── lyrics-templates.md
│   ├── style-examples.md
│   └── csv-template.csv
├── scripts/              # Implementation files
│   ├── suno_chrome_creator.py
│   └── download_script.sh
└── README.md             # Quick start guide
```

### Component Roles

- **SKILL.md**: Quick reference, activation triggers, workflow routing
- **CLAUDE.md**: Deep technical documentation, implementation details
- **workflows/**: Specific task implementations with step-by-step instructions
- **assets/**: Reusable templates, examples, and reference materials
- **scripts/**: Executable code for data processing and automation

## Chrome MCP Integration

### Current Selectors (Updated 2025)

Based on live page analysis, the following CSS selectors are used for form interaction:

```javascript
const selectors = {
    lyrics_textarea: "body > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div > div > div > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div:nth-of-type(1) > div:nth-of-type(1) > div > textarea",
    styles_textarea: "textarea[placeholder*=\"indie, electronic, synths\"]",
    song_title_input: "body > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div > div > div > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > input",
    create_button: "button[aria-label=\"Create song\"]"
};
```

**Note:** These selectors are based on Suno's current page structure. They may change with site updates and require periodic verification.

### Tool Usage Pattern

The AI assistant orchestrates all browser interactions using chrome-mcp tools:

```javascript
// Example workflow orchestration
async function generateSong(lyrics, style) {
    // 1. Environment check
    const tabs = await callTool("mcp-chrome_get_windows_and_tabs");

    // 2. Navigation
    await callTool("mcp-chrome_chrome_navigate", {
        url: "https://suno.com/create"
    });

    // 3. Scroll to form (handles dynamic page loading)
    await callTool("mcp-chrome_chrome_keyboard", {
        keys: "PageDown"
    });
    await sleep(1000); // Wait for scroll
    });

    // 3. Form interaction
    await callTool("mcp-chrome_chrome_fill_or_select", {
        selector: "textarea:first-of-type",
        value: lyrics
    });

    // 4. Generation trigger
    await callTool("mcp-chrome_chrome_click_element", {
        selector: "button:has-text('Create')"
    });

    // 5. Progress monitoring
    while (true) {
        const content = await callTool("mcp-chrome_chrome_get_web_content");
        if (content.includes("/song/")) break;
        await sleep(5000);
    }

    // 6. Result extraction (top 2 most recent songs per Suno workflow)
    const html = await callTool("mcp-chrome_chrome_get_web_content", {
        htmlContent: true
    });
    const allLinks = extractSongLinks(html);
    const topTwoLinks = allLinks.slice(0, 2); // Suno puts most recent at top
    return topTwoLinks;
}
```

### Tool Capabilities

| Tool | Purpose | Parameters |
|------|---------|------------|
| `mcp-chrome_get_windows_and_tabs` | Find browser tabs | `{}` |
| `mcp-chrome_chrome_navigate` | Navigate to URLs | `{url, newWindow}` |
| `mcp-chrome_chrome_get_web_content` | Read page content | `{textContent, htmlContent}` |
| `mcp-chrome_chrome_get_interactive_elements` | Find clickable elements | `{textQuery, includeCoordinates}` |
| `mcp-chrome_chrome_fill_or_select` | Fill form fields | `{selector, value}` |
| `mcp-chrome_chrome_click_element` | Click elements | `{selector, coordinates}` |

## Workflow Implementations

### Single Song Generation

**Trigger Phrases:**
- "generate a song"
- "create music"
- "make a track with these lyrics"

**Process Flow:**
1. Validate inputs (lyrics, style)
2. Check browser and chrome-mcp availability
3. Navigate to Suno create page
4. Verify login status and credits
5. Switch to Custom mode if needed
6. Fill lyrics and style textareas
7. Wait for Create button to be enabled
8. Click Create and monitor generation
9. Extract top 2 most recent share links from results
10. Optionally trigger downloads

**Error Scenarios:**
- Login required → Prompt user to authenticate
- Insufficient credits → Show balance and suggest upgrade
- Network timeout → Retry or check connection
- Generation failure → Extract error message and suggest fixes

### Batch CSV Processing

**Trigger Phrases:**
- "process this CSV of songs"
- "batch generate from spreadsheet"
- "create playlist from CSV"

**CSV Format:**
```csv
Title,Suno Genre And Style Prompt,Suno Share Link,Notes
My Song,upbeat pop,,
Another Song,indie rock,,
```

**Process Flow:**
1. Validate CSV structure and required columns
2. Count songs needing generation
3. Estimate total time and credits required
4. Process each row sequentially:
   - Skip if share link exists
   - Generate song using single workflow
   - Update CSV with results
   - Log progress and errors
5. Generate completion summary

**Batch Optimization:**
- Process 5-10 songs per batch initially
- Add delays between generations (5-10 seconds)
- Handle interruptions gracefully
- Provide real-time progress updates

### Download Management

**Trigger Phrases:**
- "download my generated songs"
- "organize music files"
- "manage song downloads"

**File Organization:**
```
music/
├── suno-generated/
│   ├── 2025-01-15_14-30-25_upbeat-pop_Summer-Vibes.mp3
│   └── 2025-01-15_14-32-10_indie-rock_Midnight-Dreams.mp3
└── temp/
    └── downloads-in-progress/
```

**Process Flow:**
1. Scan existing downloads
2. Navigate to each share link
3. Locate and click download buttons
4. Monitor download progress
5. Organize files with descriptive names
6. Clean up temporary files
7. Generate organization report

## Error Handling & Recovery

### Authentication Issues
```javascript
// Detection
const content = await getWebContent();
if (content.url.includes('/login')) {
    throw new Error("Please log in to Suno first");
}

// Recovery
// - Prompt user to authenticate
// - Wait for manual login completion
// - Retry operation
```

### Credit Management
```javascript
// Detection
const credits = extractCredits(content);
if (credits < 10) {
    console.warn(`Low credits: ${credits} remaining`);
}

// Recovery
// - Show current balance
// - Suggest credit purchase
// - Reduce batch size
// - Pause processing
```

### Network Resilience
```javascript
// Retry logic with exponential backoff
async function retryOperation(operation, maxRetries = 3) {
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
            return await operation();
        } catch (error) {
            if (attempt === maxRetries) throw error;
            const delay = Math.pow(2, attempt) * 1000;
            await sleep(delay);
        }
    }
}
```

### Generation Monitoring
```javascript
// Polling for completion
async function waitForGeneration(timeout = 60000) {
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
        const content = await getWebContent();

        // Check for completion indicators
        if (content.includes('/song/')) {
            return true; // Success
        }

        // Check for error indicators
        if (content.includes('error') || content.includes('failed')) {
            return false; // Failure
        }

        await sleep(5000); // Check every 5 seconds
    }

    return false; // Timeout
}
```

## Performance Optimization

### Browser Session Management
- Reuse existing tabs when possible
- Minimize navigation between operations
- Cache element selectors when stable
- Clean up temporary tabs after use

### Timing Optimization
- Strategic delays between operations
- Parallel processing where safe
- Progress monitoring without excessive polling
- Timeout management for reliability

### Resource Efficiency
- Minimal browser interactions
- Efficient DOM queries
- Memory-conscious processing
- Automatic cleanup of resources

## Integration with PAI Ecosystem

### Skill Activation
The skill integrates with PAI's natural language routing:
```
User: "Generate a song about summer nights"
→ SKILL.md activated (matches "generate a song")
→ generate-song.md workflow selected
→ AI assistant executes chrome-mcp operations
→ Results returned with share links
```

### Multi-Agent Coordination
For complex requests, coordinate with other PAI agents:
- **Research Agent**: Gather inspiration for lyrics
- **Creative Agent**: Enhance style descriptions
- **Organization Agent**: Manage resulting music library

### Hook Integration
PAI hooks can automate post-generation tasks:
- Auto-download completed songs
- Update music library databases
- Generate playlists from batches
- Backup files to cloud storage

## Testing & Validation

### Unit Testing Workflows
```bash
# Test individual components
python3 scripts/csv_processor.py read-prompts test.csv
bash scripts/download_script.sh --test

# Validate chrome-mcp integration
# (Requires AI assistant to execute tool calls)
```

### Integration Testing
- End-to-end song generation
- Batch processing with real CSV
- Download and organization workflow
- Error scenario handling

### Performance Benchmarking
- Measure generation times
- Track success rates
- Monitor resource usage
- Optimize based on metrics

## Troubleshooting Guide

### Common Issues

**"Chrome MCP tools not available"**
- Ensure Chrome browser is running
- Verify chrome-mcp extension is installed
- Check PAI configuration for tool access

**"Login required"**
- Navigate to https://suno.com manually
- Complete authentication
- Retry the operation

**"Generation timeout"**
- Check internet connection
- Verify Suno service status
- Try during off-peak hours
- Reduce batch sizes

**"Download failed"**
- May be premium feature
- Check account tier
- Manual download as fallback

### Debug Information
Enable verbose logging to troubleshoot:
```bash
export DEBUG_SUNO=1
# Operations will show detailed chrome-mcp calls
```

### Recovery Procedures
1. **Restart Browser**: Clear cache, restart Chrome
2. **Check Account**: Verify Suno account status and credits
3. **Network Test**: Confirm internet connectivity
4. **Manual Verification**: Test Suno website directly
5. **Reduce Load**: Process fewer songs simultaneously

## Future Enhancements

### Planned Features
- **Voice Integration**: PAI voice notifications for completion
- **Playlist Generation**: Auto-create playlists from batches
- **Metadata Enhancement**: Add ID3 tags to downloads
- **Quality Selection**: Choose between generated variations
- **Style Learning**: Adapt to user preferences over time

### API Integration
- Monitor Suno API developments
- Implement direct API calls when available
- Maintain backward compatibility with browser automation

### Advanced Automation
- Machine learning for style optimization
- Automated lyric generation
- Multi-platform publishing
- Social media integration

This comprehensive implementation provides robust, scalable AI music generation with full PAI ecosystem integration.