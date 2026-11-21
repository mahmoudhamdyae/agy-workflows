---
name: pre-release-check
description: >-
  Conduct a rigorous pre-release quality and readiness audit before deploying to production, App Store,
  or Google Play. Verifies clean builds, 100% passing tests, zero linter errors, no exposed secrets, valid
  app version/build numbers, permissions configuration, production API endpoints, and release optimizations.
  Never deploys automatically. Use when user invokes /pre-release-check or asks for "pre-release check",
  "readiness check", "verify release build", or "production readiness audit".
---

# Pre-Release Check Workflow

This workflow executes an exhaustive, multi-point pre-flight checklist to ensure an application is 100% stable, secure, and production-ready prior to customer release or app store submission.

> [!IMPORTANT]
> **Zero Automatic Deployment**: This workflow verifies readiness and generates a deployment clearance report. It must **NEVER** automatically push tags, trigger CI/CD deployment pipelines, upload builds to Google Play / App Store / TestFlight, or deploy to production servers without explicit user confirmation.

---

## 10-Point Pre-Flight Verification Checklist

```text
[1. Git Cleanliness] ➔ [2. Secret Scan] ➔ [3. Static Analysis] ➔ [4. Automated Tests]
    ➔ [5. Release Build Check] ➔ [6. Version & Build Numbers] ➔ [7. Config & API Target]
    ➔ [8. Native Permissions] ➔ [9. Asset Optimization] ➔ [10. Release Verdict]
```

### 1. Git Repository State
- Verify working tree is clean or has only intended changes.
- Check current branch (ensure release is not cut from an unmerged experimental branch).

### 2. Zero Secrets in Build Artifacts
- Run the sensitive files scanner to ensure no `.env` files, debug keystores, or private credentials are included in the bundle:
  ```bash
  python3 ~/.gemini/config/plugins/global-workflows/scripts/git_inspector.py --json
  ```

### 3. Static Analysis & Linting Cleanliness
- Enforce zero errors and zero warnings:
  - Flutter: `flutter analyze`
  - React / Next.js: `npm run lint && tsc --noEmit`
  - Laravel: `vendor/bin/phpstan analyse` or `php artisan pint --test`

### 4. Automated Test Suite Execution
- Run unit, component, and feature test suites. Ensure 100% pass rate with zero skipped critical tests.

### 5. Release Build Compilation
- Verify that a release / production build actually compiles without tree-shaking or minification crashes:
  - Flutter: `flutter build bundle --release` (or dry-run apk/ipa)
  - Next.js: `npm run build`
  - Laravel: `php artisan config:cache && php artisan route:cache`

### 6. Versioning & Build Numbers
- Verify application version and build number match release targets:
  - **Flutter**: `version: 1.2.0+42` in `pubspec.yaml`
  - **Next.js / Node.js**: `"version": "1.2.0"` in `package.json`
  - **Android**: `versionCode` and `versionName` in `app/build.gradle`
  - **iOS**: `CFBundleShortVersionString` and `CFBundleVersion` in `Info.plist`

### 7. Environment & Production API Endpoints
- Confirm production API URLs are configured (no `localhost:3000` or `10.0.2.2` hardcoded in release builds).
- Check that debug flags are disabled (e.g. `debugShowCheckedModeBanner: false`, `APP_DEBUG=false`).

### 8. App Permissions & Privacy Declarations
- Android: Review `AndroidManifest.xml` for unnecessary high-risk permissions (`ACCESS_BACKGROUND_LOCATION`, `READ_CONTACTS`).
- iOS: Review `Info.plist` for required usage descriptions (`NSCameraUsageDescription`, `NSLocationWhenInUseUsageDescription`).
- Web: Review Content Security Policy (CSP) and CORS headers.

### 9. Logging & Error Reporting
- Verify that verbose console debug logging (`console.log`, `print()`) is stripped or minimized in production.
- Confirm Crashlytics / Sentry / Bugsnag SDKs are initialized with production keys.

### 10. Assets & Bundle Optimization
- Verify image assets are compressed and unused assets are not inflating bundle size.

---

## Pre-Release Clearance Report Format

```markdown
# 🚀 Pre-Release Readiness Assessment

**Target Release**: `<App Name> v<X.Y.Z> (Build <N>)`  
**Platform**: `<iOS / Android / Web / Backend>`  
**Final Verdict**: 🟢 **CLEARED FOR RELEASE** | 🔴 **RELEASE BLOCKED**

---

### Verification Summary
| Checkpoint | Status | Details / Findings |
| :--- | :--- | :--- |
| **1. Git Cleanliness** | 🟢 Passed | Clean working tree on `release/vX.Y` |
| **2. Secret Screening** | 🟢 Passed | Zero private keys or `.env` in repository |
| **3. Static Analysis** | 🟢 Passed | Zero errors, zero linter warnings |
| **4. Automated Tests** | 🟢 Passed | 84/84 tests passing (100%) |
| **5. Production Build** | 🟢 Passed | Build compiled with zero errors |
| **6. Versioning** | 🟢 Passed | `v1.2.0` (Build `45`) correctly incremented |
| **7. API Target** | 🟢 Passed | Pointing to `https://api.production.com` |
| **8. Permissions** | 🟢 Passed | Usage descriptions present in `Info.plist` |
| **9. Error Reporting** | 🟢 Passed | Sentry initialized for production |
| **10. Assets** | 🟢 Passed | Assets optimized, total bundle < 25MB |

---

### Blockers & Warnings (If Any)
*(Listed only if verdict is BLOCKED)*
- 🔴 **Blocker 1**: `<Description and exact fix required>`

---

### Release Sign-Off
- **Readiness Confidence**: 100%
- **Next Step**: Awaiting user confirmation before publishing or tagging release.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
