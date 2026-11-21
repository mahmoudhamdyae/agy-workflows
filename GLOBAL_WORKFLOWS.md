# Antigravity IDE — Global Workflows System

This documentation provides the official guide to the **18 Reusable Global Workflows** installed in Antigravity IDE and CLI. These workflows are completely project-independent, cross-stack (Flutter/Dart, Next.js, React, Laravel, Node.js, Python, Go, Rust), and discoverable across all current and future workspaces.

---

## Architecture & Installation Locations

- **Global Customization Root**: `~/.gemini/config/`
- **Global Workflows Plugin**: `~/.gemini/config/plugins/global-workflows/`
- **Global Skills Directory**: `~/.gemini/config/skills/`
- **Active Global Rules**: `~/.gemini/config/plugins/global-workflows/rules/AGENTS.md`
- **Shared Engineering Standards**: `~/.gemini/config/plugins/global-workflows/references/global-engineering-standards.md`
- **Git Security & Safety Engine**: `~/.gemini/config/plugins/global-workflows/references/git-core-engine.md`
- **Automated State & Stack Inspectors**:
  - `~/.gemini/config/plugins/global-workflows/scripts/git_inspector.py`
  - `~/.gemini/config/plugins/global-workflows/scripts/project_detector.py`

---

## Workflows Quick Reference (All 18 Workflows)

| # | Workflow Name | Slash Command | Category | Purpose | Safety / Guardrail |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **01** | **Git Commit** | `/commit` | Git & VCS | Inspects, stages safe files, and creates Conventional Commit. | **Never pushes to remote.** |
| **02** | **Git Commit & Push** | `/commit-push` | Git & VCS | Performs commit, verifies remote & upstream, pushes safely. | **Never force-pushes.** Pauses if remote ahead. |
| **03** | **Project Onboarding** | `/project-onboarding` | Analysis & Maint. | Demystifies tech stack, architecture, entry points, and workflows. | **Read-only.** Does not modify files. |
| **04** | **Project Health Check** | `/health-check` | Analysis & Maint. | Comprehensive 8-pillar audit (architecture, error handling, debt). | **Audit-only.** Outputs prioritized P0–P3 report. |
| **05** | **Code Review** | `/code-review` | Analysis & Maint. | Senior-level review of diff, branch, or module for logic & bugs. | **Advisory.** Focuses on logic over subjective style. |
| **06** | **Documentation** | `/documentation` | Analysis & Maint. | Generates grounded README, API, Architecture, and ADR docs. | **Anti-hallucination.** Only documents verified code. |
| **07** | **Feature Development** | `/feature-dev` | Development | Implements new features honoring existing design patterns. | Handles loading, error, empty, and success states. |
| **08** | **API Integration** | `/api-integration` | Development | Connects frontend to backend with DTOs, auth refresh, and errors. | **No fake endpoints.** Requires verified contract. |
| **09** | **Refactoring** | `/refactor` | Development | Restructures code for readability and SRP without behavior shifts. | **Zero behavior change.** Runs tests before & after. |
| **10** | **Dependency Audit** | `/dependency-audit` | Development | Checks for CVEs, deprecated libraries, and outdated packages. | **Never updates major versions automatically.** |
| **11** | **UX Audit** | `/ux-audit` | UI/UX & Quality | Evaluates user journeys, cognitive load, navigation, and usability. | **Empirical honesty.** No fabricated user research. |
| **12** | **UI Audit** | `/ui-audit` | UI/UX & Quality | Audits visual hierarchy, spacing, contrast (WCAG), and themes. | **Preserves brand identity.** No unapproved redesigns. |
| **13** | **Design System** | `/design-system` | UI/UX & Quality | Catalogs design tokens, unifies duplicate components and variants. | Consolidates existing tokens without alien styling. |
| **14** | **Responsive Audit** | `/responsive-audit` | UI/UX & Quality | Checks mobile, tablet, desktop scaling, overflow, and touch targets. | Flags `RenderFlex overflow` and layout clipping. |
| **15** | **Test Runner** | `/test-runner` | Testing & Security | Discovers and runs project test suites with failure diagnostics. | **Never modifies tests just to make them pass.** |
| **16** | **Pre-Release Check** | `/pre-release-check` | Testing & Security | 10-point production readiness and app store pre-flight audit. | **Never publishes or deploys automatically.** |
| **17** | **Release Notes** | `/release-notes` | Testing & Security | Generates dual-audience release notes from verified Git diffs. | **Anti-hallucination.** Grounded strictly in git log. |
| **18** | **Security Audit** | `/security-audit` | Testing & Security | Technology-adapted security review (OWASP, SQLi, XSS, CSRF). | **Zero secret leakage.** Redacts all sensitive tokens. |

