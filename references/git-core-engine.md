# Intelligent Git Core Engine Reference

This reference document defines the shared architecture, security boundaries, and operational rules for Antigravity Git workflows (`commit` and `commit-push`).

---

## 1. Project & Git Detection Engine

Before making any changes or executing Git modifications, the agent must inspect and understand the repository state:

### Step 1.1: Environment & Project Root Discovery
1. Identify the current working directory (`CWD`) and active workspace root.
2. Run `git rev-parse --is-inside-work-tree`:
   - If exit code != 0 or output != `true`: The directory is **not** an initialized Git repository. Route immediately to **Section 2 (Handling Projects Without Git)**.
3. If inside a work tree, obtain:
   - **Repository Root**: `git rev-parse --show-toplevel`
   - **Git Directory**: `git rev-parse --git-dir`
   - **Current Branch**: `git branch --show-current`
   - **Detached HEAD**: If `git branch --show-current` returns empty, verify with `git rev-parse --short HEAD`. Warn the user if in a detached HEAD state.
   - **Existing Remotes**: `git remote -v`
   - **Recent Commits**: `git log -n 5 --oneline` (to learn repository-specific naming, commit conventions, ticket prefixes, or scopes).

### Step 1.2: In-Progress Operations Check
Check whether the repository is in the middle of a complex Git operation. If any of the following exist in `.git/`:
- `MERGE_HEAD`: A merge conflict is pending resolution. **HALT**. Do NOT commit automatically. Inform the user of unresolved conflicts.
- `rebase-merge` or `rebase-apply`: A rebase is in progress. **HALT**. Inform the user to complete or abort the rebase.
- `CHERRY_PICK_HEAD`: A cherry-pick is in progress. **HALT**.
- `REVERT_HEAD`: A revert is in progress. **HALT**.
- `BISECT_LOG`: A git bisect session is active. Warn the user before proceeding.

---

## 2. Handling Projects Without Git

If the current project root is not an initialized Git repository:

1. **Do NOT run `git init` automatically.**
2. Use `ask_question` (or clear interactive prompt) asking the user:
   - **Option 1**: Initialize a new local Git repository (`git init`).
   - **Option 2**: Connect this project to an existing remote repository.
3. If the user selects **Option 2 (Connect to existing remote)**:
   - Ask the user for the repository URL (HTTPS or SSH).
   - Never invent or guess URLs or GitHub usernames.
   - Once provided:
     1. Run `git init`.
     2. Run `git remote add origin <provided-url>`.
     3. Verify remote with `git remote -v`.
4. If the user selects **Option 1 (New local repository)**:
   - Initialize with `git init -b main` (or standard `git init`).
   - Proceed with safe staging and initial commit.

---

## 3. Handling Missing Remotes

If Git is initialized but `git remote -v` produces no output:

1. For **Commit** (`commit`):
   - A remote is **not mandatory** for local commits.
   - Proceed normally to create the local commit.
   - In the final summary, note: `Configured Remotes: None (Local repository)`.
2. For **Commit & Push** (`commit-push`):
   - A remote is **mandatory** because pushing requires a target repository.
   - Prompt the user:
     - Ask if they want to configure a remote repository.
     - Request the remote URL (HTTPS or SSH).
     - Run `git remote add origin <url>`.
     - Verify with `git remote -v`.
   - If the user declines to add a remote, explain that changes are committed locally but cannot be pushed, and halt.

---

## 4. Intelligent Staging & Sensitive Data Firewall

**Strict Rule:** Never run `git add .` or `git add -A` blindly.

### Step 4.1: Inspect Full Working Tree State
Run `git status --porcelain=v2 -uall` (or the helper script `git_inspector.py`) to obtain:
- Staged changes (`XY` index modified/added)
- Unstaged modified/deleted files
- Untracked files

### Step 4.2: Sensitive File Screening (Firewall)
Before staging, cross-reference all untracked and modified candidate files against sensitive patterns:

| Category | Patterns & Extensions | Action |
| :--- | :--- | :--- |
| **Environment Files** | `.env`, `.env.*`, `*.env`, `.env.local`, `.env.production` | **EXCLUDE** |
| **Private Keys & Certs** | `*.pem`, `*.key`, `*.pkcs12`, `*.pfx`, `*.p12`, `*.keystore`, `*.jks` | **EXCLUDE** |
| **SSH Keys** | `id_rsa`, `id_rsa.pub`, `id_ed25519`, `id_ecdsa`, `id_dsa` | **EXCLUDE** |
| **API Keys & Credentials** | `credentials.json`, `service-account*.json`, `client_secret*.json`, `secrets.*` | **EXCLUDE** |
| **Tokens & Auth** | `*.token`, `token.json`, `auth.json`, `oauth*.json` | **EXCLUDE** |
| **Local Configs with Secrets** | `local.properties`, `.npmrc` (with auth tokens), `.pypirc` | **EXCLUDE** |

