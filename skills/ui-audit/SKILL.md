---
name: ui-audit
description: >-
  Audit visual UI quality, aesthetics, and implementation across mobile and web interfaces.
  Evaluates visual hierarchy, typography scales, color palettes, spacing rhythm, alignment,
  contrast (WCAG AA), icon consistency, light/dark themes, and RTL/LTR layout behavior.
  Use when user invokes /ui-audit or asks for "ui audit", "evaluate visual design", "check styling consistency",
  or "audit interface quality".
---

# UI Audit Workflow

This workflow performs a comprehensive visual and design-fidelity audit of frontend user interfaces in Flutter, React, Next.js, and web frameworks. It evaluates aesthetics, spacing consistency, contrast compliance, and theme fidelity.

> [!IMPORTANT]
> **Preserve Design Identity**: This workflow audits and refines the existing visual direction of the project. It must **NOT** unilaterally redesign the brand identity, alter foundational colors, or replace the design system without explicit user consent.

---

## 10 Visual UI Dimensions

1. **Visual Hierarchy & Scanning**:
   - Clear distinction between primary, secondary, and tertiary elements.
   - Distinct focal points so users immediately understand where to look.
2. **Typography Scale & Rhythm**:
   - Adherence to a consistent type scale (e.g. Display, Headline, Title, Body, Label).
   - Readable line heights, letter-spacing, and font-weight hierarchy.
3. **Color Consistency & Token Usage**:
   - Proper use of semantic color tokens (`primary`, `surface`, `error`, `onSurface`) instead of hardcoded hex values (`#3A82F6` or `Color(0xFF2196F3)`).
4. **Spacing & 4pt/8pt Grid System**:
   - Strict spacing rhythm (4px, 8px, 12px, 16px, 24px, 32px, 48px).
   - Consistent margin and padding between adjacent cards, lists, and form fields.
5. **Alignment & Visual Balance**:
   - Horizontal and vertical alignment along common visual axes.
   - Symmetrical padding within cards, buttons, and containers.
6. **Component Uniformity & Variants**:
   - Buttons, text fields, cards, and chips sharing identical border radii, elevation/shadows, and interactive states (hover, pressed, disabled, focused).
7. **Accessibility & Color Contrast**:
   - WCAG 2.1 AA compliance: Minimum 4.5:1 contrast ratio for normal text and 3:1 for large text and UI controls against their backgrounds.
8. **Iconography & Asset Cohesion**:
   - Uniform icon stroke weights, sizing (standardized e.g. 20px, 24px), and style (all outlined or all filled, avoiding mixed icon libraries).
9. **Light & Dark Mode Parity**:
   - Ensuring dark theme retains appropriate contrast, surfaces use proper tonal elevations instead of pure `#000000`, and text remains readable.
10. **Internationalization & Layout Direction (RTL / LTR)**:
    - Proper mirroring of icons (back arrows, disclosure chevrons), text alignment, and padding start/end in right-to-left locales (Arabic, Hebrew).

---

## Audit Execution Process

### Step 1: Discover Design Foundations
1. Locate global theme definitions and style constants:
   - **Flutter**: `ThemeData`, `ColorScheme`, custom `ThemeExtension`, `AppColors`, `AppTypography` in `lib/core/theme/`.
   - **React / Next.js**: `tailwind.config.js`, `globals.css`, CSS variables, styled theme tokens.
2. Identify whether design tokens are centrally managed or scattered as hardcoded values.

### Step 2: Screen & Component Inspection
- Inspect individual screen implementations:
  - Check for hardcoded dimensions (`width: 350`, `padding: EdgeInsets.all(13)`).
  - Check for missing theme bindings (`color: Colors.black` instead of `theme.colorScheme.onSurface`).
  - Check button sizes and elevation consistency.

### Step 3: Visual Verification (When Available)
- Utilize available browser testing tools (`browser-use`), Android screenshots, or Compose previews to inspect rendered visuals.
- Distinguish between proven visual glitches (e.g. text wrapping, clipping) and theoretical code observations.

---

## Output Report Format

```markdown
# 🎨 Visual UI Audit Report

**Application**: `<App / View / Component>`  
**Design Foundation**: `<Tailwind / Material 3 / Custom Design System>`  
**Visual Cohesion Rating**: 🟢 High Polish | 🟡 Minor Inconsistencies | 🔴 Needs Visual Alignment

---

### Key Observations & Metrics
- **Hardcoded Color Invocations**: `<Count found>`
- **Non-Grid Spacing Values**: `<Count found>`
- **Contrast / Readability Warnings**: `<Count found>`
- **Theme Support**: `<Light / Dark parity status>`

---

### Detailed Findings

#### 🔴 High Priority Visual Inconsistencies
- **Component / Screen**: `[File Link](file:///path/to/screen#L55)`
  - **Issue**: <e.g., Low contrast text on dark mode or broken alignment>
  - **Visual Dimension**: Contrast / Hierarchy / Alignment
  - **Current State**: <Hardcoded light grey on white background (2.1:1 ratio)>
  - **Recommended Fix**:
    ```language
    // Exact theme token replacement
    ```

#### 🟡 Medium Priority Polish Items
- **Component / Screen**: `[File Link](file:///path/to/component#L120)`
  - **Issue**: <Inconsistent border-radius or non-standard 13px padding>
  - **Recommended Fix**: <Align with standard 8pt grid token (e.g. 16px)>

#### 🔵 Minor Polish & Icon Cohesion
- `<Note 1: Mixed icon styles in navigation bar>`
- `<Note 2: Elevation shadow clipping on card edges>`

---

### Implementation Recommendations
1. Replace all hardcoded color literals with semantic theme tokens.
2. Standardize button border radii across all modal dialogues.
3. Fix WCAG contrast failures in secondary text captions.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
