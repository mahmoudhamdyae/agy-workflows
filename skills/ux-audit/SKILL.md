---
name: ux-audit
description: >-
  Evaluate mobile, web, and desktop applications from the end-user's perspective. Audits user flows,
  information architecture, cognitive load, error prevention, form usability, empty/loading states,
  and accessibility (WCAG). Delivers structured, severity-rated UX recommendations. Use when user invokes
  /ux-audit or asks for "ux audit", "evaluate usability", "review user experience", or "audit user flows".
---

# UX Audit Workflow

This workflow evaluates digital products through the lens of human-centered design, cognitive ergonomics, and established usability heuristics (Nielsen Norman Group, WCAG 2.1).

> [!IMPORTANT]
> **Empirical Honesty Mandate**: Never invent user research data, fake survey statistics, or claim that unverified assumptions represent validated usability testing. Clearly distinguish between established UX heuristics and subjective product suggestions.

---

## 10 Core Usability Dimensions

1. **User Flows & Path to Value**:
   - Friction, dead ends, unnecessary intermediate steps, or circular navigation loops in primary user journeys (e.g. signup, checkout, search, onboarding).
2. **Information Architecture & Navigation**:
   - Clarity of menus, breadcrumbs, back-button behavior, deep-linking consistency, and mental model alignment.
3. **Cognitive Load & Progressive Disclosure**:
   - Visual clutter, decision paralysis, information density, and presenting complex inputs incrementally instead of all at once.
4. **Form Usability & Error Prevention**:
   - Inline real-time validation, sensible defaults, password reveal toggles, proper input masks (e.g. phone/date), and non-destructive resets.
5. **System Feedback & State Transparency**:
   - Visual confirmations for user actions (toasts, progress bars, optimistic UI updates), skeleton loaders, and non-blocking background tasks.
6. **Error States & Recovery**:
   - Plain-language error messages (never exposing raw error codes or cryptic stack traces), clear remediation steps, and "Retry" actions.
7. **Empty States & Onboarding**:
   - Helpful, welcoming empty states with clear primary calls-to-action (CTAs) guiding the user toward first-time completion.
8. **Accessibility (A11y)**:
   - Screen-reader labels (`Semantics` in Flutter, `aria-label` in web), minimum touch target sizes (≥ 48x48 dp/px), and keyboard navigability.
9. **Copywriting & Content Clarity**:
   - Concise, unambiguous microcopy, clear CTA button labels ("Save Changes" vs generic "Submit"), and consistent terminology.
10. **Interaction Consistency**:
    - Predictable gesture behavior (swipes, pull-to-refresh, taps), standard icon semantics, and consistent placement of primary actions.

---

## Evaluation Process

### Step 1: Discover User Journeys
1. Identify key views and screens from routes, navigation trees, or storyboard files:
   - Flutter: `routes.dart`, `GoRouter` declarations, screens in `lib/presentation/` or `lib/features/`.
   - Web: `app/` routes, page components, navigation components.
2. Trace the core workflows: Onboarding ➔ Authentication ➔ Main Dashboard ➔ Detail View ➔ Creation/Editing Flow ➔ Settings.

### Step 2: Heuristic Analysis
- Inspect code for UX anti-patterns:
  - Missing disabled states during async submissions (allowing double-tap race conditions).
  - Destructive actions (delete, reset) without confirmation dialogs.
  - Form inputs lacking auto-focus, appropriate virtual keyboard types (`keyboardType: TextInputType.emailAddress`), or autocomplete attributes.

### Step 3: Prioritize Findings
Categorize findings by user impact:
- **🔴 Blocker / High**: Prevents user from completing a task, causes accidental data loss, or violates critical accessibility.
- **🟡 Moderate / Medium**: Causes user confusion, hesitation, or unnecessary effort.
- **🔵 Minor / Low**: Minor friction or cosmetic microcopy enhancement.

---

## Output Report Format

```markdown
# 🧭 User Experience (UX) Audit Report

**Application**: `<App / Module Name>`  
**Scope**: `<Screens or Flows Evaluated>`  
**Usability Score**: 🟢 High Usability | 🟡 Moderate Friction | 🔴 High Friction

---

### Key Findings Summary
| Severity | Flow / Screen | Usability Heuristic | Primary User Impact |
| :--- | :--- | :--- | :--- |
| 🔴 High | `<Checkout / Auth>` | Error Prevention | Risk of duplicate payment on double tap |
| 🟡 Medium | `<Dashboard>` | System Feedback | User unsure if background sync succeeded |

---

### Detailed Usability Findings

#### 🔴 High Severity UX Issues
- **Screen / Component**: `[File Link](file:///path/to/screen)`
  - **Issue**: <Clear description of the usability flaw>
  - **Heuristic**: <e.g., Error Prevention / Visibility of System Status>
  - **User Impact**: <How it frustrates or blocks real users>
  - **Recommended UX Solution**:
    - <Concrete, actionable design or interaction fix>

#### 🟡 Medium Severity Friction Points
- **Screen / Component**: `[File Link](file:///path/to/screen)`
  - **Issue**: ...
  - **User Impact**: ...
  - **Recommended Solution**: ...

#### 🔵 Minor Polish & Usability Quick-Wins
- `<Quick win 1: Change button label from "Submit" to "Create Account">`
- `<Quick win 2: Add keyboard dismiss on tap-outside in mobile forms>`

---

### Recommended UX Roadmap
1. **Immediate**: Resolve blocking flows and error prevention gaps.
2. **Phase 2**: Enhance loading/empty states and feedback loops.
3. **Phase 3**: Polish accessibility labels and microcopy.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