---

## Detailed Workflow Breakdown

### CATEGORY A — Git & Version Control

#### 01. Git Commit (`/commit`)
- **When to Use**: When you have local modifications ready to be saved into version control.
- **Trigger**: `/commit` or *"commit my changes"*, *"make a commit"*.
- **Intelligence**: Automatically checks if Git is initialized (prompts if missing), detects in-progress operations (`MERGE_HEAD`, rebase), scans for secrets (`.env`, `.pem`, `id_rsa`), stages safe files selectively (no blind `git add .`), analyzes the staged diff, and crafts an imperative Conventional Commit message (`feat`, `fix`, `refactor`, etc.).
- **Guardrail**: **Strictly creates a local commit only. Never pushes to any remote repository.**

#### 02. Git Commit & Push (`/commit-push`)
- **When to Use**: When you want to commit local work and synchronize it with the remote repository in one safe step.
- **Trigger**: `/commit-push` or *"commit and push"*, *"commit-push"*, *"commit and sync"*.
- **Intelligence**: Executes all safety and staging checks from Git Commit, then checks remote configuration (prompts for URL if missing), identifies upstream tracking, and runs `git fetch` to detect remote divergence.
- **Guardrail**: If remote has new commits (`behind > 0`), it halts immediately and warns you to pull/rebase. **Never force-pushes (`--force`, `-f`, `--force-with-lease`).**

---

### CATEGORY B — Project Analysis & Maintenance

#### 03. Project Onboarding (`/project-onboarding`)
- **When to Use**: When opening an unfamiliar project, switching repositories, or onboarding team members.
- **Trigger**: `/project-onboarding` or *"onboard this project"*, *"explain this codebase"*, *"project overview"*.
- **Intelligence**: Runs non-destructive stack discovery (`project_detector.py`), reads documentation (`README.md`, `AGENTS.md`), maps directory structures, locates entry points (`main.dart`, `app/layout.tsx`, `artisan`), and outlines state management, API, and database architecture.
- **Output**: A comprehensive Onboarding Brief without touching a single file.

#### 04. Project Health Check (`/health-check`)
- **When to Use**: Before major refactors, when inheriting legacy code, or conducting periodic code health audits.
- **Trigger**: `/health-check` or *"health check"*, *"audit codebase"*, *"technical debt analysis"*.
- **Intelligence**: Audits 8 dimensions: Architecture, Error Handling, Dependencies, Code Quality, Security, Performance, Tests, and Configurations.
- **Output**: Prioritized report categorized into Critical (P0), High (P1), Medium (P2), and Low (P3) with exact file links and concrete remediation steps.

#### 05. Code Review (`/code-review`)
- **When to Use**: Before submitting or merging a pull request, or after drafting a complex feature.
- **Trigger**: `/code-review` or *"review my code"*, *"review git diff"*, *"review this PR"*.
- **Intelligence**: Reviews staged diffs, branch diffs against main, or specified files for logic bugs, null safety, race conditions, memory leaks, and architectural violations.
- **Output**: Prioritized review findings with clickable file line links and copy-paste drop-in fixes.

