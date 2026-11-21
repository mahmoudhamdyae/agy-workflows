---
name: refactor
description: >-
  Refactor and restructure existing code to improve maintainability, readability, performance, and separation
  of concerns without altering external behavior. Strictly preserves public API interfaces and backwards
  compatibility, runs tests before and after refactoring, and avoids scope creep. Use when user invokes /refactor
  or asks to "refactor code", "clean up this file", "reduce complexity", or "extract reusable component".
---

# Refactoring Workflow

This workflow systematically cleans, simplifies, and restructures existing code to eliminate code smells, reduce cognitive complexity, and improve modularity while strictly preserving external behavior.

> [!IMPORTANT]
> **Zero Behavioral Change Mandate**: Refactoring improves the internal structure of code without modifying its observable external behavior. Public interfaces, API endpoints, return types, and side effects must remain intact. If any behavior change is strictly unavoidable, it must be explicitly highlighted and approved prior to implementation.

---

## Refactoring Targets & Code Smells

1. **Large Classes & God Files (> 300-400 LOC)**: Decompose into focused single-responsibility classes or hooks/widgets.
2. **Deep Nesting & Cyclomatic Complexity**: Replace nested `if/else` and callback pyramids with guard clauses, early returns, polymorphism, or switch pattern matching.
3. **Duplicated Code (DRY Violations)**: Extract identical algorithms or UI chunks into reusable utility functions or shared components.
4. **Poor Naming & Mystery Numbers**: Replace vague abbreviations and magic numbers with descriptive constants and meaningful domain identifiers.
5. **Separation of Concerns**: Decouple data parsing, business validation, and UI layout into proper layers.
6. **State & Mutation Smells**: Replace mutable shared state with clean, predictable unidirectional data flow.

---

## 6-Step Refactoring Process

```text
[1. Baseline & Test Run] ➔ [2. Scope Boundary Definition] ➔ [3. Pattern Selection]
         ➔ [4. Incremental Transformation] ➔ [5. Regression Verification] ➔ [6. Diff Audit & Report]
```

### Step 1: Establish the Baseline
1. Inspect the target file(s) and determine their dependencies and callers.
2. Run existing tests before making any edits:
   ```bash
   # Flutter: flutter test path/to/test.dart
   # Node / Next: npm test -- path/to/test.ts
   # Laravel: php artisan test --filter TargetTest
   ```
   If tests fail before refactoring starts, document the pre-existing failures to avoid misattributing them.

### Step 2: Define Strict Scope Boundaries
- Confine all changes strictly to the file(s) or module requested by the user.
- Do NOT touch unrelated files or rewrite the application architecture.
- Do NOT introduce new heavy libraries or frameworks for small refactorings.

### Step 3: Select the Appropriate Refactoring Technique
- **Extract Method / Function**: Isolate cohesive logic blocks.
- **Extract Widget / Component**: Break oversized UI build trees into smaller, const-constructible widgets or memoized components.
- **Introduce Parameter Object / DTO**: Group unwieldy argument lists (> 4 parameters).
- **Replace Conditional with Pattern Matching**: Use Dart 3 switch expressions, modern TypeScript discriminated unions, or PHP 8.x `match` expressions.
- **Guard Clauses**: Invert conditions to return early and flatten indentation.

### Step 4: Transform Incrementally
- Apply changes in small, logical steps.
- Preserve all existing public method signatures, exported functions, and class names so external callers do not break.
- If deprecating an old method in favor of an improved one, keep the old method as a forwarded wrapper where necessary to preserve compatibility.

### Step 5: Verify Zero Regressions
1. Re-run the test suite:
   - Ensure 100% of previously passing tests continue to pass.
2. Run static analysis and linting:
   - Verify zero new compiler warnings or lint errors.
3. Inspect `git diff`:
   - Verify that the diff represents a cleaner, more readable implementation of the exact same contract.

### Step 6: Present Refactoring Summary
Provide a concise comparison report:
- **Files Refactored**.
- **Key Improvements Made** (e.g., complexity reduced, duplicate code eliminated, widgets extracted).
- **Compatibility Confirmation** (Public APIs preserved).
- **Test & Analysis Results**.

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
