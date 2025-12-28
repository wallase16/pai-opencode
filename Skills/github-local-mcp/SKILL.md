name: github-local-mcp
description: |
  Master GitHub via CLI (`gh`) - The efficient, token-saving alternative to GitHub MCP.
  Use this skill to manage repositories, issues, PRs, and gists directly from the terminal.
  Supports authentication, repo management, issue tracking, and PR workflows without external API costs.
  USE WHEN user says: "check github", "list issues", "create PR", "github status", "clone repo", "local github".

# GitHub Local MCP (gh CLI Wrapper)

## When to Activate This Skill
- "Check my GitHub issues"
- "Create a pull request for this branch"
- "List pull requests"
- "Clone this repository"
- "Who am I logged in as on GitHub?"
- "Sync with upstream"
- "View checks/CI status"

## Core Workflows

### 1. Authentication & Status
**Goal:** Verify connectivity and identity.
```bash
# Check login status
gh auth status

# Login (if needed - requires interactive browser or token)
# gh auth login
```

### 2. Repository Management
**Goal:** Clone, view, or create repos.
```bash
# View current repo info
gh repo view

# List your repos
gh repo list --limit 10

# Clone a repo
gh repo clone <owner>/<repo>

# Create a new repo from current dir
gh repo create --public --source=.
```

### 3. Issue Tracking
**Goal:** Manage tasks without leaving terminal.
```bash
# List issues assigned to you
gh issue list --assignee @me

# View specific issue
gh issue view <number>

# Create new issue (interactive or inline)
gh issue create --title "Bug: X is broken" --body "Details..."
```

### 4. Pull Request (PR) Workflow
**Goal:** Code review and merging.
```bash
# List open PRs
gh pr list

# Checkout a PR locally
gh pr checkout <number>

# Create PR from current branch
gh pr create --title "feat: New Feature" --body "Description..."

# View PR checks/CI status
gh pr checks

# Merge PR
gh pr merge <number> --squash --delete-branch
```

### 5. Gists (Code Snippets)
**Goal:** Share quick code snippets.
```bash
# List your gists
gh gist list

# Create public gist
gh gist create filename.js --public
```

## Best Practices
- **Token Economy:** This skill uses the `bash` tool with `gh`, avoiding LLM token costs for API schema processing.
- **Context:** Always check `git status` and `git remote -v` first to ensure context.
- **JSON Output:** For programmatic use, add `--json` flag (e.g., `gh issue list --json number,title,url`).

## Troubleshooting
- **"Not logged in":** Run `gh auth login` (requires user interaction or PAT).
- **"Not a git repository":** Ensure you are in the correct directory.
- **"Validation Failed":** Check your arguments and permissions.