#### 06. Documentation (`/documentation`)
- **When to Use**: When creating or updating project READMEs, architecture guides, API references, or ADRs.
- **Trigger**: `/documentation` or *"update readme"*, *"document api"*, *"write architecture doc"*.
- **Intelligence**: Extracts ground truth from actual code, routes, controllers, and environment configurations. Preserves existing documentation while replacing obsolete instructions.
- **Guardrail**: Strictly prohibits inventing endpoints, flags, or features not present in the code.

---

### CATEGORY C — Development & Implementation

#### 07. Feature Development (`/feature-dev`)
- **When to Use**: When building a new user-facing capability, screen, or domain feature.
- **Trigger**: `/feature-dev` or *"build feature"*, *"implement new capability"*, *"add feature"*.
- **Intelligence**: Follows a 10-step lifecycle: Inspects existing patterns, formulates an architecture plan, implements data/domain/UI layers, covers all 4 UI states (loading, success, empty, error), adds automated tests, and verifies zero regressions.
- **Guardrail**: Never introduces alien frameworks or unnecessary third-party packages for small features.

#### 08. API Integration (`/api-integration`)
- **When to Use**: When connecting mobile/web interfaces to backend REST, GraphQL, or RPC endpoints.
- **Trigger**: `/api-integration` or *"integrate API"*, *"connect backend endpoint"*, *"add api service"*.
- **Intelligence**: Maps verified contracts into immutable models/DTOs, implements services using the project's centralized HTTP client (Dio, Axios, Fetch), hooks into auth token refresh interceptors, handles pagination, and writes mock unit tests.
- **Guardrail**: Strictly refuses to guess or invent endpoint paths or parameter names.

#### 09. Refactoring (`/refactor`)
- **When to Use**: When simplifying complex functions, eliminating duplication, or decomposing oversized files.
- **Trigger**: `/refactor` or *"refactor code"*, *"clean up this file"*, *"reduce complexity"*.
- **Intelligence**: Runs existing tests before modifying code to establish a baseline, decomposes God classes and deep nesting, preserves public APIs and backwards compatibility, and re-verifies tests after completion.
- **Guardrail**: Confines changes strictly to requested scope; never alters observable external behavior.

#### 10. Dependency Audit (`/dependency-audit`)
- **When to Use**: When reviewing outdated packages, preparing for framework upgrades, or checking for CVEs.
- **Trigger**: `/dependency-audit` or *"audit dependencies"*, *"check outdated packages"*, *"package audit"*.
- **Intelligence**: Runs native read-only audit tools (`flutter pub outdated`, `npm audit`, `composer audit`), cross-references CVE databases, and classifies updates into Safe (minor/patch) vs Breaking (major).
- **Guardrail**: Never executes major version upgrades automatically.

---

### CATEGORY D — UI/UX & Interface Quality

#### 11. UX Audit (`/ux-audit`)
- **When to Use**: When evaluating usability, user retention bottlenecks, or user onboarding flows.
- **Trigger**: `/ux-audit` or *"ux audit"*, *"evaluate usability"*, *"review user experience"*.
- **Intelligence**: Audits user flows against Nielsen Norman heuristics and WCAG guidelines: evaluates cognitive load, error prevention, form validation, feedback transparency, and empty states.
- **Guardrail**: Does not invent user research data or claim unverified assumptions are empirical facts.

#### 12. UI Audit (`/ui-audit`)
- **When to Use**: When assessing visual polish, layout alignment, contrast, or design consistency.
- **Trigger**: `/ui-audit` or *"ui audit"*, *"evaluate visual design"*, *"check styling consistency"*.
- **Intelligence**: Inspects visual hierarchy, typography scales, 8pt grid spacing rhythm, component variants, WCAG AA contrast (4.5:1), and light/dark theme fidelity.
- **Guardrail**: Respects established brand and design identity; does not redesign the UI unprompted.

