# Skepticamp NYC — Complete Design Specification
**Version 1.0 — March 2026**
*For direct developer implementation. No decisions left open.*

---

## Table of Contents

1. Brand Identity
2. Design System Components
3. Page-by-Page Layout Specifications
4. UX Interaction Patterns
5. Responsive Behavior
6. Dark Mode vs. Light Mode
7. The WOW Factor

---

# 1. Brand Identity

## 1.1 Project Name Treatment and Tagline

**Logotype:** "Skepticamp" — set in the display font (see Typography). The "S" is rendered at 1.25× the cap height and uses the primary accent color. "NYC" is set immediately below in a smaller weight, letter-spaced at 0.25em, in the secondary text color. No logomark/icon is used — the name *is* the mark.

**Tagline:** "Share the Apple of Knowledge" — used as a supporting line on the hero and in the browser `<title>`. Secondary tagline for meta/social: "A free, one-day unconference at the intersection of science and critical thinking."

**Capitalization convention:** Always "Skepticamp NYC" — never "SkeptiCamp" or "SKEPTICAMP". Consistent casing builds brand recognition.

---

## 1.2 Color Palette

All colors are specified for both modes. CSS custom properties are named as `--color-[role]`. The design uses a base of deep midnight blue in dark mode and scientific-paper off-white in light mode — neither pure black nor pure white — to reduce eye strain and add character.

### Dark Mode (applied when `<html class="dark">`)

| Token | Hex | Usage |
|---|---|---|
| `--bg-page` | `#0D0F1A` | Page background — deep midnight |
| `--bg-card` | `#13162A` | Card and panel background |
| `--bg-elevated` | `#1C2040` | Elevated surfaces, modals, dropdowns |
| `--bg-overlay` | `rgba(13, 15, 26, 0.80)` | Modal backdrop, nav overlay |
| `--accent-primary` | `#4FAAFF` | Primary interactive color — electric blue |
| `--accent-primary-hover` | `#71BBFF` | Primary hover state |
| `--accent-primary-active` | `#3A95F0` | Primary pressed/active state |
| `--accent-primary-subtle` | `rgba(79, 170, 255, 0.12)` | Ghost button fills, focus rings |
| `--accent-secondary` | `#C084FC` | Secondary accent — violet/cosmic |
| `--accent-secondary-hover` | `#D4A8FD` | Secondary hover |
| `--accent-secondary-subtle` | `rgba(192, 132, 252, 0.12)` | Secondary ghost fill |
| `--state-success` | `#34D399` | Success states, confirmations |
| `--state-success-subtle` | `rgba(52, 211, 153, 0.12)` | Success banners background |
| `--state-warning` | `#FBBF24` | Warning states |
| `--state-warning-subtle` | `rgba(251, 191, 36, 0.12)` | Warning banners background |
| `--state-error` | `#F87171` | Error states, destructive actions |
| `--state-error-subtle` | `rgba(248, 113, 113, 0.12)` | Error banners background |
| `--state-info` | `#60A5FA` | Info toasts and alerts |
| `--state-info-subtle` | `rgba(96, 165, 250, 0.12)` | Info banners background |
| `--text-primary` | `#E8ECF4` | Body text, headings — not pure white |
| `--text-secondary` | `#9BA8C0` | Supporting text, labels |
| `--text-muted` | `#5C6880` | Placeholders, disabled text, captions |
| `--text-inverse` | `#0D0F1A` | Text on light-colored surfaces (e.g., filled primary button) |
| `--text-accent` | `#4FAAFF` | Links, highlighted terms |
| `--border-default` | `rgba(255, 255, 255, 0.08)` | Card borders, dividers |
| `--border-subtle` | `rgba(255, 255, 255, 0.04)` | Very faint separators |
| `--border-strong` | `rgba(255, 255, 255, 0.18)` | Focused inputs, emphasis borders |
| `--border-accent` | `#4FAAFF` | Focus rings, active input borders |
| `--interactive-hover-bg` | `rgba(255, 255, 255, 0.05)` | Row/item hover background |
| `--interactive-focus-ring` | `#4FAAFF` | Keyboard focus outline color |
| `--interactive-disabled-bg` | `rgba(255, 255, 255, 0.06)` | Disabled control fill |
| `--interactive-disabled-text` | `#3E4A5F` | Disabled control text |

### Light Mode (applied when `<html class="light">` or no class, system default)

| Token | Hex | Usage |
|---|---|---|
| `--bg-page` | `#F5F4F0` | Page background — warm scientific-paper |
| `--bg-card` | `#FFFFFF` | Card and panel background |
| `--bg-elevated` | `#FFFFFF` | Elevated surfaces, modals — white with shadow |
| `--bg-overlay` | `rgba(245, 244, 240, 0.85)` | Modal backdrop |
| `--accent-primary` | `#1A6FD4` | Primary interactive — deep cerulean |
| `--accent-primary-hover` | `#1560BB` | Primary hover |
| `--accent-primary-active` | `#0F4E99` | Primary active/pressed |
| `--accent-primary-subtle` | `rgba(26, 111, 212, 0.10)` | Ghost fills, focus rings |
| `--accent-secondary` | `#7C3AED` | Secondary — deep violet |
| `--accent-secondary-hover` | `#6D28D9` | Secondary hover |
| `--accent-secondary-subtle` | `rgba(124, 58, 237, 0.10)` | Secondary ghost fill |
| `--state-success` | `#059669` | Success |
| `--state-success-subtle` | `rgba(5, 150, 105, 0.10)` | Success banners |
| `--state-warning` | `#D97706` | Warning |
| `--state-warning-subtle` | `rgba(217, 119, 6, 0.10)` | Warning banners |
| `--state-error` | `#DC2626` | Error |
| `--state-error-subtle` | `rgba(220, 38, 38, 0.10)` | Error banners |
| `--state-info` | `#2563EB` | Info |
| `--state-info-subtle` | `rgba(37, 99, 235, 0.10)` | Info banners |
| `--text-primary` | `#111827` | Body text, headings |
| `--text-secondary` | `#374151` | Supporting text |
| `--text-muted` | `#9CA3AF` | Placeholders, captions |
| `--text-inverse` | `#FFFFFF` | Text on filled primary buttons |
| `--text-accent` | `#1A6FD4` | Links |
| `--border-default` | `rgba(0, 0, 0, 0.10)` | Card borders, dividers |
| `--border-subtle` | `rgba(0, 0, 0, 0.05)` | Faint separators |
| `--border-strong` | `rgba(0, 0, 0, 0.25)` | Focused inputs |
| `--border-accent` | `#1A6FD4` | Focus rings |
| `--interactive-hover-bg` | `rgba(0, 0, 0, 0.04)` | Row hover |
| `--interactive-focus-ring` | `#1A6FD4` | Keyboard focus outline |
| `--interactive-disabled-bg` | `rgba(0, 0, 0, 0.05)` | Disabled fill |
| `--interactive-disabled-text` | `#C0C8D4` | Disabled text |

### Special Gradient Tokens (Dark Mode)
Used in the hero section and decorative elements.

| Token | Value |
|---|---|
| `--gradient-hero` | `linear-gradient(135deg, #0D0F1A 0%, #131840 50%, #1A0D2E 100%)` |
| `--gradient-accent` | `linear-gradient(135deg, #4FAAFF 0%, #C084FC 100%)` |
| `--gradient-card-edge` | `linear-gradient(180deg, rgba(79,170,255,0.08) 0%, transparent 100%)` |

### Special Gradient Tokens (Light Mode)
| Token | Value |
|---|---|
| `--gradient-hero` | `linear-gradient(135deg, #EEF2FF 0%, #F5F4F0 50%, #F0EBF8 100%)` |
| `--gradient-accent` | `linear-gradient(135deg, #1A6FD4 0%, #7C3AED 100%)` |
| `--gradient-card-edge` | `linear-gradient(180deg, rgba(26,111,212,0.06) 0%, transparent 100%)` |

---

## 1.3 Typography

### Font Families

**Display / Headings:** `"DM Serif Display"` — Google Fonts. Loaded at weights 400 only (italic variant unused). This serif conveys intellectual authority and warmth. Used for display, h1, h2.

**UI / Body / Labels:** `"Inter"` — Google Fonts. Loaded at weights 400, 500, 600. Clean, readable, scientific precision.

**Monospace:** `"JetBrains Mono"` — Google Fonts. Weight 400. Used for any technical strings, confirmation codes, event IDs.

