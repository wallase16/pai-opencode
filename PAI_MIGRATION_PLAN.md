# PAI Migration Plan: OpenCode Native Adapter

## Objective
Establish a robust, "Platform Agnostic" integration between **OpenCode** and the official **Personal AI Infrastructure (PAI)** repository (v0.9.1+).
The goal is to treat `pai-opencode` not as a fork of the content, but as the **OpenCode Adapter** that enables PAI on this platform.

## Architecture
*   **PAI Core (Data):** `~/Workspaces/pai-opencode` (Will mirror the official `danielmiessler/Personal_AI_Infrastructure` structure exactly).
*   **Adapter (Logic):** `~/.config/opencode/plugin/pai-adapter.ts` (Renamed from `pai-core.ts`).
    *   Reads `PAI_DIR` from `settings.json`.
    *   Bridges OpenCode events (`session.idle`) to PAI workflows.
    *   Injects PAI Skills into OpenCode's native skill system.

## Migration Steps

### Phase 1: Standardization (The "Clean Slate")
align `~/Workspaces/pai-opencode` strictly with the official v0.9.1 spec.
1.  **Backup:** Archive current workspace.
2.  **Restructure:**
    *   `Skills/` (Nested: `Skills/CORE/SKILL.md`)
    *   `Tools/`
    *   `Memories/`
    *   `.env`
    *   `settings.json` (Crucial: Contains `PAI_DIR`)
3.  **Validation:** Verify structure against official repo spec.

### Phase 2: The Adapter (Plugin Development)
Refactor `pai-core.ts` into `pai-adapter.ts`.
1.  **Config Loading:** implement logic to read `~/Workspaces/pai-opencode/settings.json` to find `PAI_DIR`.
2.  **Native Skills:** Instead of a custom tool, the adapter will programmatically `symlink` or `register` the `PAI_DIR/Skills` directory to `~/.opencode/skill` at runtime (or setup time).
3.  **Event Bridge:** Maintain the `session.idle` -> "COMPLETED" check -> Voice/History trigger.

### Phase 3: CI/CD & Testing (Local Workflow)
Ensure reliability before "shipping" the change to your active config.

*   **Setup Script (`setup-adapter.sh`):**
    *   Installs the PAI structure (if missing).
    *   Installs/Symlinks the `pai-adapter.ts` plugin.
    *   Generates `settings.json`.
    *   **CI Check:** verification step ensuring `opencode models` and `opencode run --help` don't crash.

*   **Verification Script (`verify-pai.sh`):**
    *   Checks for `PAI_DIR` in `settings.json`.
    *   Checks if the "CORE" skill is loadable via OpenCode native tools.
    *   Simulates a "COMPLETED" event to test hooks.

## Rollback Plan
*   **Snapshot:** Before applying Phase 1, create a full tarball of `~/.config/opencode` and `~/Workspaces/pai-opencode`.
*   **Restore Script:** A script to wipe the new setup and untar the snapshot if critical failures occur.

## Success Criteria
1.  User can clone official PAI repo.
2.  User runs `setup-adapter.sh`.
3.  `opencode run "help me"` triggers PAI identity.
4.  `opencode run "use skill core"` works natively.