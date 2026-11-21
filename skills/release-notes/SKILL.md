---
name: release-notes
description: >-
  Generate comprehensive, grounded release notes from actual Git commit history, PR merges, and code diffs.
  Categorizes changes into New Features, Bug Fixes, Improvements, Breaking Changes, and Technical/DevOps tasks.
  Produces both a user-facing Changelog and a technical engineering release summary. Never invents features.
  Use when user invokes /release-notes or asks to "generate release notes", "write changelog", or "prepare release summary".
---

# Release Notes Workflow

This workflow automatically inspects the Git revision history, commit messages, and code changes since the previous release or tag to author clear, categorized, and 100% verified release notes.

> [!IMPORTANT]
> **Zero Hallucination Policy**: Every single bullet point in the release notes must be verified against actual Git commits or code diffs. Never invent features, bug fixes, or enhancements that are not explicitly evidenced in the git log or merged pull requests.

---

## 4-Step Release Notes Process

### Step 1: Discover Git Revision Boundaries
1. Identify the previous release tag or base commit:
   ```bash
   git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD
   ```
2. Determine current HEAD commit and current version:
   - Check `pubspec.yaml`, `package.json`, or release branch name.
3. Fetch the commit list between base tag and HEAD:
   ```bash
   git log <previous-tag>..HEAD --oneline --no-merges
   ```
   *(If no tags exist, inspect recent commits e.g. `git log -n 25 --oneline`).*

---

### Step 2: Code Diff & PR Semantic Analysis
1. Inspect the changed files across the revision range:
   ```bash
   git diff <previous-tag>..HEAD --stat
   ```
2. Group commits and diffs into 5 standardized categories:
   - 🚀 **New Features (`feat`)**: User-visible capabilities and enhancements.
   - 🐛 **Bug Fixes (`fix`)**: Resolutions to crashes, logic bugs, UI glitches, or broken workflows.
   - ⚡ **Performance & UX Improvements (`perf`, `refactor`)**: Speedups, smoother animations, reduced payload sizes.
   - ⚠️ **Breaking Changes (`BREAKING CHANGE`)**: Deprecated APIs, altered endpoint signatures, database schema migrations.
   - 🛠️ **Technical & Infrastructure (`build`, `ci`, `chore`, `test`)**: Dependency upgrades, CI/CD changes, refactorings.

---

### Step 3: Dual Audience Authoring
The agent generates two tailored formats:
1. **User-Facing Changelog**: Written in friendly, outcome-focused language for product end-users and App Store / Play Store "What's New" release descriptions.
2. **Technical Engineering Release Notes**: Written with precision for developers, DevOps engineers, and QA teams, linking to commit hashes and file locations.

---

## Dual Output Report Format

```markdown
# 📝 Release Notes: v<X.Y.Z> (<Date>)

**Base Revision**: `<previous-tag>` ➔ **Current**: `v<X.Y.Z>` (`<short-hash>`)  
**Total Commits**: `<N>` commits across `<M>` changed files

---

## 📱 Part 1: User-Facing "What's New" (App Store / Changelog)

### What's New in Version <X.Y.Z>
- 🚀 **<Feature 1 Title>**: <Clear 1-sentence description of the user benefit>
- 🚀 **<Feature 2 Title>**: <Clear 1-sentence description>
- 🐛 **Bug Fixes & Improvements**:
  - Fixed an issue where <brief description of user-facing fix>.
  - Enhanced loading speeds when navigating between tabs.
  - General performance and stability improvements.

---

## 💻 Part 2: Technical Engineering Release Summary

### ⚠️ Breaking Changes & Migrations
- `<None / Detailed migration instructions if public API or database schema changed>`

### 🚀 New Features
- **feat(auth)**: Add biometric authentication (Face ID / Fingerprint) (`[abc1234]`)
- **feat(profile)**: Implement user avatar upload with crop support (`[def5678]`)

### 🐛 Bug Fixes
- **fix(api)**: Handle expired refresh token gracefully without crash (`[ghi9012]`)
- **fix(ui)**: Resolve keyboard overflow on checkout form (`[jkl3456]`)

### ⚡ Performance & Refactoring
- **perf(list)**: Virtualize product catalog list with caching (`[mno7890]`)
- **refactor(network)**: Standardize Dio error interceptors (`[pqr1234]`)

### 🛠️ Dependencies & Build
- Upgraded Flutter SDK to 3.24.3
- Updated `pnpm` packages to patch CVE-2024-XXXX

---

### Contributors & Commit Metrics
- `<N>` files changed (`+A insertions`, `-B deletions`)
- Ready for publishing to `CHANGELOG.md`.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
