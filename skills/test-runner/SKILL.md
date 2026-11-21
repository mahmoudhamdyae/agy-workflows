---
name: test-runner
description: >-
  Intelligently detect, select, and execute project test suites across Flutter, Next.js, React, Node.js,
  and Laravel. Runs unit, widget/component, and integration tests, parses test failure outputs, distinguishes
  code defects from environment issues, and produces an execution report. Never modifies tests just to make
  them pass. Use when user invokes /test-runner or asks to "run tests", "execute test suite", or "verify tests".
---

# Test Runner Workflow

This workflow automatically discovers the project's testing frameworks, selects the appropriate test scope (full suite, changed files, or single module), runs the tests, and diagnoses failures with root-cause precision.

> [!IMPORTANT]
> **Test Integrity Mandate**: Never modify test assertions or comment out failing tests simply to achieve a "green" pass. Tests are specifications of correct behavior. If a test fails, the agent must diagnose whether the implementation has a bug, the test expectation is outdated due to an intentional requirements change, or the local environment is misconfigured.

---

## 5-Step Execution Lifecycle

### Step 1: Detect Testing Toolchain & Config
1. Inspect manifests using the project detector:
   ```bash
   python3 ~/.gemini/config/plugins/global-workflows/scripts/project_detector.py --json
   ```
2. Identify available test frameworks:
   - **Flutter / Dart**: `flutter test` (unit and widget tests), `flutter test integration_test/` (integration tests). Check `test/` directory.
   - **React / Next.js**: Jest, Vitest, Playwright, Cypress. Check `package.json` scripts (`"test"`, `"test:unit"`, `"test:e2e"`).
   - **PHP / Laravel**: PHPUnit (`vendor/bin/phpunit`), Pest (`php artisan test` or `./vendor/bin/pest`).
   - **Node.js**: Jest, Mocha, Vitest, Node test runner (`node --test`).
   - **Python**: `pytest` or `unittest`.

---

### Step 2: Determine Scope of Execution
Determine which tests to run based on the user's prompt and git status:
1. **Targeted / Impacted Tests (Fastest)**:
   - Run tests covering only modified files found in `git status`:
     - e.g. modified `lib/features/auth/auth_service.dart` ➔ run `test/features/auth/auth_service_test.dart`.
2. **Full Unit & Component Suite**:
   - Run all fast in-memory unit/widget tests.
3. **End-to-End / Integration Suite**:
   - Run if explicitly requested or pre-release verification is needed.

---

### Step 3: Execute Tests Safely
Run the specific commands without destructive flags:

```bash
# Flutter
flutter test --no-pub

# React / Next.js / Node.js
npm test -- --watch=false

# Laravel
php artisan test --parallel

# Python
pytest -v
```

---

### Step 4: Failure Diagnostics & Root Cause Analysis
If tests fail:
1. **Distinguish Failure Category**:
   - **Assertion Failure (Logic Defect)**: `Expected: 'Active', Actual: 'Pending'`. The implementation does not match expected business logic.
   - **Unhandled Exception / Crash**: Null pointer, missing mock dependency, unawaited promise rejection.
   - **Environment / Setup Failure**: Missing database connection, missing `.env` test variables, port collision, missing browser binary (for Playwright/Puppeteer).
2. **Locate Exact Code Reference**:
   - Extract the failing file, test case name, and line number.
   - Inspect the failed assertion and the call stack.

---

### Step 5: Present Test Execution Report

```markdown
# 🧪 Test Execution Report

**Framework**: `<Flutter Test / Vitest / Jest / Pest>`  
**Command Executed**: `<exact command>`  
**Overall Status**: ✅ All Passed | 🔴 Failures Detected | ⚠️ Environment Blocked

---

### Summary Metrics
- **Tests Passed**: `X`
- **Tests Failed**: `Y`
- **Tests Skipped**: `Z`
- **Duration**: `X.XXs`

---

### Test Failures Breakdown (If Any)

#### 🔴 Failure 1: `<Test Suite Name>` ➔ `<Test Case Name>`
- **Location**: `[test_file.dart](file:///path/to/test#L50)`
- **Failure Type**: Assertion Failure / Unhandled Exception
- **Expected**: `<Expected Value>`
- **Actual**: `<Actual Value Received>`
- **Diagnosis & Root Cause**:
  - The function `<functionName>` returns false because input validation does not account for empty string trimming.
- **Recommended Remediation**:
  - Update `lib/path/to/source.dart#L25` to trim whitespace before validation.

---

### Scope Coverage Note
- **What Was Tested**: Unit tests under `test/unit/` and widget tests under `test/widgets/`.
- **What Was NOT Tested**: E2E integration tests (require running emulator/backend).
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
