# PAI Migration Plan: OpenCode Native Adapter

## Objective
Establish a robust, "Platform Agnostic" integration between **OpenCode** and the official **Personal AI Infrastructure (PAI)** repository (v0.9.1+).

## Architecture
*   **PAI Core (Data):** `~/Workspaces/pai-opencode` (Mirror of official v0.9.1 structure).
*   **Adapter (Logic):** `~/.config/opencode/plugin/pai-adapter.ts`.

## Migration Phases

### Phase 1: Standardization (The "Clean Slate")
Align `~/Workspaces/pai-opencode` strictly with the official v0.9.1 spec.
1.  **Backup:** Archive current workspace and config.
2.  **Scaffold:** Ensure `Skills/`, `Tools/`, `Memories/`, and `settings.json` exist.

### Phase 2: Deduplication & Consolidation (Resolving Conflicts)
Cleanly merge the illegal `~/.config/opencode/skills` directory into the PAI Workspace.
1.  **Compare:** Identify skills existing in both locations.
2.  **Deduplicate:** 
    *   If a skill is a PAI standard (e.g., `CORE`), keep the version from the workspace.
    *   If a skill is custom (e.g., `suno-song-creator`), move it to the workspace.
3.  **Lowercase Renaming:** Rename all skill directories to lowercase during the move to ensure OpenCode native compatibility.
4.  **Cleanup:** Remove the illegal `~/.config/opencode/skills` directory to allow OpenCode to boot.

### Phase 3: The Adapter (Plugin Development)
1.  **Config Loading:** Plugin reads `settings.json` for `PAI_DIR`.
2.  **Native Sync:** `setup-adapter.sh` symlinks `PAI_DIR/Skills/*` to `~/.opencode/skill/*`.
3.  **Event Bridge:** Maintain `session.idle` hooks for Voice/History.

### Phase 4: CI/CD & Verification
1.  **Setup:** Run `setup-adapter.sh`.
2.  **Verify:** Run `verify-pai.sh` to confirm:
    *   OpenCode boots without "invalid directory" errors.
    *   Skills are listed natively via `/skill`.
    *   Identity (CORE) is correctly loaded.

## Rollback Plan
Full restore from `~/pai_backup_*.tar.gz` if verification fails.
