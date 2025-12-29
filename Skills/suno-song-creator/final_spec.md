# Final Specification: Bible Verse Song Pipeline

## Architecture Overview
A central `master_controller.py` script orchestrates the flow based on `bible_verse_plan.csv`. It runs daily (or on demand), checks the status of each row, and moves items through the pipeline.

## 1. Data Source (CSV)
- **Path**: `youtube-bible-verse-plan11092025.csv`
- **Columns**: `Date`, `Verse`, `Prompt`, `Thumbnail Concept`, `Status`, `MP3 Path`, `Image Path`, `Video Path`, `YouTube ID`.

## 2. Components

### A. Song Generator (Suno)
- **Tool**: `suno_chrome_creator.py` (Existing, to be integrated).
- **Trigger**: Status = `Planned`.
- **Action**: Generates song, downloads MP3.
- **Update**: Sets Status = `Song Generated`, saves `MP3 Path`.

### B. Manual Hand-off (DistroKid)
- **Trigger**: Status = `Song Generated` (Batch Check).
- **Action**: Script pauses or notifies user: "7 new songs ready for DistroKid upload."
- **User Action**: User uploads to DistroKid manually.
- **Update**: User/Script marks Status = `Registered`. (Can be optional/parallel).

### C. Visual Generator (DALL-E 3)
- **Tool**: `openai` Python client.
- **Trigger**: Status = `Song Generated` (or `Registered`).
- **Action**: Sends `Thumbnail Concept` to DALL-E 3. Downloads Image.
- **Update**: Sets Status = `Image Generated`, saves `Image Path`.

### D. Video Assembler (FFmpeg)
- **Tool**: `ffmpeg` (subprocess call).
- **Trigger**: Status = `Image Generated`.
- **Action**: Combines MP3 + Image -> MP4 (1080p, AAC audio).
- **Update**: Sets Status = `Video Ready`, saves `Video Path`.

### E. YouTube Uploader (Browser Auto)
- **Tool**: `youtube_uploader.py` (New - Selenium/Playwright).
- **Trigger**: Status = `Video Ready`.
- **Action**: Log in, Upload Video, Set Title/Desc/Tags, Set Schedule.
- **Update**: Sets Status = `Scheduled`.

### F. Podcast Publisher (RSS/GitHub)
- **Tool**: `rss_manager.py` (New).
- **Trigger**: Status = `Video Ready`.
- **Action**:
    1. Copy MP3 to local git repo (`docs/audio/`).
    2. Generate new `<item>` in `feed.xml`.
    3. Git Commit & Push to GitHub Pages.
- **Update**: Sets Status = `Podcast Published`.

## Implementation Roadmap
1.  **Phase 1**: Update `suno_chrome_creator.py` to be callable as a library.
2.  **Phase 2**: Build `master_controller.py` skeleton and CSV handling.
3.  **Phase 3**: Implement DALL-E 3 integration.
4.  **Phase 4**: Implement FFmpeg assembly.
5.  **Phase 5**: Implement RSS/GitHub Pages logic.
6.  **Phase 6**: Implement YouTube Uploader.

## Configuration
- `config.json`: Stores API keys (OpenAI), paths, and credentials.
