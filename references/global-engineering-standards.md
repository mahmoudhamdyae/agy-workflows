# Global Engineering Standards

This document establishes the mandatory engineering, safety, and operational standards for all global workflows in Antigravity IDE. All workflows across every category must adhere to these principles.

---

## 1. Project Awareness Principles

Every workflow must dynamically discover and adapt to the current project context without hardcoded assumptions:

1. **Workspace & Root Detection**:
   - Always resolve the actual project root and workspace boundaries (e.g., via `git rev-parse --show-toplevel` or filesystem traversal to the nearest package manifest).
   - Recognize multi-module or monorepo layouts (e.g., frontend + backend, Flutter packages).
2. **Technology & Framework Discovery**:
   - Inspect package manifests (`pubspec.yaml`, `package.json`, `composer.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `requirements.txt`).
   - Identify exact framework versions (e.g. Flutter 3.x, Next.js 14/15, React 18/19, Laravel 10/11, Node.js LTS).
3. **Architecture & Directory Inspection**:
   - Inspect the existing folder organization (e.g., Clean Architecture, Feature-First, MVC, Atomic Design).
   - Never impose an alien directory structure or architectural pattern on an existing codebase.
4. **Project Documentation First**:
   - Always read existing project instructions and guidelines: `README.md`, `AGENTS.md`, `GEMINI.md`, `DESIGN.md`, `ARCHITECTURE.md`.
   - Adhere to project-specific styling, linting, and naming rules before applying global fallbacks.
5. **Skill Discovery & Reuse**:
   - Check available project-specific and ecosystem skills (e.g., Flutter MCP tools, Android CLI, Canva, Figma) and leverage them instead of reinventing existing toolchains.

---

## 2. Engineering & Architecture Standards

1. **Production-Ready & Stable**:
   - Always apply current stable, officially recommended industry patterns (e.g., Dart 3 patterns, React Server Components where applicable, modern PHP 8.2+ attributes, TypeScript strict typing).
   - Avoid deprecated APIs, experimental unstable flags, or unmaintained libraries.
2. **Simplicity Over Abstraction**:
   - Prefer clean, straightforward, maintainable code.
   - Avoid premature optimization and unnecessary abstractions (no gratuitous factories, unnecessary wrappers, or complex generic layers when simple functions suffice).
3. **Separation of Concerns & Modularity**:
   - Maintain clear boundaries between UI / Presentation, Business Logic / Domain, and Data Access / Repositories.
   - Keep functions and widgets focused on a single responsibility.
4. **Preserve Existing Functionality**:
   - Ensure complete backward compatibility unless an explicit breaking change is requested and approved.
   - Do not refactor unrelated code or touch files outside the workflow's scope.
5. **Performance, Accessibility, & Security**:
   - Consider memory allocations, UI frame budget (60/120fps), network payload size, and database query complexity.
   - Respect accessibility standards (WCAG 2.1 AA, proper ARIA / semantics, minimum touch targets).
   - Sanitize all external inputs and prevent injections.

---

## 3. Safety & Security Standards

1. **Zero Secret Leakage**:
   - Never print, commit, stage, or log secrets, API keys, private keys (`.pem`, `.key`, `id_rsa`), tokens, passwords, or `.env` content.
   - Automatically exclude sensitive files from version control and reports.
2. **User Data & Code Preservation**:
   - Never overwrite unstaged user changes without explicit user permission.
   - Never execute destructive operations (`git reset --hard`, `git clean -fd`, `rm -rf`, force-pushing) automatically.
3. **Evidence-Based Verification**:
   - Never claim an operation or build succeeded without verifying terminal output or status codes.
   - Distinguish clearly between confirmed evidence (compiler output, test results, git status) and speculative assumptions.
4. **Minimal Interruption Principle**:
   - Do not ask trivial or repetitive questions.
   - Prompt the user only when an essential requirement is missing, a destructive action could occur, or multiple valid architectural options have divergent trade-offs.

---

## 4. Execution Lifecycle Standards

Every global workflow must follow this structured 7-step lifecycle:

```text
[1. Context Understanding] ➔ [2. File Inspection] ➔ [3. Analysis & Screening]
         ➔ [4. Planning] ➔ [5. Scoped Execution] ➔ [6. Verification] ➔ [7. Structured Report]
```

1. **Understand Context**: Detect workspace, framework, and exact user goal.
2. **Inspect Files**: Read manifests, relevant source code, and project docs.
3. **Analyze**: Evaluate dependencies, syntax, constraints, and safety boundaries before touching code.
4. **Plan**: Formulate a concise execution plan for complex tasks.
5. **Execute**: Implement strictly within the approved scope.
6. **Verify**: Run tests, static analysis, builds, or diff checks to ensure zero regressions.
7. **Report**: Deliver a structured, actionable summary highlighting what was completed, verified, and any open considerations.
