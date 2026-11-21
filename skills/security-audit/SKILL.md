---
name: security-audit
description: >-
  Perform a comprehensive, technology-adapted security audit and vulnerability assessment across Flutter,
  Next.js, React, Node.js, and Laravel projects. Audits authentication, authorization, OWASP Top 10 risks
  (SQL injection, XSS, CSRF), secret leaks, insecure data storage, file upload security, and CORS/CSP policies.
  Never leaks secret values. Use when user invokes /security-audit or asks for "security audit",
  "audit vulnerabilities", "penetration test review", or "check security flaws".
---

# Security Audit Workflow

This workflow executes an in-depth security and vulnerability assessment adapted to the project's specific technology stack and architecture. It evaluates code against the **OWASP Top 10** (Web & Mobile), checks for hardcoded credentials, and detects data exposure hazards.

> [!IMPORTANT]
> **Responsible Disclosure & Privacy Guardrail**: Never print, copy, or expose real secret keys, private keys, passwords, or production tokens in the generated report. If a hardcoded secret is discovered, report only its file location and a redacted identifier (e.g. `AKIAIOSFODNN7EXAMPLE` ➔ `AKIA...MPLE`). Do NOT apply automatic security patches without explicit user consent.

---

## 10 Core Security Audit Vectors

1. **Secret & Credential Management**:
   - Inspect source files, Git history, and build scripts for hardcoded API keys, private keys (`.pem`, `.key`, `id_rsa`), AWS tokens, database credentials, or exposed `.env` files.
2. **Authentication & Session Integrity**:
   - Password hashing algorithms (Argon2id, bcrypt vs insecure MD5/SHA1), brute-force protection, JWT signature verification (checking for `alg: none` vulnerabilities), token expiration, and secure logout.
3. **Authorization & Access Control**:
   - Insecure Direct Object References (IDOR), missing role-based access checks (RBAC) on sensitive endpoints, and privilege escalation vulnerabilities.
4. **Injection Vulnerabilities (SQL / NoSQL / Command)**:
   - Raw SQL string concatenations instead of parameterized/prepared statements (e.g. `DB::raw("SELECT * WHERE id = $id")`).
   - Shell command execution (`exec`, `spawn`, `Process.run`) with un-sanitized user inputs.
5. **Cross-Site Scripting (XSS)**:
   - Dangerous HTML injections: `dangerouslySetInnerHTML` in React, `v-html` in Vue, `{!! $raw !!}` in Blade, or unescaped webview content.
6. **Cross-Site Request Forgery (CSRF)**:
   - Missing CSRF middleware on state-changing POST/PUT/DELETE web endpoints; proper usage of `SameSite` cookie flags.
7. **Insecure Data Storage & Encryption**:
   - Mobile: Plaintext tokens in `SharedPreferences` or `NSUserDefaults` instead of `FlutterSecureStorage` / Android Keystore / iOS Keychain.
   - Backend: Unencrypted sensitive personal data (PII) at rest.
8. **File Upload & Parsing Security**:
   - Unrestricted file upload extensions, missing MIME-type validation, path traversal attacks (`../../uploads/evil.php`), and denial of service via oversized files.
9. **CORS, Headers & Network Security**:
   - Overly permissive CORS (`Access-Control-Allow-Origin: *` with credentials enabled).
   - Missing security headers: Content-Security-Policy (CSP), Strict-Transport-Security (HSTS), X-Content-Type-Options: nosniff.
10. **Dependency Vulnerabilities (SCA)**:
    - Scanning manifests for known CVEs using ecosystem audit tools (`npm audit`, `composer audit`).

---

## Audit Execution Process

### Step 1: Automated Secret & Git State Scan
Run the bundled security inspector:
```bash
python3 ~/.gemini/config/plugins/global-workflows/scripts/git_inspector.py --json
```

### Step 2: Stack-Specific Static Security Scans
Inspect manifests and source code using stack-specific security checks:
- **Flutter**: Search for plaintext token storage, non-HTTPS network calls, and disabled SSL certificate validation (`badCertificateCallback: (cert, host, port) => true`).
- **Next.js / React**: Search for exposed `NEXT_PUBLIC_` prefixes containing secret API keys, `dangerouslySetInnerHTML`, and open redirect vulnerabilities.
- **Laravel**: Verify CSRF middleware in `bootstrap/app.php` / `Kernel.php`, inspect `DB::raw` queries, and check authentication guards in routes.
- **Node.js**: Inspect `eval()`, `child_process.exec()`, and rate limiting middlewares.

### Step 3: Vulnerability Classification & Triage
Classify every confirmed vulnerability using CVSS-aligned severity:
- **🔴 CRITICAL (CVSS 9.0–10.0)**: Remote code execution, hardcoded live production credentials, unauthenticated database access, or SQL injection.
- **🟠 HIGH (CVSS 7.0–8.9)**: Broken authorization (IDOR), persistent XSS, missing authentication on sensitive endpoints.
- **🟡 MEDIUM (CVSS 4.0–6.9)**: Missing CSRF tokens, unencrypted local tokens, overly permissive CORS, missing rate limiting.
- **🔵 LOW / INFO (CVSS 0.1–3.9)**: Missing security headers, verbose error messages in production.

---

## Security Audit Report Format

```markdown
# 🛡️ Security Vulnerability Assessment

**Target**: `<Application Root>`  
**Primary Stack**: `<Flutter / Next.js / Laravel / Node.js>`  
**Security Posture**: 🟢 Low Risk | 🟡 Moderate Risk | 🔴 Critical Vulnerabilities Detected

---

### Vulnerability Matrix
| Severity | Count | Primary Attack Vector |
| :--- | :--- | :--- |
| 🔴 **Critical** | `X` | Secret Exposure / SQL Injection |
| 🟠 **High** | `Y` | Broken Access Control / Insecure Storage |
| 🟡 **Medium** | `Z` | CSRF / Permissive CORS |
| 🔵 **Low / Info** | `W` | Missing Security Headers |

---

### Detailed Vulnerability Findings

#### 🔴 Critical Findings
- **Vulnerability**: `<Title, e.g. Hardcoded Secret Key in Source>`
  - **Location**: `[auth_service.dart](file:///path/to/file#L14)`
  - **CVSS Score**: `9.1 (Critical)`
  - **Evidence**: `const apiKey = "AIzaSy..."` *(Redacted for safety)*
  - **Potential Impact**: Full unauthorized access to external cloud service with unlimited quota exhaustion.
  - **Remediation**:
    ```language
    // Move to environment variable loaded at runtime
    ```

#### 🟠 High Severity Findings
- **Vulnerability**: `<Title, e.g. Insecure Local Token Storage>`
  - **Location**: `[storage.ts](file:///path/to/file#L32)`
  - **Potential Impact**: Tokens extractable from device backup or XSS.
  - **Remediation**: Use secure storage API / http-only cookies.

#### 🟡 Medium Severity Findings
- **Vulnerability**: `<Title>`
  - **Location**: `[file](file:///path#L10)`
  - **Remediation**: ...

---

### Remediation Roadmap & Next Steps
1. **Immediate Emergency Patch**: Revoke and rotate exposed credentials.
2. **Sprint Fixes**: Parameterize raw SQL queries and secure token storage.
3. **Hardening**: Configure security headers and rate limiting.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