#### 13. Design System (`/design-system`)
- **When to Use**: When organizing, scaling, or auditing a shared UI component library or token set.
- **Trigger**: `/design-system` or *"audit design system"*, *"catalog tokens"*, *"standardize components"*.
- **Intelligence**: Catalogs color, typography, spacing, radius, and shadow tokens. Detects design drift (hardcoded hex colors and non-grid dimensions) and unifies duplicate component implementations.

#### 14. Responsive Audit (`/responsive-audit`)
- **When to Use**: When testing multi-screen adaptation across mobile, tablet, and desktop viewports.
- **Trigger**: `/responsive-audit` or *"audit responsiveness"*, *"check mobile layout"*, *"fix layout overflow"*.
- **Intelligence**: Evaluates layouts across a 4-tier viewport matrix (320px–1920px+). Detects `RenderFlex overflow`, clipped modals, horizontal scrollbars, and touch targets below 48x48 dp/px.

---

### CATEGORY E — Testing, Security & Delivery

#### 15. Test Runner (`/test-runner`)
- **When to Use**: When running automated tests and diagnosing failures.
- **Trigger**: `/test-runner` or *"run tests"*, *"execute test suite"*, *"verify tests"*.
- **Intelligence**: Auto-discovers test runners (`flutter test`, Jest, Vitest, Pest, PHPUnit, Pytest), selects targeted tests based on modified files, executes tests safely, and diagnoses failure root causes (distinguishing logic defects from environment misconfigurations).
- **Guardrail**: Never modifies or comments out tests just to make them pass.

#### 16. Pre-Release Check (`/pre-release-check`)
- **When to Use**: Before publishing a release, pushing to App Store / Google Play, or deploying to production.
- **Trigger**: `/pre-release-check` or *"pre-release check"*, *"readiness check"*, *"verify release build"*.
- **Intelligence**: Performs a 10-point audit: Git status, zero secrets, clean static analysis, 100% passing tests, release build compilation, version/build number verification, production API endpoints, native OS permissions, and error reporting.
- **Guardrail**: Strictly advisory; never triggers deployments or uploads without explicit approval.

#### 17. Release Notes (`/release-notes`)
- **When to Use**: When preparing release notes for App Store updates, GitHub releases, or changelogs.
- **Trigger**: `/release-notes` or *"generate release notes"*, *"write changelog"*, *"prepare release summary"*.
- **Intelligence**: Compares Git tags/commits, categorizes changes into New Features, Bug Fixes, Improvements, and Breaking Changes, and generates a dual-format report (User-Facing "What's New" + Technical Engineering Summary).
- **Guardrail**: Zero hallucinations; every bullet point is cited from verified Git commits.

#### 18. Security Audit (`/security-audit`)
- **When to Use**: For security vulnerability assessments, compliance reviews, or pre-deployment audits.
- **Trigger**: `/security-audit` or *"security audit"*, *"audit vulnerabilities"*, *"check security flaws"*.
- **Intelligence**: Evaluates code against OWASP Top 10: hardcoded secrets, authentication/session management, authorization (IDOR), SQL/command injection, XSS, CSRF, insecure local token storage, and CORS/CSP headers.
- **Guardrail**: Redacts all secret values in reports. Never makes automatic security modifications without approval.

---

## Shared Foundation: Global Engineering Standards

All 18 workflows inherit and adhere to the shared principles defined in:
[`~/.gemini/config/plugins/global-workflows/references/global-engineering-standards.md`](file:///Users/mahmoudhamdyae/.gemini/config/plugins/global-workflows/references/global-engineering-standards.md)

1. **Project Awareness**: Always detect workspace root, inspect manifests, and discover project-specific rules before acting.
2. **Engineering Excellence**: Follow official stable conventions, maintain separation of concerns, and avoid premature abstractions.
3. **Safety & Security**: Zero secret leakage, zero unprompted destructive commands (`rm -rf`, `reset --hard`, force-push), and 100% verification before claiming success.
4. **Structured Lifecycle**: Context ➔ Inspect ➔ Analyze ➔ Plan ➔ Execute ➔ Verify ➔ Report.