### Step 4.3: Exclusion & Staging Execution
1. If sensitive files are detected:
   - **Exclude them immediately from staging.**
   - Output an explicit warning:
     > ⚠️ **Security Alert**: The following sensitive file(s) were detected and excluded from staging:
     > - `<filename>`
     > Recommendation: Add these files to `.gitignore` to prevent accidental exposure.
2. Respect existing `.gitignore` and do not override exclusions.
3. Stage only safe files explicitly by path or pattern (e.g. `git add path/to/file1 path/to/file2`).
4. If files were already staged by the user prior to triggering the workflow:
   - Check if any already-staged file is sensitive.
   - If sensitive, unstage it with `git restore --staged <file>` and alert the user.
   - Keep user-staged safe changes intact.

### Step 4.4: Staged Diff Verification
Inspect `git diff --staged --stat` and `git diff --staged`:
- Verify that meaningful code or document changes are actually staged.
- Ensure no unintended files or empty commits are produced.

---

## 5. Intelligent Commit Message Generation

The commit message must accurately reflect the staged semantic changes using the Conventional Commits specification.

### 5.1 Format
```text
<type>(<scope>): <concise imperative summary>

[optional body explaining why and context]
```

### 5.2 Conventional Types
- `feat`: New feature or user-facing functionality.
- `fix`: Bug fix or error resolution.
- `refactor`: Code restructuring without changing external behavior.
- `perf`: Performance enhancement or optimization.
- `docs`: Documentation updates (README, docstrings, markdown).
- `style`: Formatting, whitespace, semicolon changes (no code logic change).
- `test`: Adding, updating, or fixing tests.
- `build`: Build system, dependencies, packaging (`pubspec.yaml`, `package.json`, `Cargo.toml`).
- `ci`: CI/CD configuration files and pipelines (`.github/workflows`, Dockerfile).
- `chore`: Maintenance tasks, meta updates, tooling configurations.

### 5.3 Rules for Generating Commit Messages
1. **Imperative Mood**: Use "add", "fix", "update", "refactor" (not "added", "fixes", "updating").
2. **Concise Subject**: Target ≤ 50 characters, hard ceiling at 72 characters. No trailing period.
3. **Meaningful Scope**: Derive scope from modified module or component (e.g. `feat(auth)`, `fix(router)`, `docs(api)`).
4. **Learn from History**: Inspect recent commits from `git log -n 5` to align with the repository's capitalization, prefix conventions, or ticket IDs (e.g. `[JIRA-123]`).
5. **No Hallucinations**: Base the message strictly on the diff, not on assumptions.

---

## 6. Pre-Push Safety & Upstream Verification (Workflow 2 Only)

Pushing must only occur after explicit safety verification:

### 6.1 Upstream Verification
1. Run `git rev-parse --abbrev-ref --symbolic-full-name @{u}`:
   - **Upstream configured**: Inspect tracking branch (e.g., `origin/main`).
   - **No upstream configured**:
     - Identify destination branch (default to matching current local branch name).
     - Target remote: default to `origin` (or ask if multiple remotes exist).
     - Prepare push command with `-u` / `--set-upstream origin <branch>`.

### 6.2 Pre-Push Remote Inspection (Conflict Prevention)
1. Safely fetch remote updates:
   ```bash
   git fetch <remote> <branch>
   ```
2. Check if the remote branch contains commits that the local branch does not have:
   ```bash
   git rev-list --count HEAD..<remote>/<branch>
   ```
3. If remote is ahead (`behind > 0`):
   - **HALT PUSH IMMEDIATELY.**
   - Output warning:
     > 🛑 **Push Paused**: Remote branch `<remote>/<branch>` contains commits that are not present locally.
     > A push would result in a non-fast-forward rejection or conflict.
     > Action required: Pull or rebase remote changes first (`git pull --rebase origin <branch>`).
   - **Never force push** (`--force`, `-f`, `--force-with-lease`).

### 6.3 Authentication & Push Execution
1. Execute safe push:
   - `git push` (if upstream tracked)
   - `git push -u <remote> <branch>` (if setting upstream)
2. Handle stderr failures:
   - **Auth Error (401/403/Permission denied)**: Explain the authentication issue clearly to the user (SSH key permissions, GitHub PAT, or `gh auth login`).
   - **Protected Branch**: Explain branch protection rules (e.g., direct pushes forbidden, pull request required).
   - **Pre-push Hook Failure**: Show the hook's stderr. Never bypass with `--no-verify`.

---

## 7. Absolute Safety Rules (Both Workflows)

1. **NO Destructive Commands**: Never run `git reset --hard`, `git clean -fd`, `git checkout .`, or `git restore .` unless explicitly requested by the user.
2. **NO Force Pushing**: Never push with `--force` or `--force-with-lease`.
3. **NO Verification Bypassing**: Never pass `--no-verify` to bypass pre-commit or pre-push hooks.
4. **NO Silent Discarding**: Never unstage or delete user modifications without explicit notice.
5. **NO Empty Commits**: Never create a commit if no changes exist (`git commit --allow-empty` is forbidden).
6. **Verification Mandatory**: Always verify that git operations succeeded by checking return codes, `git log -1`, or `git status`.
