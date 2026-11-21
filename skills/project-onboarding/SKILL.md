---
name: project-onboarding
description: >-
  Analyze and understand any project when opening it for the first time. Inspects tech stack, versions,
  architecture, entry points, dependencies, environment configs, APIs, and documentation. Produces a concise
  architectural overview. Use when user invokes /project-onboarding or asks to "onboard this project",
  "explain this codebase", "project overview", or "analyze project structure".
---

# Project Onboarding Workflow

This workflow systematically analyzes and demystifies any codebase—regardless of programming language, framework, or architecture—to provide an immediate, accurate mental model without modifying any files.

> [!NOTE]
> **Read-Only Inspection**: This workflow is purely analytical. It must **NOT** create, edit, or delete any project files unless the user explicitly requests documentation generation.

---

## Workflow Execution Steps

### Phase 1: Context & Stack Detection

1. **Locate Workspace Root & Project Boundaries**:
   Identify the project root and check whether it is a monorepo or single-package codebase:
   ```bash
   python3 ~/.gemini/config/plugins/global-workflows/scripts/project_detector.py --json
   ```

2. **Inspect Technology & Versions**:
   Identify the primary stack and ecosystem:
   - **Flutter / Dart**: Inspect `pubspec.yaml`, Flutter SDK constraint, and dependencies.
   - **Next.js / React / Node.js**: Inspect `package.json`, `tsconfig.json`, React/Next version, and package manager (`npm`, `pnpm`, `yarn`, `bun`).
   - **Laravel / PHP**: Inspect `composer.json`, PHP version requirement, and Laravel packages.
   - **Python / Go / Rust**: Inspect `pyproject.toml`, `requirements.txt`, `go.mod`, or `Cargo.toml`.

3. **Read Existing Documentation**:
   Examine any existing documentation files to capture project intent and conventions:
   - `README.md`, `AGENTS.md`, `GEMINI.md`, `DESIGN.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`.

---

### Phase 2: Architectural & Structural Inspection

1. **Map Directory Structure**:
   Inspect top-level directories and core code folders:
   - Flutter: `lib/`, `lib/core/`, `lib/features/`, `lib/src/`, `assets/`, `test/`.
   - Next.js / React: `app/` (App Router) vs `pages/` (Pages Router), `src/components/`, `src/hooks/`, `src/lib/`.
   - Laravel: `app/Http/Controllers/`, `app/Models/`, `routes/`, `resources/views/`, `database/migrations/`.
   - Backend APIs: `routes/`, `controllers/`, `services/`, `repositories/`, `prisma/` or `database/`.

2. **Identify Application Entry Points**:
   Locate entry points and bootstrapping code:
   - Flutter: `lib/main.dart` (or environment-specific entry points like `main_dev.dart`).
   - React / Next.js: `app/layout.tsx`, `pages/_app.tsx`, or `src/index.tsx`.
   - Laravel: `public/index.php`, `bootstrap/app.php`.
   - Node.js: `src/server.ts`, `src/index.ts`, `server.js`.

3. **Evaluate Architecture Pattern**:
   Identify the architectural pattern in use:
   - Clean Architecture / Domain-Driven Design (Domain, Data, Presentation layers).
   - Feature-First / Modular Architecture.
   - MVC (Model-View-Controller).
   - Server-Driven / Microservices / Monolith.

---

### Phase 3: Subsystem & Integration Analysis

1. **State Management**:
   - Flutter: Bloc/Cubit, Riverpod, Provider, MobX, GetX, or native `ValueNotifier`.
   - React / Next.js: Zustand, Redux Toolkit, React Query / TanStack, Context API.
2. **API & Network Integration**:
   - HTTP clients: Dio, `http`, Axios, Fetch, React Query, RTK Query, Guzzle, or GraphQL.
   - Base URLs, environment endpoints, interceptors, and error handling wrappers.
3. **Authentication & Authorization**:
   - Identify Auth mechanism: Firebase Auth, Supabase, OAuth2/OIDC, JWT, Session/Sanctum, NextAuth/Auth.js.
4. **Database & Persistence**:
   - Identify ORMs/Databases: Drift, Hive, Isar, Shared Preferences, Prisma, Drizzle, Mongoose, Eloquent, PostgreSQL, SQLite.
5. **Environment Configuration**:
   - Check `.env.example`, `config/`, or build flavor configurations. (Never read or expose production `.env` values!).
6. **Testing & QA Strategy**:
   - Identify test suites: Unit tests, Widget/Component tests, Integration/E2E tests (Playwright, Cypress, Flutter Driver).
   - Check linting configs: `analysis_options.yaml`, `.eslintrc`, `biome.json`, `phpstan.neon`.

---

### Phase 4: Output Synthesis

Present a clear, structured Onboarding Brief:

```markdown
# 🧭 Project Onboarding Overview: <Project Name>

### 1. Technology Stack & Key Versions
- **Primary Framework**: <e.g., Flutter 3.24 / Next.js 15 (App Router) / Laravel 11>
- **Language**: <e.g., Dart 3.5 / TypeScript 5.5 / PHP 8.3>
- **Package Manager**: <e.g., pub / pnpm / composer>
- **Entry Points**: `<path/to/main>`

### 2. Architecture & Code Layout
- **Pattern**: <e.g., Feature-First Clean Architecture>
- **Directory Breakdown**:
  - `dir/`: <purpose>
  - `dir/`: <purpose>

### 3. Core Subsystems
- **State Management**: <e.g., Flutter Bloc / Zustand>
- **Network & API**: <e.g., Dio with custom interceptors / TanStack React Query>
- **Authentication**: <e.g., Supabase Auth / JWT via http-only cookies>
- **Database / Storage**: <e.g., Drift / PostgreSQL via Prisma>

### 4. Developer Workflows & Commands
- **Install Dependencies**: `<command>`
- **Run Locally**: `<command>`
- **Execute Tests**: `<command>`
- **Lint / Analyze**: `<command>`

### 5. Key Architecture Considerations & Guidelines
- <Crucial insight about conventions, flavors, or architectural constraints found in code>
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