**Fallback stacks:**
- Display: `"DM Serif Display", Georgia, "Times New Roman", serif`
- UI: `"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- Mono: `"JetBrains Mono", "Fira Code", "Cascadia Code", monospace`

### Type Scale

| Token | Font | Size | Weight | Line-height | Letter-spacing | Usage |
|---|---|---|---|---|---|---|
| `--text-display` | DM Serif Display | 4.5rem (72px) | 400 | 1.05 | -0.02em | Hero headline only |
| `--text-h1` | DM Serif Display | 3rem (48px) | 400 | 1.1 | -0.015em | Page titles |
| `--text-h2` | DM Serif Display | 2rem (32px) | 400 | 1.2 | -0.01em | Section headings |
| `--text-h3` | Inter | 1.25rem (20px) | 600 | 1.3 | -0.005em | Card headings, subsections |
| `--text-h4` | Inter | 1rem (16px) | 600 | 1.4 | 0em | Form section labels, tight headings |
| `--text-body-lg` | Inter | 1.125rem (18px) | 400 | 1.7 | 0em | Lead paragraphs |
| `--text-body` | Inter | 1rem (16px) | 400 | 1.65 | 0em | Standard body |
| `--text-body-sm` | Inter | 0.875rem (14px) | 400 | 1.6 | 0em | Secondary body, form help text |
| `--text-label` | Inter | 0.875rem (14px) | 500 | 1.4 | 0.02em | Form labels, nav items |
| `--text-caption` | Inter | 0.75rem (12px) | 400 | 1.5 | 0.01em | Timestamps, fine print |
| `--text-overline` | Inter | 0.6875rem (11px) | 600 | 1.4 | 0.1em | Uppercase labels above headings |
| `--text-mono` | JetBrains Mono | 0.875rem (14px) | 400 | 1.5 | 0em | Code, IDs, confirmation numbers |

### Overline Treatment
Overline text is always uppercase. Example: "FREE EVENT" above the hero headline. Used to set context before a serif display heading.

---

## 1.4 Spacing Scale (4px base grid)

| Token | Value | Usage |
|---|---|---|
| `--space-xs` | 4px | Icon-to-label gap, tight internal padding |
| `--space-sm` | 8px | Input internal padding (vertical), badge padding |
| `--space-md` | 16px | Card padding (inner), form field gap |
| `--space-lg` | 24px | Section internal spacing, button padding (horizontal) |
| `--space-xl` | 40px | Between cards, between form groups |
| `--space-2xl` | 64px | Between page sections |
| `--space-3xl` | 96px | Hero vertical padding, major section breathing room |
| `--space-4xl` | 128px | Top-of-page hero vertical offset |

---

## 1.5 Border Radius Tokens

| Token | Value | Usage |
|---|---|---|
| `--radius-none` | 0px | Hard-edge decorative elements |
| `--radius-sm` | 4px | Badges, tags, chips |
| `--radius-md` | 8px | Buttons, inputs, small cards |
| `--radius-lg` | 16px | Cards, modals, panels |
| `--radius-xl` | 24px | Large hero cards, feature panels |
| `--radius-full` | 9999px | Pills, avatar circles, toggle track |

---

## 1.6 Shadow Tokens

Shadows use layered box-shadows for realism. In dark mode, shadows have a slight blue-tinted color to feel "deep" rather than muddy.

**Dark Mode:**
| Token | Value | Usage |
|---|---|---|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.5), 0 1px 2px rgba(0,0,0,0.4)` | Subtle lift on small elements |
| `--shadow-md` | `0 4px 16px rgba(0,0,0,0.5), 0 2px 6px rgba(0,0,0,0.4)` | Cards, dropdowns |
| `--shadow-lg` | `0 16px 40px rgba(0,0,0,0.6), 0 4px 12px rgba(0,0,0,0.4)` | Modals, elevated panels |
| `--shadow-glow-primary` | `0 0 24px rgba(79, 170, 255, 0.30), 0 0 8px rgba(79, 170, 255, 0.20)` | CTA buttons, focused inputs |
| `--shadow-glow-secondary` | `0 0 24px rgba(192, 132, 252, 0.25), 0 0 8px rgba(192, 132, 252, 0.15)` | Accent decorative elements |
| `--shadow-glow-success` | `0 0 16px rgba(52, 211, 153, 0.30)` | Success state confirmation |

**Light Mode:**
| Token | Value | Usage |
|---|---|---|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06)` | Subtle lift |
| `--shadow-md` | `0 4px 16px rgba(0,0,0,0.10), 0 2px 6px rgba(0,0,0,0.07)` | Cards |
| `--shadow-lg` | `0 16px 40px rgba(0,0,0,0.14), 0 4px 12px rgba(0,0,0,0.08)` | Modals |
| `--shadow-glow-primary` | `0 4px 20px rgba(26, 111, 212, 0.25)` | CTA glow in light mode |
| `--shadow-glow-secondary` | `0 4px 20px rgba(124, 58, 237, 0.20)` | Secondary glow |
| `--shadow-glow-success` | `0 4px 16px rgba(5, 150, 105, 0.25)` | Success confirmation |

---

## 1.7 Motion Tokens

All animation respects `prefers-reduced-motion`. When reduced motion is active, durations collapse to 1ms (instant, still fires JS events).

| Token | Value | Usage |
|---|---|---|
| `--ease-default` | `cubic-bezier(0.16, 1, 0.3, 1)` | General transitions — spring-like snap |
| `--ease-in` | `cubic-bezier(0.4, 0, 1, 1)` | Elements leaving the screen |
| `--ease-out` | `cubic-bezier(0, 0, 0.2, 1)` | Elements entering the screen |
| `--ease-bounce` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Toast appear, modal enter — slight overshoot |
| `--duration-instant` | `80ms` | Hover background fills |
| `--duration-fast` | `150ms` | Button state changes, focus rings |
| `--duration-default` | `250ms` | Most transitions |
| `--duration-slow` | `400ms` | Page-level transitions, modal appear |
| `--duration-xslow` | `600ms` | Hero entrance animations |

---

# 2. Design System Components

## 2.1 Button

### Variants and Visual Appearance

**Primary button:**
- Background: `--accent-primary`
- Text: `--text-inverse` (white in dark mode, white in light mode)
- Border: none
- Border-radius: `--radius-md`
- Font: Inter 500
- Transition: background, box-shadow, transform — all `--duration-fast --ease-default`
- Hover: background → `--accent-primary-hover`, box-shadow → `--shadow-glow-primary`, transform: `translateY(-1px)`
- Active/Pressed: background → `--accent-primary-active`, transform: `translateY(0)`, shadow removed
- Focus: 2px outline, offset 3px, color `--interactive-focus-ring` (never hidden)
- Disabled: background `--interactive-disabled-bg`, text `--interactive-disabled-text`, cursor not-allowed, no transform, no shadow

**Secondary button:**
- Background: `--bg-elevated`
- Text: `--text-primary`
- Border: 1px solid `--border-default`
- Hover: border-color `--border-strong`, background `--interactive-hover-bg`
- Focus: same focus ring as primary
- Disabled: same disabled pattern

**Ghost button:**
- Background: transparent
- Text: `--accent-primary`
- Border: none
- Hover: background `--accent-primary-subtle`
- Active: background slightly more opaque (1.5× the subtle opacity)
- Disabled: text `--interactive-disabled-text`

**Destructive button:**
- Background: `--state-error`
- Text: `#FFFFFF`
- Border: none
- Hover: background darkened 8% (dark mode: `#E05555`, light mode: `#C01E1E`)
- Same focus/disabled pattern

### Sizes

| Size | Height | Horizontal padding | Font size | Icon size |
|---|---|---|---|---|
| sm | 32px | 12px | 0.8125rem (13px) | 14px |
| md | 40px | 16px | 0.875rem (14px) | 16px |
| lg | 48px | 24px | 1rem (16px) | 18px |

### Icon buttons
When a button contains only an icon (no label), width equals height. Add `aria-label` describing the action.

### Accessibility
- All buttons are `<button>` elements, never `<div>` or `<a>` styled as button (unless navigating, then `<a>`)
- `aria-disabled="true"` when disabled, not the `disabled` attribute alone, so focus is still reachable for screen readers
- Loading state: add `aria-busy="true"` and replace label with spinner + sr-only text "Loading..."

---

## 2.2 Input Fields

### Base appearance (text, email, tel)
- Height: 44px (meets touch target minimum)
- Background: `--bg-card`
- Border: 1px solid `--border-default`
- Border-radius: `--radius-md`
- Font: Inter 400, `--text-body`
- Text color: `--text-primary`
- Placeholder color: `--text-muted`
- Horizontal padding: 14px
- Label: positioned above the input, `--text-label`, `--text-secondary`, margin-bottom 6px
- Help text: below input, `--text-caption`, `--text-muted`, margin-top 4px
- Transition: border-color, box-shadow — `--duration-fast`

**Idle:** border `--border-default`

**Focused:** border `--border-accent`, box-shadow `0 0 0 3px rgba(--interactive-focus-ring, 0.20)` (use the actual color value). Label color shifts to `--accent-primary`.

**Filled (has value, not focused):** border `--border-default`, text `--text-primary`. No special treatment needed beyond having a value.

**Error:** border `--state-error`, box-shadow `0 0 0 3px rgba(248,113,113,0.15)` (dark) / `rgba(220,38,38,0.12)` (light). Error message appears below in `--state-error` color with a warning icon (16px) to the left of the message text.

**Disabled:** background `--interactive-disabled-bg`, border `--border-subtle`, text `--interactive-disabled-text`, cursor not-allowed.

### Textarea
Same as text input but:
- Min height: 120px
- Padding: 12px 14px
- Resize: vertical only
- No resize handle in Firefox (use `resize: vertical`)
- `rows` attribute set to reflect visible height

