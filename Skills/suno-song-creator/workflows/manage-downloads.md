---
name: manage-downloads
description: Organize, download, and manage AI-generated song files from Suno with proper file naming and cleanup
---

# Download Management Workflow

## When to Activate
- Organizing downloaded song files
- Managing file storage and cleanup
- "manage downloads", "organize songs", "cleanup files"
- Post-generation file handling
- Setting up music library structure

## Prerequisites
- Song share links available
- Chrome browser running
- Download directory accessible
- Sufficient disk space

## Workflow Steps

### Step 1: Directory Assessment
**AI Action:** Analyze current download state
```
Check: Existing download directories
Scan: Current song files
Assess: File organization needs
Plan: Cleanup and reorganization
```

### Step 2: Download Execution
**AI Action:** Download songs from share links
```
For each share link:
   Navigate to song page
   Locate download button
   Trigger download
   Monitor progress
   Verify completion
```

### Step 3: File Organization
**AI Action:** Structure downloaded files
```
Create: Organized directory structure
Rename: Files with descriptive names
Move: Files to appropriate folders
Update: Metadata and tags
```

### Step 4: Quality Verification
**AI Action:** Check download integrity
```
Verify: File sizes and formats
Test: Audio playback capability
Check: Metadata completeness
Flag: Corrupted or incomplete files
```

### Step 5: Cleanup Operations
**AI Action:** Remove temporary files and duplicates
```
Remove: Temporary download artifacts
Delete: Duplicate files
Clean: Cache and temporary directories
Archive: Old or unused files
```

## Directory Structure

### Recommended Organization
```
music/
├── suno-generated/
│   ├── YYYY-MM-DD_HH-MM-SS_[style]_[title].mp3
│   ├── YYYY-MM-DD_HH-MM-SS_[style]_[title].mp3
│   └── playlists/
│       └── my-favorite-songs.m3u
├── archives/
│   └── YYYY-MM/
│       └── old-songs/
└── temp/
    └── downloads-in-progress/
```

### File Naming Convention
```
Format: YYYY-MM-DD_HH-MM-SS_[STYLE]_[TITLE].mp3
Example: 2025-01-15_14-30-25_upbeat-pop_Summer-Vibes.mp3
```

## Download Process

### Individual Song Downloads
1. **Navigate:** Go to song share URL
2. **Locate:** Find download button (may be premium feature)
3. **Click:** Trigger download
4. **Monitor:** Wait for completion
5. **Verify:** Check file integrity

### Batch Downloads
1. **Queue:** Collect all share links
2. **Sequence:** Download one at a time
3. **Progress:** Show completion status
4. **Errors:** Handle failed downloads gracefully

## Error Handling

### Download Failures
- **Detection:** Missing download button or premium requirement
- **Action:** Note limitation, suggest manual download
- **Recovery:** Continue with other songs

### File System Issues
- **Detection:** Permission errors, disk space issues
- **Action:** Check and report system status
- **Recovery:** Suggest alternative locations or cleanup

### Network Problems
- **Detection:** Connection timeouts during download
- **Action:** Retry with exponential backoff
- **Recovery:** Resume interrupted downloads

## Quality Assurance

### File Validation
- **Format Check:** Verify MP3/WAV format
- **Size Verification:** Ensure reasonable file sizes
- **Playback Test:** Confirm audio is playable
- **Metadata Check:** Validate title and artist info

### Duplicate Handling
- **Detection:** Identify duplicate songs
- **Comparison:** Check content hashes
- **Action:** Keep best quality version
- **Cleanup:** Remove duplicate files

## Integration Points
- **Scripts:** `scripts/download_script.sh` (download automation)
- **Assets:** File organization templates
- **Related:** `workflows/generate-song.md` (link generation)
- **Related:** `workflows/batch-process.md` (bulk operations)

## Output Format

### Download Progress
```
📥 Downloading: Summer Vibes (upbeat pop)
📊 Progress: 2/5 songs completed
⏱️ Time remaining: ~3 minutes
📁 Saving to: music/suno-generated/
```

### Completion Summary
```
✅ Download Management Complete!
📊 Results: 8/10 songs downloaded successfully
📁 Organized: 8 files in music/suno-generated/
🗑️ Cleaned up: 2 duplicate files removed
💾 Space saved: 45MB
```

## Best Practices

### Storage Management
- Regular cleanup of temporary files
- Archive old songs periodically
- Monitor disk space usage
- Backup important music collections

### Organization Tips
- Use consistent naming conventions
- Create playlists for different moods/styles
- Tag files with metadata
- Maintain a music library database

### Performance Optimization
- Download during off-peak hours
- Use stable network connections
- Monitor system resources
- Batch operations for efficiency