---
name: commit
description: >-
  Analyze the current project and Git repository state, safely inspect and stage project changes
  (strictly excluding secrets and sensitive files), generate an intelligent Conventional Commit message
  based on the actual diff, and create the commit. Never pushes to remote. Use when the user invokes
  /commit or asks to "commit", "commit my changes", or "make a commit".
---

# Commit Workflow

This intelligent workflow analyzes the current project and Git state, screens changes for secrets, stages valid modifications, generates a contextual Conventional Commit message, and creates the commit locally.

> [!IMPORTANT]
> **Strict Guardrail**: This workflow creates local commits only. It must **NEVER** execute `git push` or publish anything to a remote repository.

---

## Workflow Execution Steps

Follow these sequential phases. Do not skip any phase.

### Phase 1: Project & Git Detection

1. **Locate Workspace & Root**:
   Determine the current workspace root and check if Git is initialized:
   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Handle Projects Without Git**:
   If the command fails (not a Git repository):
   - **Do NOT run `git init` automatically.**
   - Prompt the user with options:
     - **Option A**: Initialize a new local Git repository.
     - **Option B**: Connect this project to an existing remote repository.
   - If the user chooses **Option A**: Run `git init -b main` (or `git init`).
   - If the user chooses **Option B**: Ask for the repository URL, then run `git init`, `git remote add origin <URL>`, and verify with `git remote -v`.
   - Never invent repository URLs or assume GitHub usernames.

3. **Check Repository State**:
   If Git is initialized, inspect:
   - Current branch: `git branch --show-current`
   - Detached HEAD check: If empty, run `git rev-parse --short HEAD`. Warn the user if HEAD is detached.
   - Remotes: `git remote -v`. (Note: for local commits, a remote is optional; do not require one).
   - Commit history: `git log -n 5 --oneline` (inspect style, scope patterns, ticket IDs).
   - In-progress operations: Check if `.git/MERGE_HEAD`, `.git/rebase-merge`, or `.git/CHERRY_PICK_HEAD` exist. If so, **HALT** and notify the user to resolve the active conflict/rebase first.

> [!TIP]
> You can run the bundled inspector for an instant summary:
> ```bash
> python3 ~/.gemini/config/plugins/git-workflows/scripts/git_inspector.py --json
> ```

---

### Phase 2: Sensitive Data Screening & Change Inspection

1. **Inspect Working Tree**:
   Run `git status --porcelain=v2 -uall` to inspect all staged, unstaged, and untracked files.

2. **Empty Working Tree Check**:
   If there are no changes whatsoever (staged, unstaged, or untracked):
   - Inform the user: `Working tree is clean. No changes to commit.`
   - **Stop execution.** Do NOT create an empty commit.

3. **Screen Sensitive Files**:
   Before staging, check all candidate files against sensitive patterns:
   - Environment files: `.env`, `.env.*`, `*.env`, `.env.local`
   - Private keys & certs: `*.pem`, `*.key`, `*.pkcs12`, `*.pfx`, `*.p12`, `*.keystore`, `*.jks`
   - SSH keys: `id_rsa*`, `id_ed25519*`, `id_ecdsa*`, `id_dsa*`
   - Credentials & tokens: `credentials.json`, `service-account*.json`, `client_secret*.json`, `token.json`, `auth.json`, `oauth*.json`
   - Local configurations with secrets: `local.properties`, `.npmrc` with auth tokens

4. **Action on Sensitive Files**:
   - **EXCLUDE** all detected sensitive files from staging.
   - Warn the user explicitly:
     > ⚠️ **Excluded Sensitive File(s)**: The following files were detected and will NOT be committed:
     > - `<file>`
     > Recommendation: Add them to `.gitignore`.
   - If a sensitive file was already staged by the user prior to this command, unstage it immediately:
     ```bash
     git restore --staged <file>
     ```

---

### Phase 3: Intelligent Staging

1. **Selective Staging**:
   - Do NOT run `git add .` blindly.
   - Stage the identified safe modified, deleted, and untracked files:
     ```bash
     git add <safe-file-1> <safe-file-2> ...
     ```
   - Respect `.gitignore` rules.

2. **Staged Diff Verification**:
   Inspect the staged changes to verify only intended files are staged:
   ```bash
   git diff --staged --stat
   ```
   If nothing is staged after excluding sensitive files:
   - Inform the user that no safe, commit-eligible changes remain.
   - Stop execution.

---

### Phase 4: Conventional Commit Message Generation

Analyze the staged changes using `git diff --staged` to generate a descriptive Conventional Commit message:

1. **Structure**:
   `<type>(<scope>): <summary>`

2. **Commit Types**:
   - `feat`: Net-new functionality or capabilities.
   - `fix`: Bug fix, error resolution, crash fix.
   - `refactor`: Code restructuring without modifying behavior.
   - `perf`: Performance improvement or optimization.
   - `docs`: Documentation, README, markdown updates.
   - `style`: Whitespace, formatting, missing semi-colons.
   - `test`: Adding or updating test cases.
   - `build`: Dependency changes, build system configs.
   - `ci`: CI/CD pipelines, GitHub Actions workflows.
   - `chore`: Tooling, configs, or maintenance tasks.

3. **Rules**:
   - Use imperative mood: "add" not "added", "fix" not "fixes".
   - Keep subject ≤ 50 chars (max 72). No trailing period.
   - Include an optional body only if the "why" or context is non-obvious.
   - Match existing repository conventions if observed from `git log -n 5`.
   - Never hallucinate changes or generate generic placeholders like "update files".

---

### Phase 5: Commit Execution & Verification

1. **Execute Commit**:
   Run the commit command with the generated message:
   ```bash
   git commit -m "<type>(<scope>): <summary>"
   ```

2. **Hook Failure Handling**:
   - Never use `--no-verify`.
   - If pre-commit hooks fail, capture the hook error output, present it to the user, and halt. Do NOT bypass the hooks.

3. **Verify Commit**:
   Confirm that the commit was successfully written:
   ```bash
   git log -1 --stat
   ```

4. **Present Output Report**:
   Present the final result to the user using the following format:

```markdown
### ✅ Commit Completed

- **Commit Hash**: `<short-hash>` (`<full-hash>`)
- **Commit Message**: `<type>(<scope>): <summary>`
- **Current Branch**: `<branch-name>`
- **Files Committed**:
  - `<file-path-1>` (+X, -Y)
  - `<file-path-2>` (+A, -B)

> ℹ️ *Note: This workflow is local-only. Changes were committed locally and were NOT pushed to any remote.*
```

---

## Shared References & Details

For extended safety guidelines, secret patterns, and edge case resolutions, see:
- [references/git-core-engine.md](../../references/git-core-engine.md)
