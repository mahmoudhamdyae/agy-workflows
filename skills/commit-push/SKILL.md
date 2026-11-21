---
name: commit-push
description: >-
  Analyze the current project and Git repository state, safely screen and stage changes (strictly excluding
  secrets and sensitive files), create an intelligent Conventional Commit, perform pre-push safety checks,
  verify upstream tracking, and safely push to the remote repository. Never force-pushes. Use when the user
  invokes /commit-push or asks to "commit and push", "commit-push", or "commit and sync".
---

# Commit & Push Workflow

This intelligent workflow performs the complete commit preparation process (repository inspection, sensitive file exclusion, intelligent staging, and Conventional Commit creation), followed by pre-push remote verification and safe publishing to the upstream remote repository.

> [!IMPORTANT]
> **Strict Guardrails**:
> - **NEVER force push** (`--force`, `-f`, `--force-with-lease`).
> - **NEVER bypass hooks** (`--no-verify` is prohibited).
> - If remote has unmerged changes or push is rejected, **STOP** and explain. Never attempt automatic destructive recovery.

---

## Workflow Execution Steps

Follow these sequential phases. Do not skip any phase.

### Phase 1: Project & Git Detection

1. **Locate Workspace & Root**:
   Check if current directory is inside a Git repository:
   ```bash
   git rev-parse --is-inside-work-tree
   ```

2. **Handle Projects Without Git**:
   If not a Git repository:
   - **Do NOT run `git init` automatically.**
   - Prompt the user:
     - **Option A**: Initialize a new local Git repository.
     - **Option B**: Connect this project to an existing remote repository.
   - If user selects **Option A**: Run `git init -b main`.
   - If user selects **Option B**: Request remote repository URL, run `git init`, `git remote add origin <URL>`, and verify with `git remote -v`.
   - Never invent repository URLs or guess usernames.

3. **Check Repository State**:
   Inspect current Git environment:
   - Current branch: `git branch --show-current`
   - Detached HEAD check: If empty, run `git rev-parse --short HEAD`. Warn user if HEAD is detached.
   - Remotes: `git remote -v`
   - Commit history: `git log -n 5 --oneline` (to match project commit conventions)
   - In-progress operations: Check `.git/MERGE_HEAD`, `.git/rebase-merge`, or `.git/CHERRY_PICK_HEAD`. If any exist, **HALT** and instruct user to resolve active conflict/rebase first.

> [!TIP]
> You can run the bundled inspector for an instant summary:
> ```bash
> python3 ~/.gemini/config/plugins/git-workflows/scripts/git_inspector.py --json
> ```

---

### Phase 2: Sensitive Data Screening & Change Inspection

1. **Inspect Changes**:
   Run `git status --porcelain=v2 -uall` to inspect staged, unstaged, and untracked files.

2. **Empty Working Tree Check**:
   If working tree is clean with no changes:
   - Inform the user: `Working tree is clean. No changes to commit or push.`
   - **Stop execution.**

3. **Screen Sensitive Files**:
   Filter all candidate files against sensitive patterns:
   - Environment files: `.env`, `.env.*`, `*.env`, `.env.local`
   - Private keys & certs: `*.pem`, `*.key`, `*.pkcs12`, `*.pfx`, `*.p12`, `*.keystore`, `*.jks`
   - SSH keys: `id_rsa*`, `id_ed25519*`, `id_ecdsa*`, `id_dsa*`
   - Credentials & tokens: `credentials.json`, `service-account*.json`, `client_secret*.json`, `token.json`, `auth.json`, `oauth*.json`
   - Local configurations with secrets: `local.properties`, `.npmrc` with auth tokens

4. **Action on Sensitive Files**:
   - **EXCLUDE** all detected sensitive files from staging.
   - Explicitly warn the user of excluded files and suggest adding them to `.gitignore`.
   - If any sensitive file was already staged, unstage it with `git restore --staged <file>`.

---

### Phase 3: Intelligent Staging

1. **Selective Staging**:
   - Do NOT run `git add .` blindly.
   - Stage verified safe modified, deleted, and untracked project files:
     ```bash
     git add <safe-file-1> <safe-file-2> ...
     ```

2. **Staged Diff Verification**:
   Inspect staged diff: `git diff --staged --stat`.
   If no changes remain staged after screening, inform user and halt.

