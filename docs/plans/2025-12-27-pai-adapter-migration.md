# PAI Adapter Migration - Task 1

## Task 1: Standardization & Cleanup

### 1.1 Create Directories
- Ensure `opencode/scripts` exists.
- Ensure `opencode/plugin` exists.
- Ensure `docs/plans` exists.

### 1.2 Move Scripts
Move the following root-level scripts to `opencode/scripts/`:
- `check-pai-type.sh`
- `pai-status.sh`
- `test-pai-bash.sh`

### 1.3 Cleanup
- Remove the moved scripts from the root directory.

### 1.4 Create Documentation
- Create `opencode/README.md` explaining the directory structure:
    - `plugin/`: Contains the PAI adapter source code.
    - `scripts/`: Helper scripts for setup, verification, and maintenance.
    - `voices/`: Voice configuration and models.

## Success Criteria
- Root directory is clean of shell scripts.
- All scripts function correctly from their new location (may need path updates).