### Accessibility
- Always use `<label>` with `for` attribute matching input `id`
- Error message linked via `aria-describedby`
- Required fields: `aria-required="true"`, do NOT use red asterisk as the only indicator — include "(required)" in help text or label

---

## 2.3 Select / Dropdown

**Appearance:**
- Same height/border/radius/font as text input (44px, `--radius-md`)
- Custom arrow icon: 16px chevron-down SVG in `--text-muted`, positioned 14px from right edge
- Native `<select>` element — `appearance: none` to hide default chrome
- Background: `--bg-card`

**Open state (native behavior):** Browser handles the dropdown. This is intentional for accessibility and progressive enhancement — custom dropdowns are a known accessibility foothole. Do not rebuild with Vue unless the UX requires it (e.g., searchable select).

**Focused:** Same focus ring as inputs.
**Error:** Same error treatment as text input.
**Disabled:** Same disabled treatment.

---

## 2.4 Checkbox and Radio Group

### Checkbox
**Visual:**
- Custom checkbox: 20×20px square, `--radius-sm` (4px), border 2px solid `--border-strong`
- Background: `--bg-card`
- Checkmark: white SVG check, visible only when checked
- Checked state: background `--accent-primary`, border-color `--accent-primary`
- Checked animation: scale from 0.7 to 1.0 over `--duration-fast` with `--ease-bounce`
- Label: `--text-body`, `--text-primary`, cursor pointer, 8px gap between box and label

**Hover (unchecked):** border-color `--border-accent`, background `--accent-primary-subtle`
**Focus:** 2px focus ring offset 2px, same color as all focus rings
**Disabled:** box `--interactive-disabled-bg`, border `--border-subtle`, label `--interactive-disabled-text`

**HTML:** Use real `<input type="checkbox">` visually hidden (clip-path or sr-only) with a sibling `<span>` as the visual target. Never hide with `display:none` (breaks keyboard).

### Radio Group
**Visual:**
- 20×20px circle, border 2px solid `--border-strong`
- Selected: outer ring `--accent-primary` (full border), inner filled dot: 8×8px circle `--accent-primary` centered
- Selection animation: inner dot scales from 0 to 1 over `--duration-fast --ease-bounce`
- Group label: `--text-h4`, `--text-secondary`, margin-bottom `--space-sm`
- Each option: same label/gap treatment as checkbox
- Options arranged vertically (stacked) by default; can be 2-column grid on desktop when options are short

**Accessibility:**
- Wrapped in `<fieldset>` + `<legend>` for screen reader grouping
- `role="radiogroup"` on the container if not using `<fieldset>`

---

## 2.5 Progress Stepper (Multi-Step Wizard)

**Layout:** Horizontal row at the top of the registration wizard, spanning full card width. On mobile (< 640px), collapses to "Step 2 of 4" text with a linear progress bar below.

**Desktop step anatomy:**
```
  [1]  ——————————  [2]  ——————————  [3]  ——————————  [4]
 Step  Step label  Step  Step label  Step  Step label  Step
```

**Step indicator circle:** 32×32px circle.
- Completed: filled `--accent-primary` background, white checkmark icon (16px SVG)
- Active/Current: filled `--accent-primary` background, white step number (Inter 600)
- Future: border 2px solid `--border-default`, background transparent, number in `--text-muted`

**Connector line:** 2px horizontal line between circles.
- Completed segment: `--accent-primary`
- Incomplete segment: `--border-default`
- Line animates fill from left to right when a step is completed (transition: width over `--duration-slow --ease-out`)

**Step label text:** Below the circle, `--text-caption`, centered.
- Completed: `--text-secondary`
- Active: `--accent-primary`, Inter 600
- Future: `--text-muted`

**Accessibility:**
- Wrap in `<nav aria-label="Registration steps">`
- Each step is an `<ol>` list item
- Active step: `aria-current="step"`
- Completed steps: `aria-label="Step 1: Personal Info — completed"`
- Future steps do NOT link — they are non-interactive

---

## 2.6 Card

### Default card
- Background: `--bg-card`
- Border: 1px solid `--border-default`
- Border-radius: `--radius-lg`
- Padding: `--space-lg` (24px) all sides
- Box-shadow: `--shadow-sm`
- No transition

### Interactive (clickable) card
- Same as default, plus:
- Cursor: pointer
- Transition: border-color, box-shadow, transform — `--duration-default --ease-default`
- Hover: border-color `--border-accent`, box-shadow `--shadow-md`, transform `translateY(-2px)`
- Active: transform `translateY(0)`
- Focus (keyboard): 2px focus ring, offset 3px, `--interactive-focus-ring`
- Entire card is wrapped in `<a>` or has `role="button"` tabindex="0" — use `<a>` where the destination is a URL

### Elevated card
- Background: `--bg-elevated`
- No border (relying on shadow instead)
- Box-shadow: `--shadow-md`
- Border-radius: `--radius-xl`
- Padding: `--space-xl` (40px)
- In dark mode: adds a subtle top-edge gradient (`--gradient-card-edge`) as a pseudo-element to suggest light hitting the top edge

---

## 2.7 Badge / Tag

**Usage:** Registration type labels (Attendee, Presenter, Volunteer), event format labels.

**Anatomy:** Inline-flex, vertically centered. Optional 12px icon to the left of text.

**Sizes:**
- Default: height 24px, horizontal padding 10px, `--text-caption`, border-radius `--radius-sm`
- Large: height 32px, horizontal padding 14px, `--text-body-sm`, border-radius `--radius-sm`

**Variants:**

| Variant | Background (dark) | Text (dark) | Background (light) | Text (light) |
|---|---|---|---|---|
| Attendee | `rgba(79,170,255,0.15)` | `#4FAAFF` | `rgba(26,111,212,0.10)` | `#1A6FD4` |
| Presenter | `rgba(192,132,252,0.15)` | `#C084FC` | `rgba(124,58,237,0.10)` | `#7C3AED` |
| Volunteer | `rgba(52,211,153,0.15)` | `#34D399` | `rgba(5,150,105,0.10)` | `#059669` |
| Neutral | `--border-default` | `--text-secondary` | `--border-default` | `--text-secondary` |

No border on badges — colored background + colored text is sufficient.

---

## 2.8 Navigation Bar

### Desktop (≥ 1024px)
**Height:** 64px
**Position:** Fixed to top, full width, z-index 100
**Background:** `--bg-page` at 95% opacity with `backdrop-filter: blur(20px) saturate(180%)`
**Bottom border:** 1px solid `--border-subtle`

**Left zone:** Logo/wordmark — "Skepticamp NYC" in display font, 1.25rem. Clicking navigates to `/`.

**Center zone:** Navigation links — `--text-label`, `--text-secondary`. Links: Home, About, Contact. Spacing: 32px between each link.
- Hover: `--text-primary`, underline 2px `--accent-primary` with animation (width from 0% to 100%, `--duration-fast`)
- Active page: `--text-primary`, permanent 2px underline `--accent-primary`

**Right zone:** Two elements, 16px gap.
1. Theme toggle button (see Section 4.1)
2. "Register" CTA — primary button, size `sm`

**Scroll behavior:** At page top, the nav background is fully transparent. After scrolling 20px, the frosted-glass background fades in over `--duration-default`. This gives the hero a seamless full-bleed effect.

### Mobile (< 1024px)
**Height:** 56px
**Left:** Logo wordmark
**Right:** Two icons — theme toggle, then hamburger (three horizontal lines, 24px SVG)

**Hamburger open state:**
- Full-screen overlay: `--bg-page` at 98% opacity, slides in from right over `--duration-slow --ease-out`
- Hamburger icon morphs to X (cross) via SVG path animation over `--duration-default`
- Nav links stacked vertically, centered, 48px tap targets, `--text-h2` size, `--text-primary`
- Links appear sequentially with staggered fade-in (50ms delay between each)
- "Register" button at the bottom of the list, full width, primary variant, lg size
- Close on: X tap, Escape key, link navigation, backdrop tap

**Accessibility:**
- Nav is `<nav aria-label="Main navigation">`
- Mobile menu button: `aria-expanded`, `aria-controls="mobile-menu"`
- Mobile menu div: `id="mobile-menu"`, `role="dialog"`, `aria-modal="true"`, `aria-label="Navigation menu"`
- Focus trapped inside open mobile menu
- First focusable element inside menu receives focus on open; focus returns to hamburger on close

---

## 2.9 Modal / Dialog

**Backdrop:** `--bg-overlay`, covers full viewport, z-index 200. Clicking backdrop closes the modal (unless `dismissible={false}`).

**Modal container:**
- Max-width: 560px for standard; 760px for wide variant
- Width: `calc(100vw - 48px)` on mobile
- Background: `--bg-elevated`
- Border: 1px solid `--border-default`
- Border-radius: `--radius-xl`
- Box-shadow: `--shadow-lg`
- Padding: `--space-xl` (40px)

**Animation:**
- Enter: backdrop fades from opacity 0 to 1 (`--duration-slow`); modal scales from 0.95 + opacity 0 to 1.0 + opacity 1 (`--duration-slow --ease-out`)
- Exit: reverse, `--duration-default`

