---
name: code-review
description: >-
  Review code changes (unstaged, staged, PR branch diff, or specified files/modules) for logic bugs,
  security vulnerabilities, performance defects, edge cases, and architectural compliance. Produces prioritized,
  actionable findings with line links and fixes. Use when user invokes /code-review or asks to "review my code",
  "review this PR", "review git diff", or "inspect code quality".
---

# Code Review Workflow

This workflow provides a rigorous, senior-level code review focusing on **correctness, security, performance, resilience, and architectural integrity**. It avoids bikeshedding over subjective formatting preferences and delivers high-signal, actionable feedback.

> [!IMPORTANT]
> **Advisory Scope**: This workflow evaluates and critiques code. It does **NOT** automatically edit code files unless the user explicitly asks to apply recommended fixes.

---

## Review Scope Determination

The agent inspects the review target based on user context:
1. **Uncommitted Changes (Default)**:
   - Staged + unstaged working tree diff: `git diff HEAD`
   - Staged changes only: `git diff --staged`
2. **Branch / PR Diff**:
   - Compare current feature branch against main/base:
     ```bash
     git diff origin/main...HEAD
     ```
3. **Explicit Files / Directories**:
   - Read and review specific files provided by the user (e.g. `/code-review lib/features/auth/`).

---

## 10 Critical Review Dimensions

Review every line of code against these 10 criteria:

1. **Logic Bugs & Flaws**:
   - Off-by-one errors, reversed conditionals, flawed boolean expressions, unintended infinite loops or deadlocks.
2. **Null Safety & Edge Cases**:
   - Unhandled `null`/`undefined`, empty arrays/collections, missing return cases, division by zero, type mismatches.
3. **Security Vulnerabilities**:
   - Injection risks (SQL, Command, NoSQL), XSS, CSRF, insecure deserialization, broken access controls, secrets checked into code.
4. **Asynchronous & Concurrency Issues**:
   - Missing `await`, race conditions, unhandled rejected promises, uncancelled timers/streams, stale closures in React hooks.
5. **State Management & Data Flow**:
   - Uncontrolled side-effects, mutating immutable state, inconsistent state transitions, missing loading/error flags.
6. **Error Handling & Fault Tolerance**:
   - Swallowed exceptions (empty `catch {}`), lack of user-facing feedback on failure, unhandled network disconnections.
7. **Performance & Memory Leaks**:
   - O(N²) or heavier algorithms on large inputs, un-indexed queries, missing UI list virtualization, unclosed file/socket handles.
8. **Architectural & Layer Boundaries**:
   - UI code invoking database queries directly, bypass of repository/service layer, circular module imports.
9. **Code Duplication & Reusability**:
   - Copy-pasted blocks that should leverage existing shared project utilities.
10. **Testability & Test Coverage**:
    - Untested edge cases, hardcoded dependencies that prevent unit test mocking.

---

## Review Output Format

Organize findings in descending order of severity:

```markdown
# 🔍 Senior Code Review Report

**Target**: `<Branch, Diff, or Specific Files>`  
**Total Changes**: `<+X lines, -Y lines across Z files>`  
**Verdict**: ✅ Approved | 🟡 Approved with Comments | 🔴 Changes Requested

---

### Critical Issues (Must Fix Before Merge)
- **[file.ext](file:///path/to/file.ext#L45-L52)**: `<Issue Title>`
  - **Severity**: 🔴 Critical
  - **Category**: Logic Bug / Security / Crash
  - **Problem**: <Clear explanation of what is wrong>
  - **Why It Matters**: <Concrete consequence in production>
  - **Recommended Fix**:
    ```language
    // Exact drop-in replacement snippet
    ```

---

### Important Improvements (High/Medium Priority)
- **[file.ext](file:///path/to/file.ext#L110-L115)**: `<Issue Title>`
  - **Severity**: 🟠 High / 🟡 Medium
  - **Category**: Performance / Error Handling / Maintainability
  - **Problem**: ...
  - **Why It Matters**: ...
  - **Recommended Fix**: ...

---

### Minor Notes & Edge Cases (Low Priority)
- **[file.ext](file:///path/to/file.ext#L80)**: <Concise suggestion or edge-case reminder>

---

### Summary Checklist
- [ ] Critical defects resolved
- [ ] Error states handled gracefully
- [ ] Tests added/updated for new paths
- [ ] Zero secret leaks or security vulnerabilities
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
