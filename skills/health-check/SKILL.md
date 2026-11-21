---
name: health-check
description: >-
  Perform a comprehensive technical health check and code audit of the project. Evaluates architecture,
  dependency health, error handling, performance risks, test coverage, and technical debt. Produces a prioritized
  report categorized by severity (Critical, High, Medium, Low). Use when user invokes /health-check or asks for
  "health check", "audit project", "evaluate codebase quality", or "technical debt analysis".
---

# Project Health Check Workflow

This workflow performs a structured, end-to-end technical audit of an existing codebase to detect architecture smells, performance bottlenecks, unhandled failure modes, testing gaps, and security risks.

> [!IMPORTANT]
> **Audit-Only**: This workflow inspects and analyzes the codebase. It does **NOT** automatically modify files or dependencies. All recommendations include exact file references and actionable remediation steps.

---

## Audit Dimensions

The audit systematically reviews 8 core pillars:

1. **Architecture & Modularity**:
   - Boundary enforcement (layer leakage, e.g. database logic inside UI components/widgets).
   - Circular dependencies, God classes/files (> 400-500 LOC), and spaghetti control flow.
2. **Error Handling & Resilience**:
   - Unhandled promises, empty catch blocks, or silent swallowed exceptions.
   - Global error boundary and crash reporting presence.
3. **Dependency Health**:
   - Outdated dependencies with known deprecations or major version gaps.
   - Redundant or overlapping packages (e.g. using both Axios and Fetch, multiple date libraries).
4. **Code Quality & Static Analysis**:
   - Unresolved linter warnings and compiler diagnostics.
   - Dead or commented-out code, duplicate logic, and `TODO`/`FIXME` density.
5. **Security & Sensitive Data**:
   - Hardcoded tokens, API keys, or plaintext secrets in source code.
   - Permissive CORS or missing input validation on user-facing boundaries.
6. **Performance & Memory**:
   - N+1 query patterns, excessive re-renders (missing memoization), large unoptimized assets.
   - Resource leaks (unclosed streams, subscriptions, or database connections).
7. **Test Coverage & Confidence**:
   - Presence of unit, integration, and widget/component tests.
   - Fragile tests or lack of test coverage for critical business logic paths.
8. **Configuration & Environment**:
   - Presence of `.env.example`, clear build configurations, and container/CI setup.

---

## Execution Process

### Step 1: Automated Diagnostics & Stack Detection
1. Detect project type using the bundled detector:
   ```bash
   python3 ~/.gemini/config/plugins/global-workflows/scripts/project_detector.py --json
   ```
2. Run non-destructive project linters/analyzers if configured:
   - Flutter: `dart analyze` or `flutter analyze`
   - Node / React / Next.js: `npm run lint` or `npx eslint .` / `tsc --noEmit`
   - Laravel: `php artisan test --no-coverage` or `composer check` / `phpstan`
3. Check for secrets or sensitive files committed to Git:
   ```bash
   python3 ~/.gemini/config/plugins/global-workflows/scripts/git_inspector.py --json
   ```

### Step 2: In-Depth Code Inspection
- Sample key architectural files: entry points, API clients, state containers, and routing definitions.
- Inspect large files (> 300 LOC) to detect SRP (Single Responsibility Principle) violations.
- Check error handling patterns across async boundaries.

### Step 3: Synthesis & Report Generation
Categorize all verified findings into 4 priority tiers:
- **CRITICAL (P0)**: Security vulnerabilities, secret leaks, data corruption risks, broken build/crashes.
- **HIGH (P1)**: Unhandled runtime errors, severe performance bottlenecks, major architectural leaks, broken tests.
- **MEDIUM (P2)**: Missing tests on core logic, outdated deprecated packages, code duplication, missing error states.
- **LOW (P3)**: Minor naming inconsistencies, missing documentation, lint formatting tweaks, non-critical tech debt.

---

## Output Report Format

```markdown
# 🩺 Project Health Check Audit Report

**Project**: `<Project Root>`  
**Stack**: `<Framework & Language>`  
**Overall Status**: 🟢 Healthy | 🟡 Needs Attention | 🔴 At Risk

---

### Summary of Findings
| Severity | Count | Primary Impact Area |
| :--- | :--- | :--- |
| 🔴 **Critical** | `X` | Security / Crashes |
| 🟠 **High** | `Y` | Architecture / Error Handling |
| 🟡 **Medium** | `Z` | Technical Debt / Test Coverage |
| 🔵 **Low** | `W` | Code Cleanliness / Minor Lints |

---

### Detailed Findings

#### 🔴 Critical Issues
- **[File Name](file:///path/to/file#L12)**: `<Issue Title>`
  - **Problem**: <Clear description of the defect or vulnerability>
  - **Why It Matters**: <Real-world impact on system stability, security, or data>
  - **Recommended Fix**:
    ```language
    // Proposed solution or refactor snippet
    ```

#### 🟠 High Priority Issues
- **[File Name](file:///path/to/file#L45)**: `<Issue Title>`
  - **Problem**: ...
  - **Why It Matters**: ...
  - **Recommended Fix**: ...

#### 🟡 Medium Priority Issues
- **[File Name](file:///path/to/file#L100)**: `<Issue Title>`
  - **Problem & Recommendation**: ...

#### 🔵 Low Priority Improvements
- `<Improvement 1>`
- `<Improvement 2>`

---

### Recommended Action Plan (Next Steps)
1. **Immediate (Next 24h)**: Fix Critical items.
2. **Short-Term (Next Sprint)**: Refactor High priority items.
3. **Maintenance**: Address Medium debt during feature cycles.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
