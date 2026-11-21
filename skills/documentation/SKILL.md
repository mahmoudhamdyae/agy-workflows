---
name: documentation
description: >-
  Create, update, and maintain accurate technical documentation based strictly on real project code.
  Generates READMEs, architecture guides, API references, environment variable guides (.env.example docs),
  installation setups, and Architectural Decision Records (ADRs). Never invents fake endpoints or configs.
  Use when user invokes /documentation or asks to "write docs", "update readme", "document api", or "create architecture doc".
---

# Documentation Workflow

This workflow produces clear, comprehensive, and accurate documentation grounded entirely in the actual implementation of the project.

> [!IMPORTANT]
> **Anti-Hallucination Mandate**: Never invent endpoints, configuration variables, CLI flags, database tables, or features that do not exist in the codebase. All documentation must cite concrete code locations and actual commands.

---

## Supported Documentation Types

1. **Project README (`README.md`)**:
   - Project description, tech stack, prerequisites, step-by-step local installation, running the app, testing, and project layout.
2. **Architecture Documentation (`docs/ARCHITECTURE.md`)**:
   - System design, directory structure, data flow, state management lifecycle, and module boundaries.
3. **API & Contract Reference (`docs/API.md`)**:
   - Real routes, endpoints, HTTP verbs, required headers, query parameters, payload schemas, and response formats extracted directly from route handlers and controllers.
4. **Environment & Configuration Guide (`docs/ENVIRONMENT.md` or updated `.env.example`)**:
   - Documents every required environment variable, expected type, default value, and where to obtain credentials (without ever exposing real secrets!).
5. **Architectural Decision Records (`docs/adr/XXXX-title.md`)**:
   - Documents the context, decision, consequences, and alternatives considered for significant architectural choices.
6. **Deployment & CI/CD Guide (`docs/DEPLOYMENT.md`)**:
   - Build steps, Docker commands, release commands, and infrastructure requirements.

---

## Execution Process

### Step 1: Discover Ground Truth
1. Inspect project manifests (`pubspec.yaml`, `package.json`, `composer.json`, etc.) using:
   ```bash
   python3 ~/.gemini/config/plugins/global-workflows/scripts/project_detector.py --json
   ```
2. Scan existing documentation files to preserve historical context and valuable manual notes.
3. Inspect entry points, route definitions, build scripts, and test suites.

### Step 2: Code-Level Fact Extraction
- For **API docs**: Read router files (`routes/api.php`, `app/api/...`, `lib/core/network/...`).
- For **Environment docs**: Grep codebase for `process.env.`, `env()`, `Platform.environment`, `dotenv`, or configuration classes.
- For **Run/Build commands**: Extract exact script names from `package.json` scripts, `artisan` commands, `pubspec.yaml`, or `Makefile`.

### Step 3: Synthesis & Authoring
- Preserve existing valid sections in target documents.
- Use GitHub Flavored Markdown with syntax highlighting, clear tables, and callouts (`[!NOTE]`, `[!TIP]`, `[!WARNING]`).
- Include runnable code snippets that are validated against the actual codebase.

### Step 4: Verification
- Verify that every listed command can execute in the environment.
- Verify all relative file links (`[file](file:///...)`).
- Verify that no secret keys or passwords were unintentionally included.

---

## Standard README Template Example

```markdown
# <Project Name>

<Concise 1-2 sentence description of what the application does.>

---

## 🛠️ Tech Stack & Prerequisites
- **Framework**: <Framework & Version>
- **Language**: <Language & Version>
- **Required Tools**: <Node.js version, Flutter SDK, PHP version, Docker, etc.>

---

## 🚀 Getting Started

### 1. Clone & Setup
```bash
git clone <repo-url>
cd <repo-folder>
```

### 2. Install Dependencies
```bash
<actual install command: npm install / flutter pub get / composer install>
```

### 3. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your local credentials
```

### 4. Run the Application
```bash
<actual dev command: npm run dev / flutter run / php artisan serve>
```

---

## 🧪 Testing & Code Quality
```bash
<test command>
<lint command>
```

---

## 📁 Project Structure
```text
<clean ASCII tree of key folders and their purposes>
```
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
