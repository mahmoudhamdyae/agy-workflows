---
name: design-system
description: >-
  Inspect, audit, maintain, and expand an existing UI design system and component library across Flutter,
  React, Next.js, and web apps. Catalogs design tokens (colors, typography, spacing, radii, shadows), detects
  hardcoded visual values and duplicate components, and establishes variant consistency. Use when user invokes
  /design-system or asks to "audit design system", "catalog tokens", "standardize components", or "design system review".
---

# Design System Workflow

This workflow systematically analyzes, catalogs, and refines an existing design system and UI component library. It ensures design token fidelity, eliminates duplicate UI components, and establishes consistent variant APIs without reinventing the project's brand identity.

> [!IMPORTANT]
> **Preserve Established Identity**: This workflow structures and consolidates the **existing** design system. It must **NOT** introduce an unrequested new brand style guide, alien color palette, or third-party UI framework without explicit user direction.

---

## 4-Pillar Design System Inspection

### Pillar 1: Design Tokens
Catalog the fundamental design variables:
- **Color Tokens**:
  - Primary, Secondary, Tertiary, Neutral/Surface, Background, Error, Success, Warning.
  - Interactive states (hover, active, focused, disabled).
  - Light vs Dark mode semantic mapping.
- **Typography Scale**:
  - Font families, sizes, line heights, font weights, and letter spacing across Headline, Title, Body, and Caption tokens.
- **Spacing & Layout Scale**:
  - 4pt / 8pt spacing scale (`none: 0`, `xs: 4`, `sm: 8`, `md: 16`, `lg: 24`, `xl: 32`, `2xl: 48`).
  - Standard container max-widths and responsive breakpoints (sm, md, lg, xl).
- **Shape & Elevation Tokens**:
  - Border radii (`none: 0`, `sm: 4px`, `md: 8px`, `lg: 12px`, `full: 9999px`).
  - Box shadows / elevation levels (elevation 1, 2, 3).

---

### Pillar 2: Core Component Library
Evaluate reusable component availability and API structure:
1. **Buttons & Actions**: Primary, Secondary, Outlined, Ghost/Text, Destructive, Icon-only buttons with consistent loading and disabled states.
2. **Form Controls & Inputs**: Text fields, textareas, selects/dropdowns, checkboxes, radio buttons, switches, sliders, error text, helper hints.
3. **Feedback & Status**: Snackbars/toasts, banners, dialogs, progress bars, skeleton loaders, badges/chips.
4. **Surfaces & Cards**: Elevated cards, flat borders, list tiles, bottom sheets, drawers, navigation bars.

---

### Pillar 3: Anti-Pattern & Drift Detection
Scan the codebase for design system drift:
- **Hardcoded Hex / RGB / Color Literals**: Searching for raw color values outside token files.
- **Arbitrary Pixel Dimensions**: Non-standard margins, paddings, or font sizes (e.g. `11px`, `17px`, `23px`).
- **Duplicate Components**: Detecting multiple custom implementations of the same primitive (e.g. three different custom button widgets instead of one unified `AppButton`).
- **Inconsistent Variant APIs**: Components where properties are named inconsistently (e.g. `variant="danger"` in one place vs `isDestructive={true}` in another).

---

### Pillar 4: Documentation & Developer Ergonomics
- Inspect Code Connect or Storybook configurations if present.
- Verify clear exports (e.g. barrel files `components/index.ts` or `lib/core/components/`).
- Verify prop types and documentation comments for all component variants.

---

## Output Report & Catalog Format

```markdown
# 🏛️ Design System Catalog & Audit Report

**Architecture**: `<Tailwind / Flutter ThemeData / CSS Variables / Component Library>`  
**Token Location**: `[File Link](file:///path/to/theme/tokens)`  
**Component Directory**: `[Folder Link](file:///path/to/components)`

---

### 1. Token Foundations Summary
- **Color Palette**: `<X semantic tokens defined, Light & Dark themes supported>`
- **Typography**: `<Type scale defined with Y levels>`
- **Spacing Scale**: `<Strict 8pt grid / Arbitrary values detected>`
- **Radii & Shadows**: `<Standardized across Z variants>`

---

### 2. Component Inventory
| Component | Variants Supported | States Handled | Consistency Rating |
| :--- | :--- | :--- | :--- |
| `Button` | Primary, Secondary, Outlined | Normal, Hover, Disabled, Loading | 🟢 Unified |
| `TextField` | Standard, Outlined | Focus, Error, Disabled | 🟡 Missing clear error state |
| `Card` | Flat, Elevated | Static | 🔴 Duplicate implementations found |

---

### 3. Design System Drift & Code Smells
- **Hardcoded Colors**: Found `<N>` instances of raw hex/color codes outside token files.
  - Example: `[screen.tsx](file:///path#L40)` uses `#2563EB` instead of `theme.colors.primary`.
- **Component Duplication**:
  - Found `CustomSubmitButton.dart` and `PrimaryButton.dart` serving identical roles.
- **Variant Discrepancies**:
  - Inconsistent border radius: Inputs use `12px` while buttons use `4px`.

---

### 4. Consolidation & Refactoring Plan
1. **Unify Duplicates**: Deprecate `<ComponentA>` in favor of `<ComponentB>`.
2. **Replace Hardcoded Values**: Migrate discovered raw literals to design tokens.
3. **Component API Standardization**: Ensure consistent `size`, `variant`, `disabled`, and `loading` props across all action elements.
```

---

## Shared References
- [Global Engineering Standards](../../references/global-engineering-standards.md)