**Structure:**
- Header: title (`--text-h3`), optional subtitle (`--text-body-sm --text-secondary`), close button (X icon, 24px, ghost icon button, top-right corner)
- Body: scrollable if content overflows, max-height `calc(100vh - 200px)`
- Footer: action buttons, right-aligned, gap `--space-sm`

**Accessibility:**
- `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to title
- Focus trapped inside; first focusable element gets focus on open
- Close button: `aria-label="Close dialog"`
- Escape key closes
- `<body>` gets `overflow: hidden` while modal is open

---

## 2.10 Toast Notifications

**Position:** Fixed, bottom-right corner on desktop; bottom-center on mobile. 24px from edges.

**Anatomy:** 16px icon (left) + text content (flex-grow) + optional dismiss X button (right). Height: auto, min 48px. Max-width: 380px. Padding: 14px 16px.

**Appearance:**
- Border-radius: `--radius-md`
- Border-left: 4px solid (color varies by variant)
- Background: `--bg-elevated`
- Box-shadow: `--shadow-lg`

| Variant | Left border color | Icon | Icon color |
|---|---|---|---|
| Success | `--state-success` | checkmark-circle | `--state-success` |
| Error | `--state-error` | x-circle | `--state-error` |
| Info | `--state-info` | info-circle | `--state-info` |
| Warning | `--state-warning` | alert-triangle | `--state-warning` |

**Title:** `--text-body-sm`, Inter 600, `--text-primary`
**Message:** `--text-caption`, `--text-secondary`

**Animation:**
- Enter: slides up from bottom + fade in, `--duration-default --ease-bounce`
- Exit: slides down + fade out, `--duration-fast --ease-in`
- Multiple toasts stack with 8px gap; new toasts push existing ones up

**Auto-dismiss:** Success and info: 5 seconds. Error and warning: persist until dismissed manually (or 10 seconds). A thin progress bar along the bottom of the toast shows time remaining.

**Accessibility:**
- `role="status"` for success/info; `role="alert"` for error/warning
- `aria-live="polite"` for status; `aria-live="assertive"` for alerts
- Dismiss button: `aria-label="Dismiss notification"`

---

## 2.11 Cookie Consent Banner

**Position:** Fixed, bottom of viewport, full width. z-index 300 (above everything except modals).

**Appearance:**
- Background: `--bg-elevated`
- Top border: 1px solid `--border-default`
- Box-shadow: `--shadow-lg` (inverted — upward)
- Padding: `--space-md` `--space-lg` (16px top/bottom, 24px sides)

**Layout (desktop):** Two columns. Left: icon + text. Right: action buttons.
- Left icon: cookie SVG, 24px, `--accent-primary`
- Heading: "This site uses cookies" — `--text-body-sm`, Inter 600
- Body: "We use cookies to remember your theme preference and measure visit traffic (if you allow). We never sell your data." — `--text-caption`, `--text-secondary`
- Link: "Privacy policy" inline in body text, `--text-accent`

**Buttons (right, row, gap `--space-sm`):**
1. "Manage preferences" — ghost, sm
2. "Decline all" — secondary, sm
3. "Accept all" — primary, sm

**Enter animation:** Slides up from below viewport over `--duration-slow --ease-out`, after a 400ms page-load delay (so it doesn't compete with hero entrance).

**Preferences modal** (triggered by "Manage preferences"):
- Opens standard modal with toggle switches for each category
- Categories: "Necessary" (always on, disabled), "Analytics" (default off)
- Each toggle: 44×24px pill with sliding thumb, same animated style as theme toggle
- "Save preferences" primary button at bottom

**Accessibility:**
- Banner: `role="region"`, `aria-label="Cookie consent"`
- Dismiss via Escape key (declines all — most conservative action)

---

## 2.12 Loading States

### Spinner
- 24px SVG circle with a 3px stroke, 25% of the arc colored `--accent-primary`, rest `--border-default`
- Rotates 360° over 800ms linear, infinite
- Sm variant: 16px, 2px stroke
- Lg variant: 40px, 4px stroke

### Skeleton Screen
Used in place of content while loading asynchronous data.

**Anatomy:** Rounded rectangles at the same size and position as the content they replace.
- Background: linear-gradient shimmer — from `--border-subtle` through `--border-default` back to `--border-subtle`, animated at 1.5s linear infinite (shimmer moves left to right)
- Border-radius: matches the element being replaced (`--radius-sm` for text lines, `--radius-lg` for cards)
- Text skeleton lines: height 12px for body, 20px for headings, width varies (100%, 75%, 50% for multiple lines)

**Full page loading:** Center-screen spinner with the Skepticamp NYC wordmark above it, both fading in at `--duration-slow`.

---

# 3. Page-by-Page Layout Specifications

## 3.1 Home / Hero Page

### Hero Section

**Full viewport height.** Background: `--gradient-hero`. Overflow hidden.

**Decorative background layer (CSS only, no images required):**
In dark mode: a large, blurred radial gradient positioned upper-right, approximately 60vw diameter, colors `rgba(79,170,255,0.07)` to transparent. A second smaller radial gradient lower-left, colors `rgba(192,132,252,0.06)` to transparent. These create the impression of distant nebulae — a nod to scientific inquiry. In light mode: the same treatment in very low opacity (`0.04`) creates a warm, barely-there color wash.

**Content layout:** Centered column, max-width 760px, horizontally and vertically centered in the viewport with a slight upward bias (vertical translation -40px from true center).

**Content (top to bottom):**

1. **Overline tag:** Badge component (Neutral variant, lg size): "December 6, 2025 · Free · New York City". Appears with fade-in + slide-up, delay 0ms.

2. **Display headline:** `--text-display` (4.5rem), DM Serif Display, `--text-primary`. Text:
   > "Share the Apple of Knowledge"
   The word "Knowledge" is rendered with `--gradient-accent` applied as a `background-clip: text` gradient. Appears with fade-in + slide-up, delay 100ms.

3. **Subheadline:** `--text-body-lg`, `--text-secondary`, max-width 560px, centered. Text:
   > "A free, one-day unconference where curious New Yorkers present and explore science, critical thinking, and consumer protection — no credentials required."
   Appears with fade-in + slide-up, delay 200ms.

4. **CTA button row:** Two buttons, center-aligned, gap 16px. Appears with fade-in + slide-up, delay 300ms.
   - Primary lg: "Register Now" — navigates to `/register/` (registration type selection page)
   - Ghost lg: "Learn More" — smooth-scrolls to the About strip below

5. **Scroll indicator:** At bottom of hero viewport, centered. A small animated chevron-down icon (16px `--text-muted`) bouncing gently (translateY -6px to 0, 1.5s ease-in-out infinite). Disappears after user scrolls 50px.

**Slide-up entrance animation:** All hero text elements translate from `translateY(24px)` + `opacity: 0` to `translateY(0)` + `opacity: 1`. Duration `--duration-xslow`, easing `--ease-out`. Uses staggered delays as listed above.

---

### Event Info Strip

**Directly below hero.** Full width. Background: `--bg-card`. Border top and bottom: 1px solid `--border-default`. Padding: `--space-lg` 0.

**Layout:** Horizontal row of three stats, evenly spaced, centered. Separated by 1px vertical dividers.

| Icon | Stat |
|---|---|
| Calendar SVG | "December 6, 2025 · 9:30 AM – 6 PM EST" |
| Map-pin SVG | "151 W. 30th St, 3rd Floor, New York, NY 10001" |
| Tag/ticket SVG | "Free — Optional $20 donation to NYC Skeptics" |

**Each item:** 20px icon (left, `--accent-primary`), then two lines: label in `--text-overline` `--text-muted` uppercase, value in `--text-body-sm` `--text-primary` Inter 500.

On mobile: stacks vertically, dividers become horizontal.

---

### Registration Type Cards

**Section:** Full-width, background `--bg-page`. Padding: `--space-3xl` 0.

**Section header:**
- Overline: "Join Us" (centered, `--text-overline`, `--text-muted`)
- Heading: "How do you want to participate?" — `--text-h1`, DM Serif Display, centered
- Subtext: "Everyone is welcome. Choose your role — you can always change your mind later." — `--text-body-lg`, `--text-secondary`, centered, max-width 560px

**Card layout:** Three cards in a horizontal row (1-column on mobile), gap `--space-lg`, max-width 1100px, centered with horizontal padding.

**Each card is an Interactive card component (see 2.6) with these specifics:**

**Attendee Card:**
- Top accent: 4px top border, color `#4FAAFF` (or light mode `#1A6FD4`)
- Icon: 48px in a 72×72px rounded square container, background `rgba(79,170,255,0.12)`, icon color `#4FAAFF` — use a "person walking" or "audience" style icon
- Badge: "Attendee" badge (blue variant) in top-right corner of card
- Heading: "Come and Learn" — `--text-h3`
- Body: "Attend talks from fellow curious New Yorkers. No agenda, no jargon requirements — just science and good conversation." — `--text-body-sm`, `--text-secondary`
- List (3 bullet points with checkmark icons in `--state-success`):
  - "Free entry to all sessions"
  - "Live and streaming options available"
  - "Adults, college students, and families welcome"
