# Final Specification: Bible Verse Song Pipeline (Mock/Offline Mode)

## Overview
Same architecture, but **Image Generation** is replaced with a **Mock Generator** that uses a placeholder image or simple text-overlay. This allows building and testing the FULL pipeline (Suno -> Video -> YouTube) without needing live API keys immediately.

## Updated Components

### C. Visual Generator (Mock / Placeholder)
- **Tool**: `visual_generator_mock.py`
- **Trigger**: Status = `Song Generated`.
- **Action**:
    - Takes `Thumbnail Concept` (e.g., "Vibrant comic style...").
    - **Instead of calling Gemini**:
        - Generates a static 1920x1080 background (solid color or gradient).
        - Overlays the `You Tube Title` text using `PIL` (Python Imaging Library).
        - Saves as `thumbnail_mock.jpg`.
- **Update**: Sets Status = `Image Generated`.

## Why This is Smart
1.  **Zero Cost Development**: We build the logic without burning credits or managing keys.
2.  **Verify Pipeline**: We prove FFmpeg assembly and YouTube upload work.
3.  **Easy Swap**: Later, we just replace `visual_generator_mock.py` with `visual_generator_gemini.py`. The rest of the system won't know the difference.

## Implementation Roadmap (Updated)
1.  **Refactor Suno Script** (Library mode).
2.  **Build Master Controller**.
3.  **Build Mock Visual Generator** (PIL text overlay).
4.  **Build FFmpeg Assembler**.
5.  **Build YouTube Uploader** (Browser Auto).
6.  **Build RSS Manager**.
