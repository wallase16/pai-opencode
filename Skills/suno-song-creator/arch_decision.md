# Architecture Decision: Skill vs. Project

## The Question
Should the "Bible Verse Song Pipeline" be wrapped as a **Skill** (reusable tool) or kept as a **Project** (standalone application)?

## Option A: As a Skill (`suno-song-creator`)
**Concept**: The pipeline remains part of the `suno-song-creator` skill directory.
**Pros**:
- **Integrated**: Keeps all Suno-related tools in one box.
- **Agent-Ready**: Easy for an agent to "use skill suno-song-creator" and execute the pipeline.
**Cons**:
- **Bloated**: A general "Song Creator" skill shouldn't necessarily know about "Bible Verses" or "YouTube Uploads". That's specific business logic.
- **Hard to Maintain**: Tying specific project logic (the CSV format, the YouTube schedule) into a generic skill makes the skill brittle.

## Option B: As a Standalone Project (Recommended)
**Concept**: Move the specific logic (`master_controller.py`, `bible_verse_plan.csv`) into a dedicated project folder (e.g., `~/Projects/BibleVerseSongs/`), importing the generic functionality from the `suno-song-creator` skill.
**Pros**:
- **Separation of Concerns**: The Skill handles "How to make a song". The Project handles "What songs to make and where to post them".
- **Clean**: Your specific schedule and metadata don't clutter the generic tool.
- **Scalable**: You can create *another* project (e.g., "Techno Tuesday Pipeline") using the same Suno skill without copying code.

## Recommendation
**Hybrid Approach**:
1.  **Keep the Generic Tools** (`suno_lib.py`, `video_assembler.py`) in the **Skill**.
2.  **Move the Business Logic** (`master_controller.py`, `bible_verse_plan.csv`) to a **Project Folder** (`/home/wallase16/Documents/BibleSongs/`).
3.  The Project imports the Skill's scripts as a library.

**Why?**
Because "Make a song" is a skill. "Run my daily Bible channel" is a business/project.

## Proposed Action
1.  Refactor: Ensure `suno_lib.py` and `video_assembler.py` stay in the Skill as generic tools.
2.  Migrate: Move `master_controller.py` and the CSV to a new Project directory.
3.  Update: Make `master_controller.py` import the tools from the Skill path.