- CTA: Full-width primary button "Register as Attendee" at bottom of card

**Presenter Card:**
- Top accent: 4px top border, color `#C084FC` (or light mode `#7C3AED`)
- Icon: same container, background `rgba(192,132,252,0.12)`, icon `#C084FC` — use a "microphone" or "speaking" icon
- Badge: "Presenter" badge (violet variant) — with a small star icon to the left to indicate "featured" role
- Heading: "Share What You Know" — `--text-h3`
- Body: "Have something to say about science, skepticism, or critical thinking? Submit a talk proposal. 15 or 30 minute slots available." — `--text-body-sm`, `--text-secondary`
- List (3 points):
  - "15 or 30 minute presentation slots"
  - "Topic proposals reviewed by organizers"
  - "No expert credentials required"
- CTA: Full-width primary button variant using `--accent-secondary` color "Submit a Talk" at bottom

**Volunteer Card:**
- Top accent: 4px top border, color `#34D399` (or light mode `#059669`)
- Icon: same container, background `rgba(52,211,153,0.12)`, icon `#34D399` — use a "hands helping" or "star" icon
- Badge: "Volunteer" badge (green variant)
- Heading: "Help Make It Happen" — `--text-h3`
- Body: "Volunteers keep Skepticamp running smoothly. Set up, check-in, AV support, and more — plus you get to see every talk." — `--text-body-sm`, `--text-secondary`
- List (3 points):
  - "A/V, registration, and setup roles"
  - "Lunch and snacks provided"
  - "First access to presenter Q&A"
- CTA: Full-width secondary button "Volunteer with Us" at bottom

