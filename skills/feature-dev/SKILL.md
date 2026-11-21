---
name: feature-dev
description: >-
  Implement new features in existing codebases while strictly honoring the established architecture,
  design patterns, and coding conventions. Handles all UI/state/network states (loading, success, empty, error),
  adds automated tests, and verifies zero regressions. Use when user invokes /feature-dev or asks to
  "build a new feature", "implement feature", "add capability", or "create screen/module".
---

# Feature Development Workflow

This workflow guides the implementation of new features into any existing codebase. It ensures the new code fits naturally into the existing project patterns without introducing alien architectures, unnecessary third-party packages, or breaking existing functionality.

---

## 10-Step Implementation Process

```text
[1. Requirements Clarification] ➔ [2. Codebase Inspection] ➔ [3. Dependency & Pattern Mapping]
       ➔ [4. Architecture Plan] ➔ [5. Incremental Implementation] ➔ [6. State Coverage]
       ➔ [7. Testing] ➔ [8. Static Analysis & Build] ➔ [9. Self-Review] ➔ [10. Completion Report]
```

### Step 1: Understand Requirements
- Break down the user's feature request into concrete domain entities, UI components, business logic rules, and data persistence/API requirements.
- Identify edge cases, permissions, input constraints, and failure modes.

### Step 2: Inspect Existing Implementation
- Locate existing similar features to understand the project's idioms:
  - How are models structured? (e.g. Freezed / Equatable in Flutter, Zod / TypeScript interfaces in Next.js).
  - How is state managed? (Bloc, Riverpod, Zustand, Redux, Pinia, Livewire).
  - How are APIs invoked? (Repository pattern, API services, direct queries).
  - How are UI components styled? (Tailwind, CSS Modules, Styled Components, Flutter Material/Cupertino widgets).

### Step 3: Map Affected Files & Integration Points
- Identify existing files that need modifications (routes, navigation bars, dependency injection containers, service locators).
- Identify new files to be created following existing file and folder naming conventions.

### Step 4: Propose an Implementation Plan
- For complex or multi-file features, outline a concise plan:
  - 1. Data Layer: Models, API clients, DTOs, migrations.
  - 2. Domain / Business Logic Layer: Services, repositories, state managers (Blocs/Stores).
  - 3. UI / Presentation Layer: Components, pages/screens, routing.
  - 4. Test Strategy: Unit tests, component tests.
- Proceed once the direction is sound.

### Step 5: Implement Incrementally
- Write clean, type-safe, maintainable code following existing patterns.
- Reuse existing shared UI components (buttons, inputs, modals, loaders) rather than building duplicates.
- Keep functions and widgets modular with clear single responsibilities.

### Step 6: Ensure Complete State Coverage
Every user-facing feature must explicitly handle all 4 core UI states:
1. **Loading State**: Shimmers, spinners, or skeletons while fetching/mutating data.
2. **Success State**: Clean, responsive rendering of data.
3. **Empty State**: User-friendly visual and message when no items/data exist, with call-to-action if appropriate.
4. **Error State**: Informative error messaging, retry mechanism, and logging without raw stack traces.

### Step 7: Add or Update Automated Tests
- Add unit tests for business logic, services, and state reducers/blocs.
- Add widget/component tests verifying rendering of key states (loading, error, success).
- Ensure new tests adhere to project testing conventions.

### Step 8: Build & Static Analysis Verification
Run the project's native build and verification commands:
- Flutter: `flutter analyze && flutter test`
- Next.js / React: `npm run lint && npm test`
- Laravel: `php artisan test` or `vendor/bin/phpunit`

### Step 9: Verify No Regressions
- Check `git diff` to confirm that untouched files were not inadvertently changed.
- Verify that existing tests continue to pass.

### Step 10: Present Final Feature Summary
Output a concise completion summary detailing:
- Files created and modified.
- Architectural patterns followed.
- State handling implementation.
- Verification results (build, lint, test execution).

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
