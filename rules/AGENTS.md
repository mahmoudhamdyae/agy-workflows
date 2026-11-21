# Global Engineering Standards for Antigravity

All agent interactions across Flutter, Frontend, Backend, API Integration, Testing, and DevOps must adhere to these active guidelines:

## 1. Project Awareness & Context Discovery
- Before modifying or generating code, inspect the project root, package manifests (`pubspec.yaml`, `package.json`, `composer.json`, etc.), and existing architecture.
- Always check for project instructions (`AGENTS.md`, `README.md`, `DESIGN.md`) and respect existing conventions.
- Never impose alien frameworks or architectural paradigms without explicit user approval.

## 2. Engineering Quality
- Write production-ready, clean, maintainable, and type-safe code using modern stable standards.
- Avoid unnecessary abstractions, boilerplate, or unneeded third-party dependencies.
- Maintain clear separation of concerns (UI, Business Logic, Data/Network).
- Never modify unrelated code or silently alter public APIs.

## 3. Safety & Secret Protection
- Never stage, commit, or print credentials, private keys (`.pem`, `.key`, `id_rsa`), tokens, API secrets, or `.env` files.
- Never execute destructive commands (`git reset --hard`, `git clean -fd`, `rm -rf`, force-push) automatically.
- Always verify execution results with compilers, linters, tests, or status checks before claiming completion.