**Card hover behavior:** On hover, the top accent border glows via box-shadow (matching the card's accent color at 30% opacity, spread 4px). The icon container background opacity increases slightly.

---

### About Teaser Strip

**Below registration cards.** Background: `--bg-card`. Padding: `--space-3xl` 0.

**Layout:** Two columns on desktop (50/50 split), single column on mobile.

**Left column:** Text content.
- Overline: "About Skepticamp"
- Heading: "Critical thinking, community-built" — `--text-h2`
- Body (2 paragraphs): Describe NYC Skeptics mission, the unconference format, history since 2009.
- Link: "Read our full story →" — ghost button pointing to `/about/`

**Right column:** An abstract, CSS-only decorative panel. A grid of 5×5 dots (8px circles, `--border-default` fill), centered in the column. The center 9 dots (3×3 grid) use `--accent-primary` and `--accent-secondary` in a gradient fill. This creates a "constellation" effect suggesting scientific data visualization. In dark mode it glows faintly.

---

### Past Events Strip

**Below About Teaser.** Background: `--bg-page`. Padding: `--space-2xl` 0.

**Layout:** Horizontal row of year badges — a simple, low-height strip.
- Label: "Skepticamp NYC has been happening since" — `--text-body-sm`, `--text-muted`
- Year chips: Pill badges (Neutral variant) for each year from 2009 to 2024, displayed in a wrapping flex row, gap 8px, centered.
- Below: "…and we're not stopping." — `--text-body-sm`, `--text-secondary`, italic, centered.

---

### Footer

**Background:** `--bg-card`. Border-top: 1px solid `--border-default`. Padding: `--space-2xl` 0 `--space-lg`.

**Layout:** Three columns on desktop, stacked on mobile.

**Column 1 — Brand:**
- Skepticamp NYC wordmark
- "An unconference by NYC Skeptics"
- Link to nycskeptics.org (opens in new tab with `rel="noopener noreferrer"`)

**Column 2 — Navigation:**
- Links: Home, About, Contact, Register, Admin Login
- `--text-body-sm`, `--text-secondary`

**Column 3 — Contact:**
- "admin@skepticampnyc.org" — linked
- Organizer: Mitchell Scott Lampert

**Bottom bar:** Full-width divider, then "© 2025 NYC Skeptics · 501(c)(3) nonprofit · All rights reserved" centered in `--text-caption --text-muted`. Right-aligned: "Privacy Policy" link.

---

## 3.2 About Page

**Page title:** "About Skepticamp NYC" — `--text-h1`, DM Serif Display

**URL:** `/about/`

### Hero (not full-viewport — shorter)
**Height:** 360px on desktop, 280px on mobile.
**Background:** `--gradient-hero` with the same subtle radial gradients as home.
**Content:** Centered column.
- Overline: "Our Story"
- Heading: "Where skeptics come to share and learn" — `--text-h1`
- No CTA buttons — this is a reading destination

### Section 1 — What is Skepticamp?
**Background:** `--bg-page`. Padding: `--space-3xl` 0.
**Layout:** Single centered column, max-width 700px.
- `--text-h2` heading: "The unconference format"
- `--text-body-lg` lead paragraph: "Skepticamp is not a traditional conference. There's no keynote, no ticket price, and no speaker bureau. Anyone with something to say about science or critical thinking can propose a talk."
- Standard body paragraphs explaining the open/collaborative format. Each paragraph max-width 700px, generous line-height (1.7).

### Section 2 — What is Scientific Skepticism?
**Background:** `--bg-card`. Full-width. Padding: `--space-3xl` 0.
**Layout:** Two-column on desktop. Left: definition text. Right: a styled "pull quote" card.

**Pull quote card (right column):**
- Elevated card component
- Large quotation mark: "❝" in display font, 96px, `--accent-primary`, opacity 0.5 (decorative)
- Quote text: "Scientific skepticism is the intersection of science education and consumer protection. We help people learn from science to avoid spending money on products and services that do not work." — `--text-body-lg`, `--text-secondary`
- Attribution: "— NYC Skeptics" — `--text-label`, `--text-muted`

### Section 3 — The Organizers
**Background:** `--bg-page`. Padding: `--space-3xl` 0.
**Section heading:** `--text-h2` "The team behind Skepticamp"
**Layout:** Horizontal row of cards, or 2-column grid. Each card:
- 64×64px circle avatar placeholder (background `--bg-elevated`, dashed border `--border-default` if no image — initials centered in the avatar circle in `--text-h4 --text-secondary`)
- Name: `--text-h4`
- Role/title: `--text-body-sm`, `--text-muted`
Cards centered, max 5 per row.

Team: Mitchell Scott Lampert (Lead Organizer), Jonathan Nelson, Benny Pollak, Russ Dobler, Craig Sachs.

### Section 4 — NYC Skeptics Partnership
**Background:** `--bg-card`. Padding: `--space-2xl` 0.
**Layout:** Centered column, max-width 700px. Logo + text + link to nycskeptics.org.

### Section 5 — CTA Banner
**Background:** Uses `--gradient-accent` as background (the blue-to-violet gradient). Padding: `--space-2xl`.
- Text: "Ready to join us?" — `--text-h2`, white
- Subtext: "Register free in under 2 minutes." — `--text-body-lg`, `rgba(255,255,255,0.80)`
- Two buttons: "Register Now" (white background, `--accent-primary` text), "Contact Us" (white outline)

---

## 3.3 Contact Page

**URL:** `/contact/`

**Page hero:** Short (240px), same style as About. Heading: "Get in Touch". Subtext: "Questions about Skepticamp NYC? We're here to help."

### Form Section
**Layout:** Two-column on desktop (≥ 1024px). Left: form. Right: contact info sidebar.

**Left — Contact form:**
Wrapped in an elevated card component.

Fields (in order):
1. **Name** — text input, required, placeholder "Your full name"
2. **Email** — email input, required, placeholder "your@email.com"
3. **Subject** — select dropdown. Options: "General question", "Presenter inquiry", "Volunteer inquiry", "Sponsorship", "Accessibility accommodation", "Other"
4. **Message** — textarea, required, min-height 160px, placeholder "Tell us what's on your mind…"
5. **Privacy acknowledgment** — single checkbox: "I understand that my contact information will only be used to respond to this inquiry and will not be shared with third parties." Required.

Submit button: Primary, lg, full width. Text: "Send Message"

**Inline validation:** On blur for each field. Error appears below the field. Submit button stays enabled — validation runs on submit if user hasn't touched a field.

**Success state:** Form is replaced (fade out/in) by a success panel within the same card:
- Large checkmark icon (48px) in `--state-success` with a `--shadow-glow-success`
- Heading: "Message sent!" — `--text-h3`
- Body: "We'll get back to you at [user's email] within a few days. Thank you for reaching out."
- "Back to Home" ghost button

**Right — Contact info sidebar:**
Not a card — plain layout with generous spacing.
- Email: admin@skepticampnyc.org (mailto link)
- Lead organizer: Mitchell Scott Lampert
- "We're a volunteer-run organization — we appreciate your patience with response times."
- Org link: New York City Skeptics (nycskeptics.org)

Below sidebar: a minimal FAQ list (3–4 items) using an accordion component (not specified above, but simple: question in `--text-h4`, answer in `--text-body-sm`, expand/collapse with chevron rotation animation `--duration-fast`).

FAQ items:
- "Is Skepticamp really free?" — Yes. There's an optional $20 donation to NYC Skeptics.
- "Can I present if I'm not an expert?" — Absolutely. The unconference format welcomes all curious people.
- "Is there a streaming option?" — Yes, details announced closer to the event.
- "Is the venue accessible?" — Yes, 151 W. 30th St has elevator access. Contact us for specific needs.

---

## 3.4 Registration Flow

**URL structure:**
- `/register/` — registration type selection (gateway)
- `/register/attendee/` — attendee wizard
- `/register/presenter/` — presenter wizard
- `/register/volunteer/` — volunteer wizard
- `/register/confirmation/<token>/` — confirmation page

### Registration Gateway (`/register/`)

Short hero (280px). Heading: "Register for Skepticamp NYC". Subtext: "December 6, 2025 · Free"

Below hero: Three large interactive cards, same design as home page registration cards (Section 3.1), but without the bullet list — more minimal. Each card links to its respective wizard URL.

---

### Wizard Shell (shared by all three flows)

**Layout:** The wizard sits in a centered elevated card, max-width 680px, with horizontal padding. Vertical padding `--space-xl`. The card is the primary focus — page background (`--bg-page`) is visible around it, creating depth.

**Above the card:** Breadcrumb — "Registration > [Attendee / Presenter / Volunteer]" in `--text-caption --text-muted`.

**Inside the card, fixed top:** Progress Stepper component (Section 2.5). Stays at top as user scrolls through a step with long content.

**Step content area:** Padding `--space-lg` top. Each step scrolls internally if needed (though steps should be kept short enough not to require this on desktop).

**Navigation buttons (bottom of card, always visible):**
- Left: "← Back" — ghost sm button (hidden on Step 1)
- Right: "Continue →" (all steps except last) or "Submit Registration" (last step) — primary sm button

Button row is sticky at bottom of the card with a `--border-default` top border separator and `--bg-elevated` background to avoid content showing through.

---

### Attendee Wizard (4 steps)

**Step 1: Personal Information**
- Heading: "Tell us about you" — `--text-h3`
- Fields:
  - First name (required) + Last name (required) — side by side on desktop, stacked on mobile
  - Email (required)
  - Phone (optional) — help text: "Only used if we need to reach you day-of"
  - "How did you hear about Skepticamp?" — select: "Friend/word of mouth", "NYC Skeptics mailing list", "Eventbrite", "Social media", "Google/web search", "Other"

**Step 2: Attendance Preferences**
- Heading: "How will you attend?"
- Fields:
  - Radio group — "Attendance format": "In-person at 151 W. 30th St", "Live stream (online)"
  - Checkbox group — "Dietary needs" (if attending in person): "Vegetarian", "Vegan", "Gluten-free", "Nut allergy", "No restrictions"
  - Textarea (optional) — "Any accessibility accommodations needed?" — help text: "We will do our best to accommodate all needs."

**Step 3: Donation (Optional)**
- Heading: "Support NYC Skeptics" — `--text-h3`
- Subtext: "Skepticamp is free, but your support keeps it going. NYC Skeptics is a 501(c)(3) nonprofit."
- Radio group: "$0 (no donation)", "$10", "$20", "$50", "Other amount"
- If "Other amount" selected: a text input appears below with `--duration-fast` slide-down animation. Placeholder: "Enter amount ($USD)".
- Note: "Donation processed separately — this is not a payment step. You'll receive a link after registration."
- No actual payment processing in this form.

**Step 4: Review and Submit**
- Heading: "Review your information" — `--text-h3`
- Display all collected information in a read-only summary view. Each field shown as:
  - Label: `--text-label --text-muted`
  - Value: `--text-body --text-primary`
  - "Edit" link next to each section (jumps back to that step)
- Checkbox: "I confirm that the information above is correct and I agree to the [Code of Conduct](#)." Required. Link opens modal.
- Submit button: "Complete Registration" (primary, lg, full width)

---

### Presenter Wizard (5 steps)

**Step 1: Personal Information** — same as Attendee Step 1.

**Step 2: Talk Proposal**
- Heading: "Your presentation" — `--text-h3`
- Fields:
  - Talk title (required) — text input, max 100 characters, character counter shown below right (e.g., "47/100")
  - Talk duration — radio group: "15 minutes", "30 minutes"
  - Talk description (required) — textarea, min-height 200px, max 500 chars, character counter. Help text: "Summarize your topic, what attendees will learn, and why it matters."
  - Expertise level of audience — select: "General public", "Scientifically curious", "Technical audience"

**Step 3: Speaker Background**
- Heading: "About you as a speaker" — `--text-h3`
- Fields:
  - Short bio (optional) — textarea, max 250 chars, character counter. Help text: "Shared in the program — keep it casual."
  - Affiliation (optional) — text input. Help text: "Organization, university, or 'Independent' — whichever you prefer."
  - Have you presented at Skepticamp before? — radio: "Yes", "No"
  - AV needs — checkbox group: "Projector/screen", "Microphone", "Whiteboard", "None — I'll just talk"

**Step 4: Attendance and Format**
- Heading: "Day-of details" — `--text-h3`
- Fields:
  - Will you present in person or remotely? — radio: "In person", "Remote (video call)"
  - If remote selected: a note appears — "Remote presenting is available but equipment is not guaranteed. Please contact us in advance."
  - Preferred session time — select: "Morning (9:30 AM – 12 PM)", "Afternoon (1 PM – 3 PM)", "Late afternoon (3 PM – 6 PM)", "No preference"
  - Dietary needs (same checkbox group as Attendee)

**Step 5: Review and Submit** — same structure as Attendee Step 4, but showing all presenter-specific fields too. Submit button: "Submit Talk Proposal".

---

### Volunteer Wizard (3 steps)

**Step 1: Personal Information** — same as Attendee Step 1.

**Step 2: Volunteer Preferences**
- Heading: "How do you want to help?" — `--text-h3`
- Checkbox group (required, select at least one) — "Volunteer roles I'm interested in":
  - "Registration / check-in"
  - "A/V and technical support"
  - "Setup and breakdown (8 AM – 10 AM)"
  - "Social media / live coverage"
  - "Floater (wherever needed)"
- Textarea (optional) — "Anything else we should know about your availability or skills?"
- Attendance format — radio: "Attending full day", "Available for specific shifts only"
- If "Specific shifts": textarea appears — "Describe your availability"
- Dietary needs (same checkbox group)

**Step 3: Review and Submit** — same structure. Submit button: "Sign Up to Volunteer".

---

### Confirmation Page (`/register/confirmation/<token>/`)

**Layout:** Full-page centered column, max-width 600px. Vertical padding `--space-4xl`. Not inside a wizard shell — fresh, celebratory page.

**Content:**

1. **Animated checkmark:** A 72×72px circle (border `--state-success`, box-shadow `--shadow-glow-success`). Inside: a checkmark SVG that draws itself via `stroke-dashoffset` animation — the path draws from 0% to 100% over 600ms `--ease-out`. The circle scales in from 0.5 to 1.0 simultaneously.

2. **Heading:** (varies by type)
   - Attendee: "You're in! See you December 6th."
   - Presenter: "Talk proposal submitted!"
   - Volunteer: "Welcome to the team!"
   All in `--text-h1`, DM Serif Display.

3. **Subtext:** `--text-body-lg`, `--text-secondary`.
   - Attendee: "A confirmation email is on its way to [email]. We'll send event details closer to the date."
   - Presenter: "We'll review your proposal and get back to you at [email] within a week."
   - Volunteer: "We'll be in touch at [email] with your shift details."

4. **Confirmation card:** Elevated card, monospace font, showing:
   - "Confirmation #" label + token (e.g., `SKC-2025-A-00187`) in `--text-mono`
   - Type badge (Attendee/Presenter/Volunteer)
   - Name, email, event date

5. **Action row:**
   - "Add to Calendar" — secondary button (generates `.ics` file)
   - "Return to Home" — ghost button

6. **Social share nudge** (below action row, optional): "Spread the word →" with small icon links to Twitter/X and LinkedIn. Icon buttons only, 24px. `--text-muted` color, `--text-accent` on hover.

---

## 3.5 Admin Login Page

**URL:** `/admin-login/`

**Philosophy:** Distinct from the public site. The admin login is intentionally restrained — less decorative, more austere — signaling a different context (secured, professional). Uses the same color system but stripped of gradient hero and decorative elements.

**Layout:** Full-page center-aligned card (480px wide, vertically centered).

**Page background:** `--bg-page` with no gradient decoration — just flat.

**Card:** Elevated card, `--radius-xl`, `--shadow-lg`. Padding `--space-xl`.

**Card contents:**

1. **Header:**
   - Small "Skepticamp NYC" wordmark (not the full logo treatment — smaller, `--text-label` weight, `--text-muted` color). Signals the brand without fanfare.
   - Heading: "Admin Login" — `--text-h3`, Inter 600 (not serif — intentional departure)
   - Subtext: "Authorized personnel only." — `--text-caption`, `--text-muted`

2. **Security notice strip:** A narrow banner inside the card, background `--state-warning-subtle`, border `--state-warning`, border-radius `--radius-sm`, padding `--space-sm --space-md`. Text: "Access restricted to allowlisted IP addresses and requires multi-factor authentication." Icon: lock (16px, `--state-warning`). `--text-caption`, `--text-secondary`.

3. **Form fields:**
   - Username — text input, required
   - Password — password input with show/hide toggle icon button (eye/eye-off SVG) on the right side of the input
   - TOTP Code — text input, `--text-mono` font, max 6 characters, `inputmode="numeric"`. Label: "Authenticator Code". Help text: "6-digit code from your authenticator app."

4. **Submit button:** Primary lg, full width. "Sign In"

5. **Error state:** If login fails, a full-width error alert appears above the form:
   - Background `--state-error-subtle`, border `--state-error`, border-radius `--radius-md`, padding `--space-sm --space-md`
   - Icon: x-circle (16px, `--state-error`)
   - Message: "Invalid credentials or access denied. Contact your administrator if you believe this is an error."
   - `role="alert"` for screen reader announcement

6. **Footer of card:** "← Back to site" — ghost sm button, left aligned.

**No** "Forgot password?" link. Admin credential recovery is handled out-of-band.

**Rate limiting notice:** After 3 failed attempts, a notice appears: "Multiple failed attempts detected. Please wait 60 seconds before trying again." The submit button disables for 60 seconds with a countdown in the button label: "Try again in 57s…"

---

# 4. UX Interaction Patterns

## 4.1 Theme Toggle

**Placement:** In the navigation bar, rightmost icon before the Register CTA on desktop; second icon from right on mobile (before hamburger).

**Visual:** A 40×24px pill-shaped track with a 20px circle "thumb" inside.
- Dark mode: track background `#1C2040` (elevated surface color), thumb background `--accent-primary` (#4FAAFF). A crescent moon SVG (14px, white) is inside the thumb.
- Light mode: track background `#E0EBFF`, thumb background `#FFFFFF`. A sun SVG (14px, `--accent-primary`) is inside the thumb.

**Toggle animation:**
- Thumb slides from left position to right position (or vice versa) over `--duration-default --ease-default`
- Thumb uses `cubic-bezier(0.34, 1.56, 0.64, 1)` (bounce easing) to give a tactile feel
- The icon inside the thumb (moon/sun) fades out and the other fades in, cross-dissolving over `--duration-fast`
- The track background cross-fades over `--duration-slow`
- The entire page color scheme transitions via CSS transition on `--bg-page`, `--bg-card`, `--text-primary` etc., all set with `transition: color 300ms, background-color 300ms` on `:root` (or `html` element)

**State management:** Class `dark` or `light` toggled on `<html>`. Preference saved to `localStorage`. On page load, Django renders a `<script>` in `<head>` (before body renders) that reads `localStorage` and applies the class immediately — avoiding flash of wrong theme. If no preference exists, respect `prefers-color-scheme` media query.

**Accessibility:** `role="switch"`, `aria-checked="true/false"`, `aria-label="Switch to dark/light mode"`. Keyboard: Space or Enter toggles.

---

## 4.2 Multi-Step Wizard Transitions

**Transition type:** Horizontal slide. Current step slides out to the left; new step slides in from the right. When navigating backward (Back button), current slides out right, previous slides in from left.

**Mechanism:**
- Steps are absolutely positioned within a `overflow: hidden` container of fixed height
- Height of the container animates to match the incoming step's height over `--duration-default`
- Slides use `translateX` from `100%` → `0%` (entering) and `0%` → `-100%` (leaving)
- Duration: `--duration-slow` (400ms), easing `--ease-out` for enter, `--ease-in` for exit

**Field animation:** Within a step, if a field conditionally appears (e.g., "Other amount" input in Step 3 of Attendee), it slides down from `max-height: 0` to `max-height: 120px` and fades in over `--duration-default --ease-out`. Hiding is the reverse, `--ease-in`.

**Progress stepper update:** When advancing, the connector line between the completed step and the new active step fills from left to right over `--duration-slow`. The completed step's circle fills with `--accent-primary` and the number is replaced by a checkmark — both transitions happen via opacity cross-fade.

---

## 4.3 Form Validation

**Strategy:** Hybrid approach.
- **On blur** (field loses focus): validate that single field. Show error immediately below if invalid.
- **On submit:** validate all remaining untouched required fields. Scroll to the first error field smoothly (`scroll-behavior: smooth`, `scrollIntoView({block: 'center'})`). Focus the first error input.
- **On user correction:** as soon as the errored field has valid input, the error message dismisses in real time (on input event). Transition: opacity 0 + `max-height: 0` over `--duration-fast`.
- No real-time validation of untouched fields (avoids aggressive error messages before the user has had a chance to fill them out).

**Error message anatomy:** See Section 2.2 inputs. 16px warning icon + message text in `--state-error`. The input border turns `--state-error`. The label turns `--state-error`.

**Required field indication:** An asterisk (*) in `--state-error` appears after the label text. A note at the top of each step: "Fields marked * are required." — `--text-caption --text-muted`.

---

## 4.4 Cookie Consent Banner

**Appearance timing:** Fades in + slides up from below viewport 400ms after the page's `DOMContentLoaded` event. This delay prevents it competing with hero entrance animations.

**Persistence:** Once user makes a choice (Accept all, Decline all, or saves preferences), the choice is stored in `localStorage` (`skepcamp_cookie_consent`) and a session cookie is set. Banner never appears again for that user until the cookie expires (13 months) or they clear storage.

**Manage Preferences modal:**
Opens the standard modal component (Section 2.9). Title: "Cookie Preferences". Description: "We use cookies only as described below. You can change your preference at any time."

Toggle switches (44×24px pill, same animation as theme toggle but smaller):
- **Necessary cookies** — Always on. Toggle is permanently enabled (visually locked), `aria-disabled="true"`. Includes: session authentication, CSRF protection, theme preference. Description: "Required for the site to function. Cannot be disabled."
- **Analytics** — Default off. Includes: visit count tracking (no personal data). Description: "Helps us understand how many people attend versus register. No personal data collected."

Footer: "Save preferences" (primary, sm) | "Cancel" (ghost, sm)

**Escape key behavior:** Closes the consent banner by declining all non-essential cookies (most conservative action). This is documented in `aria-keyshortcuts`.

---

## 4.5 Mobile Navigation Behavior

**Trigger:** Tapping the hamburger icon.

**Open sequence:**
1. Overlay div fades in (opacity 0 → 1, `--duration-default`)
2. Panel slides in from the right (translateX: 100% → 0, `--duration-slow --ease-out`) — panel is full width on mobile
3. Hamburger icon morphs to X: the top line rotates 45°, the middle fades out, the bottom rotates -45°. All via CSS transforms over `--duration-default`
4. Navigation links fade in with stagger: each link fades from opacity 0 to 1 + translateY(12px → 0), delays: 50ms, 100ms, 150ms, 200ms, 250ms
5. Focus moves to the first navigation link in the menu

**Close triggers:**
- Tapping X button
- Pressing Escape
- Tapping a navigation link (after navigation begins)
- Tapping outside the panel (on the backdrop)

**Close sequence:** Reverse of open, but faster (`--duration-default` for panel, `--duration-fast` for overlay). Focus returns to hamburger button.

**Body scroll:** Locked (`overflow: hidden` on `<body>`) while menu is open.

---

## 4.6 Keyboard Navigation and Focus Rings

**Focus ring specification:**
All interactive elements: `outline: 2px solid var(--interactive-focus-ring); outline-offset: 3px;`
This is always visible — never `outline: none` without an equivalent alternative.

**Skip link:** First focusable element in `<body>` is a "Skip to main content" link, visually hidden until focused (using clip/translate transform, not `display:none`). On focus: slides into view at top of page — background `--accent-primary`, text white, padding `--space-sm --space-md`, `--radius-md`. Activating it moves focus to `<main id="main-content">`.

**Tab order:** Follows DOM order, which matches visual order. No `tabindex` values other than 0 and -1. Negative tabindex used only for: items in closed menus, non-interactive slider items.

**Roving tabindex:** Used inside radio groups and the progress stepper to allow arrow key navigation between options. Enter/Space activates the focused option.

---

# 5. Responsive Behavior

## 5.1 Breakpoints

| Name | Min-width | Notes |
|---|---|---|
| Mobile (default) | 0px | Single column, stacked layouts, touch targets |
| Tablet | 640px | Two-column possible for simple forms |
| Desktop-sm | 1024px | Full navigation, multi-column layouts |
| Desktop | 1280px | Max-width containers kick in |
| Wide | 1536px | No changes beyond 1280px — content doesn't grow wider |

**Container max-widths:**
- Narrow (text content): max-width 700px
- Standard: max-width 1100px
- Wide: max-width 1280px

All containers: `width: 100%; margin: 0 auto; padding: 0 var(--space-lg);` — horizontal padding 24px on mobile, 40px on desktop.

---

## 5.2 Layout Changes by Breakpoint

### Navigation
- **0–1023px:** Logo left, theme toggle + hamburger right. No visible nav links.
- **1024px+:** Full horizontal nav with links center, Register CTA right.

### Hero
- **0–639px:** Display font size reduces to 2.5rem. Subheadline reduces to `--text-body`. CTA buttons stack vertically (full width).
- **640–1023px:** Display font 3.5rem. CTA buttons side by side.
- **1024px+:** Full 4.5rem display, full layout.

### Registration Cards (Home)
- **0–767px:** Single column, cards full width.
- **768–1023px:** Two columns (Attendee + Presenter, then Volunteer full-width below).
- **1024px+:** Three columns.

### Event Info Strip
- **0–767px:** Stacked vertical list, no dividers.
- **768px+:** Horizontal row with vertical dividers.

### About Page
- **0–767px:** Single column throughout.
- **768px+:** Two-column for "What is Skepticamp" section and About Teaser on home.

### Contact Page
- **0–1023px:** Single column (form full width, sidebar below).
- **1024px+:** Two-column (form 60%, sidebar 40%).

### Wizard Shell
- **0–639px:**
  - Progress stepper collapses to "Step X of Y" + linear progress bar
  - Wizard card has no padding-x beyond the container padding
  - Navigation buttons: Back (full width, secondary) above Continue (full width, primary), stacked
- **640px+:** Full step indicators, side-by-side navigation buttons.

### Confirmation Page
- **0–639px:** Vertical padding reduced to `--space-2xl`. Confirmation card is full width.
- **640px+:** Max-width 600px, centered.

### Footer
- **0–767px:** Three columns stack into single column, each section headed by its column title in `--text-label --text-muted`.
- **768px+:** Three-column grid.

---

# 6. Dark Mode vs. Light Mode

## 6.1 Dark Mode Feel and Mood

Dark mode is the **primary, designed-first experience**. The mood is: observatory at night. Deep midnight blues, precisely calibrated glow effects, and a sense of depth created through layered surfaces. It feels like looking at the universe through a telescope — focused, vast, precise, thrilling.

Key dark mode characteristics:
- Surfaces are not black — they're deep navy blue (`#0D0F1A` base), which reads as "rich dark" rather than "void"
- Cards and panels are lighter shades of the same blue, creating a layered atmosphere rather than flat dark gray boxes
- Accent colors glow — the primary `#4FAAFF` has genuine luminosity on dark backgrounds (achieved via `--shadow-glow-primary` on hover states)
- Typography is cream-white (`#E8ECF4`), not pure white — which would be harsh
- The hero's radial gradient decorations suggest the glow of distant lights or nebulae
- The dot constellation on the home page About teaser glows faintly via a `filter: blur(1px)` on the lit dots
- Borders are barely visible — `rgba(255,255,255,0.08)` — surfaces feel carved from space, not boxed in
- Shadows have slight blue tints for realism (dark surfaces don't cast warm brown shadows)

## 6.2 Light Mode Feel and Mood

Light mode is: a well-lit lecture hall. Warm off-white (`#F5F4F0` — a deliberate warm tint rather than blue-white) suggests printed paper and natural light. It's clean, serious, and credible without being clinical.

Key light mode characteristics:
- The page background `#F5F4F0` is warm — a 5% warm tint relative to pure white. Cards (`#FFFFFF`) lift cleanly off this background with minimal shadow.
- Shadows are soft and neutral (`rgba(0,0,0,0.08)`) — no color, no drama. Elevation is communicated through shadow size, not color.
- Accent blue `#1A6FD4` is a classic scientific blue — deep, trustworthy, ink-on-page. No glow effects in light mode (glows look garish on light backgrounds).
- Typography `#111827` is near-black, readable, authoritative.
- The hero gradient is extremely subtle — barely perceptible tints of indigo and violet at the edges. Light mode hero feels like a sunny afternoon scientific journal.
- The About teaser dot constellation: in light mode, the accent dots are filled solid `--accent-primary` and `--accent-secondary` — no glow, just clean geometric dots.

## 6.3 Elements That Change Beyond Color Swaps

1. **Shadows:** Dark mode uses glow shadows (colored, outward-radiating). Light mode uses drop shadows (neutral, directional). Not just a color swap — the shadow technique changes entirely.

2. **Hero background:** Dark mode has visible radial gradient "nebula" orbs. Light mode replaces these with an extremely low-opacity tinted wash that is barely visible — the hero feels "airy" not "atmospheric."

3. **Card borders:** Dark mode relies on `rgba(255,255,255,0.08)` borders as the primary card definition mechanism. Light mode reduces the border to almost nothing (`rgba(0,0,0,0.05)`) because the shadow + white background already separate the card from the page background.

4. **Elevated card top-edge gradient:** Only present in dark mode (simulates light hitting the top edge from above). Removed in light mode — it would look unnatural.

5. **Focus rings:** Dark mode focus ring is `#4FAAFF` (bright electric blue — visible against dark). Light mode focus ring is `#1A6FD4` (deeper blue — WCAG contrast compliant against white backgrounds).

6. **Text gradient on display heading:** "Knowledge" in the hero uses `--gradient-accent`. In dark mode this is vivid (bright blue to violet on dark). In light mode it's the same gradient but slightly muted — both colors are darker, so it reads as a color accent rather than a neon effect.

---

# 7. The WOW Factor

## 7.1 Hero Text Gradient with Parallax Shift

The word "Knowledge" in the hero headline — rendered with a CSS `background-clip: text` gradient — slowly shifts its gradient position on mouse movement (on desktop) or on scroll (on mobile). Using `mousemove` event, the gradient's `background-position` shifts by up to ±15% as the cursor moves across the screen. At rest it shows the default gradient. This creates a subtle "alive" feeling — the text seems to refract light.

**Implementation:** JavaScript `mousemove` listener updates a CSS custom property `--gradient-shift` (range: -15% to 15%). The gradient is defined as `background-position: calc(50% + var(--gradient-shift)) center`. Throttled with `requestAnimationFrame`. On `prefers-reduced-motion`, the shift is disabled entirely.

---

## 7.2 Registration Card 3D Tilt Effect

The three registration type cards on the home page respond to mouse hover with a gentle 3D tilt using CSS `perspective` and `transform: rotateX() rotateY()`. As the cursor moves over a card, the card tilts toward the cursor position — maximum tilt ±6°. The card's accent glow (box-shadow) shifts its blur radius and position to simulate a light source following the cursor.

**Implementation:**
- Parent container: `perspective: 1000px`
- Card: `transform-style: preserve-3d; will-change: transform`
- On `mousemove`: calculate cursor position relative to card center, map to ±6° for X and Y rotation
- On `mouseleave`: animate back to flat via `transition: transform 500ms --ease-out`
- On `prefers-reduced-motion`: only the shadow shifts (no tilt transform)
- WCAG: no functional information conveyed by the tilt — purely decorative

---

## 7.3 The Drawing Checkmark Confirmation

On the registration confirmation page, the success checkmark SVG draws itself via `stroke-dashoffset` animation (see Section 3.4, Confirmation Page). This is not new technology — but executed precisely it creates a moment of genuine delight.

**The extra touch:** After the checkmark finishes drawing (at ~600ms), a subtle particle burst emits from the checkmark's center — 8 small dots (4px each) in `--accent-primary` and `--state-success`, animated outward radially using `transform: translateX() translateY()` and `opacity: 0`, over 500ms with `--ease-out`. The dots then fade out. This is pure CSS with 8 `<span>` elements and keyframe animations.

**On `prefers-reduced-motion`:** Checkmark is fully visible immediately (no draw animation, no particles). Still delightful because the circle scale-in uses `--duration-instant`.

---

## 7.4 The "Constellation" Dot Grid — Interactive

The CSS dot grid on the About teaser section (home page) and on the About page becomes subtly interactive: as the cursor moves near a dot (within ~60px), that dot scales up from 1 to 1.5 and briefly brightens (`filter: brightness(1.8)`). The effect ripples to adjacent dots at 30ms delays. When the cursor leaves, all dots return to baseline.

**Implementation:** Each dot is a `<span>` element. A single `mousemove` listener on the grid container calculates the cursor's distance from each dot's center. Dots within range get a CSS class added; the class drives `transform: scale(1.5)` and `filter: brightness(1.8)` via `transition`. Distance-based delay is set via inline `transition-delay` style.

On mobile: the dots pulse gently on a randomized interval (each dot independently, 2–5 second intervals, scale 1 → 1.3 → 1, `--ease-bounce`). This maintains the "alive" feeling on touch devices.

---

## 7.5 The Progress Stepper "Fill" on Advance

When the user clicks "Continue" in the wizard, the following sequence happens in ~1 second total, making progress feel earned and physical:

1. **(0ms)** The connector line between the current step and the next step begins filling from left to right (width transition from 0% to 100%, `--duration-slow --ease-out`).
2. **(200ms)** The current step's circle begins transitioning: the number fades out, the background fills to `--accent-primary`, and a checkmark SVG draws itself (stroke-dashoffset, 200ms).
3. **(350ms)** The next step's circle "pulses" once — scale 1 → 1.15 → 1 over `--duration-default --ease-bounce` — and its border transitions to `--accent-primary`.
4. **(400ms)** The step content begins its horizontal slide transition (Section 4.2).

This sequenced micro-animation communicates progress, success, and forward momentum simultaneously. It transforms a dry form wizard into something that feels rewarding to complete.

---

*End of Skepticamp NYC Design Specification v1.0*
*Questions: reference CLAUDE.md for stack and architecture decisions.*
