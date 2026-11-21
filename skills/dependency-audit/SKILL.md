---
name: dependency-audit
description: >-
  Audit project dependencies across Flutter, Node.js, Next.js, Laravel, and Python codebases. Inspects installed
  vs latest stable versions, flags deprecated or abandoned libraries, checks CVE security advisories, detects
  unused packages, and produces a prioritized, non-destructive upgrade plan. Never updates major versions blindly.
  Use when user invokes /dependency-audit or asks to "audit dependencies", "check outdated packages", or "update libraries".
---

# Dependency Audit Workflow

This workflow conducts a comprehensive, non-destructive audit of third-party dependencies, packages, and plugins to ensure stability, security, and compatibility.

> [!IMPORTANT]
> **Safe Upgrade Principle**: This workflow does **NOT** execute destructive `update` or major version upgrades automatically. Major dependency changes frequently introduce breaking API shifts. The agent produces a categorized, risk-rated upgrade plan and waits for explicit user confirmation before applying updates.

---

## 4-Step Audit Process

### Step 1: Detect Ecosystem & Package Manifests
1. Identify package manager and manifest files:
   - **Flutter / Dart**: `pubspec.yaml`, `pubspec.lock`
   - **Node.js / Next.js / React**: `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lockb`
   - **PHP / Laravel**: `composer.json`, `composer.lock`
   - **Python**: `pyproject.toml`, `requirements.txt`, `Pipfile.lock`

2. Inspect direct dependencies vs developer tooling dependencies.

---

### Step 2: Run Ecosystem Audit Commands (Read-Only)
Execute the native inspection tools in read-only/dry-run mode:

- **Flutter / Dart**:
  ```bash
  flutter pub outdated
  ```
  *(Checks current, upgradable, and resolvable latest versions).*

- **Node.js / npm / pnpm / yarn**:
  ```bash
  npm audit --json  # or pnpm audit / yarn audit
  npm outdated
  ```
  *(Flags known CVEs and outdated package versions).*

- **PHP / Laravel**:
  ```bash
  composer audit
  composer outdated --direct
  ```
  *(Checks Packagist security advisories and outdated packages).*

- **Python**:
  ```bash
  pip list --outdated  # or pip-audit if installed
  ```

---

### Step 3: Analyze Risk & Compatibility
Categorize all flagged packages into 4 update tiers:

1. **🔴 Security Vulnerabilities (CVEs)**:
   - High or Critical severity vulnerabilities reported by security advisories.
2. **🟠 Deprecated or Abandoned Packages**:
   - Packages officially marked deprecated on pub.dev, npmjs.org, or packagist.org.
   - Packages with zero maintenance (> 2 years) or replaced by native framework APIs (e.g., using an old third-party package when Flutter or Node provides built-in support).
3. **🟡 Major Version Updates (Breaking Changes Expected)**:
   - SemVer major bumps (e.g. `v4.x` ➔ `v5.0.0`).
   - Requires reviewing migration guides before touching code.
4. **🟢 Minor & Patch Updates (Safe / Non-Breaking)**:
   - Bug fixes and backwards-compatible feature additions (e.g. `v1.2.1` ➔ `v1.2.4`).

---

### Step 4: Generate Prioritized Upgrade Report

```markdown
# 📦 Dependency Health & Upgrade Audit

**Ecosystem**: `<Flutter / npm / Composer>`  
**Manifest**: `<pubspec.yaml / package.json / composer.json>`  
**Total Dependencies**: `<Total direct: X, Dev: Y>`

---

### 1. 🚨 Security Vulnerabilities (Immediate Action Required)
| Package | Installed | Vulnerability | Severity | Advisory / CVE | Patched In |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `<name>` | `v1.0.0` | `<summary>` | High | `CVE-2024-XXXX` | `v1.0.4` |

---

### 2. ⚠️ Deprecated or Abandoned Libraries
- **`<package>`** (`vX.Y.Z`): Marked deprecated on registry.
  - *Recommendation*: Migrate to `<official-alternative>`.

---

### 3. 🔄 Outdated Packages Breakdown

#### Safe Updates (Minor / Patch — No Breaking Changes)
- `<pkg1>`: `1.2.0` ➔ `1.2.5`
- `<pkg2>`: `2.4.1` ➔ `2.4.9`

#### Major Updates (Potential Breaking Changes — Requires Plan)
- `<pkg3>`: `2.1.0` ➔ `3.0.0` (Breaking: API changed for X method. Review migration guide).

---

### 4. 🧹 Potential Unused Dependencies
- `<pkg>`: Listed in manifest but not found in any import statement across `src/` or `lib/`.

---

### 5. Recommended Execution Plan
1. **Step 1 (Safe)**: Update minor/patch versions and re-test:
   ```bash
   <command to apply safe patches>
   ```
2. **Step 2 (Security)**: Upgrade vulnerable packages individually to patched versions.
3. **Step 3 (Planned)**: Schedule major upgrades with dedicated regression testing.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
