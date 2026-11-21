---
name: responsive-audit
description: >-
  Audit responsive interface behavior, multi-screen scaling, and cross-platform layout resilience across
  mobile, tablet, and desktop viewports. Detects UI overflow (RenderFlex overflow), clipping, broken wrapping,
  inadequate touch targets (<48dp), mobile vs desktop navigation adaptation, and RTL/LTR layout behavior.
  Use when user invokes /responsive-audit or asks to "audit responsiveness", "check mobile layout",
  "fix layout overflow", or "test screen sizes".
---

# Responsive Audit Workflow

This workflow evaluates how frontend layouts behave across diverse screen dimensions, orientations, display densities, and platforms (iOS, Android, Web, Desktop). It identifies layout breaks, overflow errors, touch target hazards, and poor responsive adaptation.

---

## Target Viewport Matrix

Evaluate layouts across 4 standard form factors:

| Form Factor | Viewport Range | Primary Input Mode | Key Layout Requirements |
| :--- | :--- | :--- | :--- |
| **Mobile Portrait** | 320px – 430px | Touch | Single column, sticky bottom bars, hamburger / tab navigation, touch targets ≥ 48px |
| **Mobile Landscape / Small Tablet** | 600px – 840px | Touch | 2-column grids, split views, avoiding vertical modal height clipping |
| **Tablet / Foldable** | 840px – 1024px | Touch & Keyboard | Navigation rail / persistent drawer, multi-pane layouts |
| **Desktop / Wide Screen** | 1200px – 1920px+ | Mouse & Keyboard | Multi-column, max-width content bounding (avoiding runaway stretch), hover states |

---

## 8 Critical Responsive Checks

1. **Overflow & Clipping**:
   - Flutter: `RenderFlex overflowed by X pixels` caused by unbounded `Column`/`Row` inside `SingleChildScrollView` or missing `Expanded`/`Flexible`.
   - Web: Horizontal scrollbars appearing unintentionally on mobile screens due to fixed width elements (`width: 600px`).
2. **Text Scaling & Wrapping**:
   - Long labels, localized strings, or enlarged user accessibility text sizes causing text clipping or overlapping adjacent UI.
   - Proper use of `overflow: TextOverflow.ellipsis` or flex wrapping.
3. **Adaptive Layout Strategy**:
   - Flutter: Proper usage of `LayoutBuilder`, `MediaQuery.sizeOf(context)`, or responsive packages (e.g. `responsive_builder`, `flutter_screenutil`).
   - Web: CSS container queries, Tailwind responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`), CSS Grid `auto-fit` / `minmax`.
4. **Touch Target Sizing**:
   - Ensuring interactive buttons, icons, and list items satisfy Apple HIG & Android Material minimum touch target guidelines (≥ 48x48 dp / px).
5. **Adaptive Navigation Patterns**:
   - Transitioning smoothly from bottom navigation bars (mobile) to navigation rails (tablet) and persistent sidebar drawers (desktop).
6. **Keyboard Occlusion & Safe Areas**:
   - Flutter: Ensuring `SafeArea` wraps screens and inputs scroll into view when the on-screen software keyboard opens (`resizeToAvoidBottomInset: true`).
   - Web: Dynamic viewport units (`100dvh` vs `100vh`) to prevent mobile browser URL bar clipping.
7. **Orientation Changes**:
   - Landscape usability on mobile phones (ensuring forms and dialogs remain scrollable and submit buttons do not get pushed off-screen).
8. **Right-to-Left (RTL) Adaptability**:
   - Using logical properties (`EdgeInsetsDirectional`, `margin-inline-start`, `start` vs `left`) so layouts mirror naturally in Arabic/Hebrew.

---

## Execution Process

### Step 1: Detect Stack & Responsive Architecture
1. Identify responsive primitives in use:
   - **Flutter**: Search for `LayoutBuilder`, `MediaQuery`, `OrientationBuilder`, `Wrap`, `Flexible`, `Expanded`.
   - **Web / React**: Search for `@media`, `min-width`, Tailwind responsive utility classes, container queries.

### Step 2: Code-Level Vulnerability Scan
- Scan for rigid layout smells:
  - Hardcoded fixed container widths (e.g. `width: 380`, `width: 500px`) without `maxWidth: 100%`.
  - Non-scrollable columns containing user input forms (destined to overflow when keyboard opens).
  - Absolute positioning without boundary constraints.

### Step 3: Screen & Viewport Testing
- If running in web context: Use browser automation (`browser-use`) with mobile viewport emulation (e.g. 375x812) to verify rendering.
- If Flutter project: Inspect widget tree constraints and layout builders.

---

## Output Report Format

```markdown
# 📱 Responsive & Cross-Platform Audit Report

**Application**: `<App / View / Screen>`  
**Primary Stack**: `<Flutter / Next.js / React>`  
**Responsiveness Rating**: 🟢 Highly Adaptive | 🟡 Minor Tablet/Mobile Gaps | 🔴 Critical Layout Breaks

---

### Viewport Matrix Summary
| Viewport | Status | Issues Detected |
| :--- | :--- | :--- |
| **Mobile (375px)** | 🔴 Broken | Unbounded horizontal row causing overflow |
| **Tablet (768px)** | 🟡 Warning | Modals clip vertically on landscape |
| **Desktop (1440px)** | 🟢 Passed | Content properly bounded in container |

---

### Detailed Findings

#### 🔴 Critical Layout Breaks
- **Component**: `[File Link](file:///path/to/widget#L88)`
  - **Issue**: RenderFlex overflow on small screens / mobile viewport.
  - **Root Cause**: Rigid `Row` with 3 fixed-width children without `Flexible`/`Expanded`.
  - **Recommended Fix**:
    ```language
    // Wrap children in Flexible or use a Wrap widget
    ```

#### 🟠 Touch Target & Ergonomics Warnings
- **Component**: `[File Link](file:///path/to/button#L140)`
  - **Issue**: Close icon has hit target of 24x24 px (recommended minimum: 48x48 px).
  - **Fix**: Increase padding or wrap with minimum hit-test area.

#### 🟡 Desktop / Tablet Adaptation Improvements
- **Screen**: `[File Link](file:///path/to/page#L22)`
  - **Observation**: Form inputs stretch full width (1400px) on desktop screens.
  - **Fix**: Wrap in constrained container (`maxWidth: 600px`).

---

### Actionable Remediation Checklist
- [ ] Replace fixed widths with flexible flex/grid layouts.
- [ ] Wrap form columns in `SingleChildScrollView` to prevent keyboard overflow.
- [ ] Ensure all buttons meet minimum 48px touch targets.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