---

### Phase 4: Conventional Commit Message Generation

Analyze `git diff --staged` and generate a Conventional Commit message:

1. **Format**: `<type>(<scope>): <summary>`
2. **Types**: `feat`, `fix`, `refactor`, `perf`, `docs`, `style`, `test`, `build`, `ci`, `chore`.
3. **Rules**:
   - Imperative mood ("add", "fix", "update").
   - ≤ 50 chars subject line (hard ceiling 72).
   - Match existing repository patterns if seen in `git log -n 5`.

---

### Phase 5: Commit Execution & Verification

1. **Execute Commit**:
   ```bash
   git commit -m "<type>(<scope>): <summary>"
   ```
2. **Verify Commit**:
   ```bash
   git log -1 --stat
   ```
   If pre-commit hooks fail, show error and halt. Do NOT bypass hooks with `--no-verify`.

---

### Phase 6: Remote & Upstream Safety Verification

Before pushing, ensure remote connectivity and prevent conflicts:

1. **Check Configured Remotes**:
   Run `git remote -v`.
   - If **NO remote is configured**:
     - Prompt the user:
       > No remote repository is configured for this project.
       > Would you like to connect a remote repository now?
     - Request the repository URL.
     - Add remote: `git remote add origin <URL>`.
     - Verify: `git remote -v`.
     - If the user declines, report that changes were committed locally and stop without pushing.
   - If multiple remotes exist (e.g. `origin` and `upstream`) and upstream tracking is unset: ask the user which remote to target.

2. **Check Upstream Tracking**:
   Run `git rev-parse --abbrev-ref --symbolic-full-name @{u}`:
   - **Has Upstream**: Target remote and branch are defined (e.g. `origin/main`).
   - **No Upstream**:
     - Destination branch: Defaults to current local branch name (e.g., `main`).
     - Target remote: Defaults to `origin`.
     - If destination is ambiguous or HEAD is detached, ask the user. Never guess.
     - Push will use `--set-upstream origin <branch>`.

3. **Pre-Push Remote Inspection (Conflict Prevention)**:
   Safely fetch the remote target:
   ```bash
   git fetch <remote> <branch>
   ```
   - If fetch fails with authentication error (e.g., HTTP 401/403, Permission denied):
     - Explain the authentication issue clearly to the user (check SSH keys, GitHub token, or run `gh auth login`).
     - Stop execution.
   - Check if the remote branch contains commits not present locally:
     ```bash
     git rev-list --count HEAD..<remote>/<branch>
     ```
   - **If remote is ahead (`count > 0`)**:
     - **HALT PUSH IMMEDIATELY.**
     - Inform user:
       > 🛑 **Push Paused**: Remote branch `<remote>/<branch>` has new changes not present locally.
       > Pushing now would cause a non-fast-forward rejection or overwrite work.
       > Action required: Pull or rebase remote changes first (`git pull --rebase <remote> <branch>`).
     - **NEVER attempt force push.**

---

### Phase 7: Push Execution & Verification

1. **Execute Push**:
   - If upstream is configured:
     ```bash
     git push
     ```
   - If setting upstream:
     ```bash
     git push -u <remote> <branch>
     ```

2. **Handle Push Result**:
   - If rejected (protected branch rules, permissions, hook failure):
     - Output the exact error message from Git.
     - Stop execution. Do not attempt risky automatic workarounds.
   - If successful:
     - Verify local and remote synchronization:
       ```bash
       git status -b --porcelain=v2
       ```

3. **Present Final Report**:
   Present the final result to the user using the following format:

```markdown
### 🚀 Commit & Push Completed

- **Commit Hash**: `<short-hash>` (`<full-hash>`)
- **Commit Message**: `<type>(<scope>): <summary>`
- **Current Branch**: `<branch-name>`
- **Remote Repository**: `<remote-name>` (`<remote-url>`)
- **Destination Branch**: `<remote-name>/<branch-name>`
- **Push Result**: ✅ Successfully pushed and synchronized with upstream.
- **Files Included**:
  - `<file-path-1>` (+X, -Y)
  - `<file-path-2>` (+A, -B)
```

---

## Shared References & Details

For extended safety guidelines, secret patterns, and edge case resolutions, see:
- [references/git-core-engine.md](../../references/git-core-engine.md)
