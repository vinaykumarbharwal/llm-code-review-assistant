# design.md — Lumeo AI Assistant

**Version:** 1.0.0 · **Platform:** Web + Mobile · **Theme:** Dark-first · **Status:** Active

---

## 1. Design Philosophy

Lumeo's interface is built around one idea: **the AI should feel like a calm, trusted colleague — not a chatbot.**

Every visual decision flows from three principles:

**Recede until needed.** The UI stays out of the way. No aggressive CTAs, no banner noise, no color fireworks. The chrome disappears; only the content and conversation remain.

**Dark as default, not an afterthought.** The dark palette isn't a mode toggle — it's the primary canvas. Deep indigo-blacks create a focused workspace that reduces eye strain during long sessions.

**Motion earns its place.** No animation exists for decoration. Every transition orients the user (where did I come from, where am I going) or confirms an action (the message was sent, the task was saved).

---

## 2. Brand Identity

### Name & Logo

- **Product name:** Lumeo
- **Tagline:** Your workflow, simplified.
- **Logo mark:** A compact circle or orb icon rendered as a gradient from Violet → Teal, set in a softly rounded square container (8px radius). Represents the AI "core" — glowing, intelligent, contained.
- **Wordmark:** Set in Syne 700. Letter-spacing: -0.01em. Never stretched, never outlined.

### Voice & Tone

The AI speaks like a sharp, warm colleague. Short sentences. No filler. It leads with the answer, then explains if asked.

| Situation | Lumeo says | Not |
|-----------|-----------|-----|
| Task complete | "Done. Moved to archive." | "I have successfully completed the requested operation!" |
| Missing info | "Which project — Design or Eng?" | "I'm sorry, I need more information to proceed." |
| Error | "Couldn't reach your calendar. Try again?" | "An unexpected error has occurred. Please retry." |

---

## 3. Color System

### Palette Overview

Lumeo uses a focused 8-color palette. **Violet is the only true accent color.** All other colors are semantic — they communicate state, not decoration.

```
Void          #0D0D10   App background
Surface       #17171F   Cards, panels, modals
Surface Hi    #1E1E28   Hover states, active items
Glass         rgba(255,255,255,0.04)   Subtle overlays

Violet        #7C6FF7   Brand, CTAs, active nav, focus rings
Violet Soft   rgba(124,111,247,0.15)   User message bubbles, tints
Teal          #3ECFB2   AI identity, success states, gradient pair
Teal Soft     rgba(62,207,178,0.12)    AI tints

Text Primary    #F0EFFE   Headings, labels, values
Text Secondary  #9997B8   Body text, descriptions
Text Tertiary   #5C5A7A   Timestamps, metadata, placeholders

Border          rgba(255,255,255,0.07)   Default separators
Border Hi       rgba(255,255,255,0.12)   Focused inputs, active cards

Success   #5CCE8F   Completed tasks, confirmed actions
Warning   #F5B94E   Pending, in-progress, needs attention
Danger    #F06B6B   Errors, destructive actions, overdue
```

### Color Rules

1. **Violet is interactive.** Only use `#7C6FF7` on elements the user can interact with — buttons, active nav items, links, focus rings. Never use it as a background decoration.

2. **Teal is the AI's color.** The AI avatar, typing indicator, and AI-sourced result highlights all use teal. This creates an immediate visual grammar: violet = you, teal = Lumeo.

3. **Semantic colors are binary.** Success is `#5CCE8F`. Warning is `#F5B94E`. Danger is `#F06B6B`. No intermediate shades. Never use them for non-semantic purposes (e.g., don't use success green as a decorative accent on a card).

4. **Gray text, never black.** On the dark canvas, pure white creates harsh contrast. `#F0EFFE` (with a slight violet undertone) reads as "primary" while feeling native to the dark palette.

### Gradient Usage

The Lumeo logo and AI avatar use the only approved gradient:

```css
background: linear-gradient(135deg, #7C6FF7 0%, #3ECFB2 100%);
```

This gradient is **never used as a background** for content areas. Only for the logo mark, AI avatar, and the send button on focus.

---

## 4. Typography

### Font Stack

```
Display / Headings:   Syne (Google Fonts)
UI / Body:            DM Sans (Google Fonts)
Mono / Code / Meta:   DM Mono (Google Fonts)
```

**Why Syne?** It's geometric and confident without being cold. The slight idiosyncrasies in letterforms give Lumeo's headings personality — it reads as "designed," not "defaulted."

**Why DM Sans?** Humanist, neutral, and exceptionally readable at 13–16px on dark backgrounds. Paired with Syne it creates tension between expressive display and functional body.

### Type Scale

| Role | Font | Size | Weight | Line Height | Letter Spacing |
|------|------|------|--------|-------------|----------------|
| Display | Syne | 48px | 800 | 1.05 | -0.02em |
| H1 | Syne | 32px | 700 | 1.1 | -0.02em |
| H2 | Syne | 24px | 700 | 1.2 | -0.01em |
| H3 | Syne | 18px | 600 | 1.3 | -0.01em |
| Label / Button | DM Sans | 14px | 500 | 1.0 | 0 |
| Body | DM Sans | 15px | 400 | 1.75 | 0 |
| Body Small | DM Sans | 13px | 400 | 1.65 | 0 |
| Mono / Meta | DM Mono | 12px | 400 | 1.5 | +0.04em |

### Usage Rules

- **Never use Syne below 16px.** The geometric letterforms lose legibility at small sizes.
- **Body text is always `#9997B8`** (Text Secondary). Only labels, values, and headings use `#F0EFFE` (Text Primary).
- **Timestamps and metadata always use DM Mono** — this gives them a subtle "data" feel that distinguishes them from UI labels.
- **Two weights in body text only: 400 and 500.** Bold (600+) is reserved for display and H1/H2 headings.

---

## 5. Spacing & Layout

### Base Unit

All spacing is built on a **4px base unit**. All values are multiples of 4.

```
xs    4px    Icon gaps, badge padding
sm    8px    Inline element spacing
md   12px    Component internal padding (tight)
lg   16px    Component internal padding (standard)
xl   24px    Between components
2xl  32px    Section gaps
3xl  48px    Page-level rhythm
4xl  64px    Hero / section breathing room
```

### Grid System

| Breakpoint | Columns | Gutter | Margin |
|------------|---------|--------|--------|
| Mobile `< 768px` | 4 | 16px | 20px |
| Tablet `768–1024px` | 8 | 20px | 32px |
| Desktop `1024–1440px` | 12 | 24px | 48px |
| Wide `> 1440px` | 12 | 24px | auto (max-width: 1080px) |

### Layout Structure (Desktop)

```
┌─────────────────────────────────────────────────────────┐
│  Sidebar 240px  │  Chat Area (flex-1)  │  Panel 280px  │
│                 │                      │  (optional)   │
│  fixed          │  scrollable          │  collapsible  │
└─────────────────────────────────────────────────────────┘
```

The sidebar collapses to **56px (icon-only mode)** via a toggle. The right panel is hidden by default and slides in contextually when the AI returns a structured result.

### Layout Structure (Mobile)

Sidebar becomes a **bottom tab bar** (4 tabs: Chat, Browse, Timeline, Tasks). The right panel becomes a **full-screen bottom sheet** that slides up on trigger.

---

## 6. Component Specifications

### 6.1 Navigation Sidebar

```
Width:            240px (expanded) / 56px (collapsed)
Background:       #101015 (slightly darker than app bg)
Padding:          16px
Logo zone height: 56px

Nav item height:  36px
Nav item radius:  8px
Nav item padding: 9px 10px

Active state:
  background:     rgba(124,111,247,0.15)
  border-left:    2px solid #7C6FF7
  text color:     #C4BCF9

Hover state:
  background:     rgba(255,255,255,0.04)
  transition:     120ms ease-out

Section labels:
  font:           DM Mono 10px
  color:          #5C5A7A
  text-transform: uppercase
  letter-spacing: 0.1em
  margin-bottom:  6px
```

### 6.2 Chat Bubbles

**User message:**
```
Alignment:        right
Max width:        68% of chat area
Background:       rgba(124,111,247,0.15)
Border:           1px solid rgba(124,111,247,0.25)
Border radius:    16px 16px 4px 16px
Padding:          12px 16px
Font:             DM Sans 14px / Text Primary
```

**AI message:**
```
Alignment:        left, with 32px avatar
Max width:        76% of chat area
Background:       #17171F
Border:           1px solid rgba(255,255,255,0.12)
Border radius:    4px 16px 16px 16px
Padding:          14px 18px
Font:             DM Sans 14px / Text Secondary
Avatar:           32px circle, Violet→Teal gradient, "L" in Syne 700
```

### 6.3 Input Bar

```
Position:         sticky bottom of chat area
Background:       #17171F
Border:           1px solid rgba(255,255,255,0.12)
Border radius:    24px (pill)
Padding:          14px 18px
Height:           52px (single line) / auto (multi-line, max 120px)

Placeholder:      "Ask Lumeo anything..." / Text Tertiary / DM Sans 14px
Text:             Text Primary / DM Sans 14px

Send button:
  Width/Height:   34px circle
  Background:     #7C6FF7 (active) / rgba(124,111,247,0.3) (empty input)
  Icon:           Paper plane, 14px, white fill
  Transition:     background 150ms ease-out

Attachment button: 20px icon, Text Tertiary, appears left of send
Voice button:      20px icon, Text Tertiary, appears left of attachment
```

### 6.4 Result Cards

Result cards appear in the AI response stream or the right panel. They carry structured data back from Lumeo's tools.

```
Background:       #17171F
Border:           1px solid rgba(255,255,255,0.07)
Border radius:    12px
Padding:          20px
Max width:        480px

Header row:
  Title:          DM Sans 13px / 500 / Text Primary
  Tag/Badge:      DM Mono 11px / semantic color bg + text / border-radius 20px

List item row:
  Height:         38px
  Background:     rgba(255,255,255,0.04)
  Border:         1px solid rgba(255,255,255,0.07)
  Border radius:  8px
  Padding:        10px 12px
  Status icon:    18px circle (success green or pending gray)
  Text:           DM Sans 13px / Text Secondary
```

### 6.5 Badges & Tags

```
Font:             DM Mono 11px / 500
Padding:          3px 8px
Border radius:    20px (pill)

Variants:
  success   bg: rgba(92,206,143,0.12)   text: #5CCE8F
  warning   bg: rgba(245,185,78,0.12)   text: #F5B94E
  danger    bg: rgba(240,107,107,0.12)  text: #F06B6B
  neutral   bg: rgba(255,255,255,0.06)  text: #9997B8
  violet    bg: rgba(124,111,247,0.15)  text: #A99DF5
```

### 6.6 AI Typing Indicator

```
Three dots in a row, 6px each, 4px gap
Color:            #3ECFB2 (Teal)

Animation (per dot):
  Keyframes: scale 1.0 → 1.35 → 1.0 + opacity 0.5 → 1.0 → 0.5
  Duration:  600ms, ease-in-out, infinite
  Stagger:   dot-2 delays 120ms, dot-3 delays 240ms

ARIA:             role="status" aria-label="Lumeo is typing"
```

### 6.7 Floating Widget

```
Size:             320px × 480px
Position:         fixed, bottom-right, 24px margin
Background:       #17171F
Border:           1px solid rgba(255,255,255,0.12)
Border radius:    20px
Box shadow:       0 24px 48px rgba(0,0,0,0.6), 0 0 0 1px rgba(124,111,247,0.1)

Header:           40px, logo + "Lumeo" + minimize button
Content:          Top-3 priority items (result card, compact variant)
Input:            Mini input bar, same spec as 6.3 but 44px height
Expand trigger:   "Open full view →" link at bottom, Text Tertiary 12px

Toggle shortcut:  ⌘+L (Mac) / Ctrl+L (Win)
Enter animation:  slide-up 12px + fade, 280ms spring ease
Exit animation:   fade + scale to 0.95, 180ms ease-in
```

---

## 7. Icon System

**Library:** Feather Icons (outline style)  
**Stroke:** 2px, round linecap and linejoin  
**Default size:** 18px  
**Color:** Always inherits from semantic context — never hardcoded

| Icon | Name | Context |
|------|------|---------|
| `message-square` | Chat | Nav — Chat Assistant |
| `search` | Browse | Nav — Browse / Search |
| `calendar` | Timeline | Nav — Timeline |
| `check-square` | Tasks | Nav — Tasks |
| `mail` | Email | Nav — Email |
| `send` | Send | Input bar send button |
| `paperclip` | Attach | Input bar attachment |
| `mic` | Voice | Input bar voice input |
| `check-circle` | Done | Task / result status |
| `clock` | Pending | Task / result status |
| `alert-circle` | Error | Error states |
| `chevron-right` | Expand | Collapsible sections |
| `x` | Close | Modals, widget dismiss |
| `minimize-2` | Minimize | Widget header |

**Icon sizing rules:**
- Nav icons: 18px
- Input bar icons: 18px
- Status icons in result cards: 16px
- Decorative/empty state icons: 40px (with 10% opacity background circle)

---

## 8. Screen Designs

### S1 — Main Chat Screen

The primary screen. Users land here by default.

**Layout:**
```
[Sidebar 240px] | [Chat header 56px] 
                | [Message history — scrollable flex column]
                | [Typing indicator — conditionally rendered]
                | [Input bar — sticky bottom]
```

**Chat header:** User's name + greeting ("Good morning, Alex"), today's date in DM Mono, and a three-dot overflow menu (Settings, Export, Keyboard shortcuts).

**Empty state:** When no conversation exists, show three quick-start chips centered in the chat area: "Summarize my emails", "What's on my calendar?", "Show me my tasks". Chips styled as ghost buttons with violet border.

**Scroll behavior:** Messages scroll freely. Input bar never scrolls. When the user sends a message, auto-scroll to the bottom. A "scroll to bottom" FAB (24px, violet) appears when the user has scrolled up more than 2 message heights.

### S2 — Browse Screen

AI-assisted web browsing and search.

**Layout:**
```
[Large search input — full width, 56px height]
[AI summary bubble — pinned below search, collapsible]
[Results grid — 3 col desktop, 2 tablet, 1 mobile]
```

Each result card shows: favicon (16px), source domain, title (Syne 15px / 600), excerpt (2 lines max, DM Sans 13px / Secondary), and timestamp (DM Mono 11px).

The AI summary bubble uses the AI message bubble style but spans full width, with a teal left border accent (3px).

### S3 — Timeline & Planning

Unified view of tasks and calendar.

**Layout:**
```
[AI digest banner — "Here's what matters today", collapsible]
[Horizontal timeline bar — today's time blocks, 64px height]
[Two-column below: Task list left | Calendar day view right]
```

Timeline bar: Each event is a colored pill (height 100%, width proportional to duration). Color: violet for meetings, teal for focus time, amber for deadlines. Overflow events collapse into a "+N more" indicator.

Task list items have a checkbox (16px circle), task name, optional due time, and a drag handle (visible on hover). Drag-and-drop triggers an AI confirmation: "Move 'Design review' to 2pm?" with Accept/Cancel chips.

### S4 — Result Detail Screen

Displays when the AI returns a rich single result (an email, document, or search result).

**Layout:**
```
[Breadcrumb ← Back to chat]
[Split view: Left 55% AI summary + actions | Right 45% source content]
```

Left panel: AI-generated summary in a clean card, followed by action chips (primary action in violet, secondary in ghost style). Examples: "Reply", "Archive", "Create Task", "Reschedule".

Right panel: Raw source rendered in a scrollable frame with a subtle inner border. Font size bumped to 14px for readability. If the source is an email: shows From, To, Subject header row in DM Mono.

### S5 — Floating Widget

See Component Spec 6.7. Design notes:

The widget header gradient bar (2px height, full width, Violet→Teal) gives it a distinctive, premium feel and visually connects it to the brand logo. No other surface uses this gradient bar.

---

## 9. Motion & Animation

### Principles

1. **Ease-out always.** Elements arrive fast and settle slow. This reads as responsive and confident. Never use linear or ease-in for UI transitions.

2. **One orchestrated reveal.** On page load, all elements fade up with staggered delays — not independently on scroll. The whole page "breathes in" together.

3. **Spring for personality.** The message bubble pop-in and widget entrance use a spring curve `cubic-bezier(0.34, 1.56, 0.64, 1)` — it overshoots slightly, which reads as alive.

### Timing Tokens

```css
--ease-fast:    80ms  ease-out;                         /* Icon changes, badge updates */
--ease-base:    180ms cubic-bezier(0.2, 0, 0, 1);      /* Hover states, card entry */
--ease-slow:    280ms cubic-bezier(0.2, 0, 0, 1);      /* Page transitions, modal open */
--ease-spring:  320ms cubic-bezier(0.34, 1.56, 0.64, 1); /* Bubbles, widget, FAB */
```

### Interaction Animations

**Page load (staggered, all fire once):**
```
0ms   — Sidebar fades in (opacity 0→1, y 0→0)
60ms  — Chat history slides up (y +20px→0, opacity 0→1)
120ms — Input bar fades in
Duration: 280ms / ease-out
```

**Message send:**
```
User bubble: scale 0.92→1.0, opacity 0→1, 180ms spring
Input clear: content fades out 80ms
AI typing indicator: appears after 200ms delay
```

**AI response arrive:**
```
AI bubble: y +12px→0, opacity 0→1, 220ms ease-out
If result card: same, but staggered at +40ms per card
```

**Nav switch (cross-fade, no slide):**
```
Outgoing: opacity 1→0, 120ms ease-in
Incoming: opacity 0→1, 200ms ease-out
```

**Widget toggle:**
```
Enter: y +16px→0, opacity 0→1, scale 0.95→1, 280ms spring
Exit:  opacity 1→0, scale 1→0.95, 180ms ease-in
```

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

All motion is purely visual enhancement. No information is conveyed exclusively through animation.

---

## 10. Accessibility

### Target Standard

WCAG 2.1 Level AA compliance across all screens and states.

### Contrast Ratios

| Combination | Ratio | Pass |
|-------------|-------|------|
| `#F0EFFE` on `#0D0D10` | 16.8:1 | AA + AAA |
| `#9997B8` on `#0D0D10` | 5.2:1 | AA |
| `#9997B8` on `#17171F` | 4.8:1 | AA |
| `#7C6FF7` on `#0D0D10` | 4.6:1 | AA (large text) |
| `#A99DF5` on `#0D0D10` | 7.1:1 | AA + AAA |

### Keyboard Navigation

- All interactive elements reachable via `Tab`
- Logical focus order matches visual order
- Focus ring: `2px solid #7C6FF7` with `2px offset` — never `outline: none` without a custom replacement
- `Escape` closes modals, sheets, and the widget
- `⌘+L` / `Ctrl+L` toggles the floating widget
- Arrow keys navigate within result card lists

### Screen Reader Requirements

```
AI typing indicator:  role="status" aria-live="polite" aria-label="Lumeo is typing"
Chat messages:        role="log" aria-label="Conversation"
Each message:         role="article" with aria-label="[You / Lumeo]: [first 80 chars]"
Send button:          aria-label="Send message"
Icon-only buttons:    aria-label describing the action
Sidebar nav:          role="navigation" aria-label="Main navigation"
```

### Focus Management

When the AI response arrives, focus stays on the input bar — never auto-moves to the response. When a modal opens, focus moves to the modal's first focusable element. When it closes, focus returns to the trigger element.

---

## 11. Design Tokens (CSS)

The single source of truth. Import this file; never hardcode values.

```css
/* lumeo-tokens.css */

:root {
  /* ── Backgrounds ── */
  --lm-bg-void:         #0d0d10;
  --lm-bg-surface:      #17171f;
  --lm-bg-raised:       #1e1e28;
  --lm-bg-sidebar:      #101015;
  --lm-bg-glass:        rgba(255, 255, 255, 0.04);

  /* ── Brand Colors ── */
  --lm-violet:          #7c6ff7;
  --lm-violet-soft:     rgba(124, 111, 247, 0.15);
  --lm-violet-border:   rgba(124, 111, 247, 0.25);
  --lm-teal:            #3ecfb2;
  --lm-teal-soft:       rgba(62, 207, 178, 0.12);
  --lm-gradient:        linear-gradient(135deg, #7c6ff7 0%, #3ecfb2 100%);

  /* ── Semantic ── */
  --lm-success:         #5cce8f;
  --lm-success-soft:    rgba(92, 206, 143, 0.12);
  --lm-warning:         #f5b94e;
  --lm-warning-soft:    rgba(245, 185, 78, 0.12);
  --lm-danger:          #f06b6b;
  --lm-danger-soft:     rgba(240, 107, 107, 0.12);

  /* ── Text ── */
  --lm-text-1:          #f0effe;
  --lm-text-2:          #9997b8;
  --lm-text-3:          #5c5a7a;

  /* ── Borders ── */
  --lm-border:          rgba(255, 255, 255, 0.07);
  --lm-border-hi:       rgba(255, 255, 255, 0.12);

  /* ── Radius ── */
  --lm-radius-xs:       4px;
  --lm-radius-sm:       8px;
  --lm-radius-md:       12px;
  --lm-radius-lg:       18px;
  --lm-radius-xl:       24px;

  /* ── Spacing ── */
  --lm-space-xs:        4px;
  --lm-space-sm:        8px;
  --lm-space-md:        12px;
  --lm-space-lg:        16px;
  --lm-space-xl:        24px;
  --lm-space-2xl:       32px;
  --lm-space-3xl:       48px;
  --lm-space-4xl:       64px;

  /* ── Typography ── */
  --lm-font-display:    'Syne', sans-serif;
  --lm-font-ui:         'DM Sans', sans-serif;
  --lm-font-mono:       'DM Mono', monospace;

  /* ── Motion ── */
  --lm-ease-fast:       80ms ease-out;
  --lm-ease-base:       180ms cubic-bezier(0.2, 0, 0, 1);
  --lm-ease-slow:       280ms cubic-bezier(0.2, 0, 0, 1);
  --lm-ease-spring:     320ms cubic-bezier(0.34, 1.56, 0.64, 1);

  /* ── Shadows ── */
  --lm-shadow-widget:   0 24px 48px rgba(0, 0, 0, 0.6),
                        0 0 0 1px rgba(124, 111, 247, 0.1);
  --lm-shadow-modal:    0 32px 64px rgba(0, 0, 0, 0.7);
  --lm-shadow-card:     0 4px 16px rgba(0, 0, 0, 0.3);

  /* ── Layout ── */
  --lm-sidebar-width:   240px;
  --lm-sidebar-collapsed: 56px;
  --lm-panel-width:     280px;
  --lm-chat-max-width:  1080px;
}
```

---

## 12. Figma File Structure

```
Lumeo Design System v1
├── 🎨 Foundations
│   ├── Colors         (all tokens as Figma Variables)
│   ├── Typography     (text styles for all 8 scale entries)
│   ├── Spacing        (layout grids + spacing styles)
│   └── Shadows        (effect styles)
├── 🧩 Components
│   ├── Navigation     (Sidebar — expanded, collapsed, mobile tabs)
│   ├── Chat           (User bubble, AI bubble, Input bar, Typing indicator)
│   ├── Cards          (Result card, Task item, Email item, Search result)
│   ├── Badges         (All 5 variants)
│   ├── Buttons        (Primary, Ghost, Icon-only, Chip)
│   └── Widget         (Floating widget — collapsed, expanded)
├── 📱 Screens
│   ├── S1 Chat        (Desktop, Tablet, Mobile)
│   ├── S2 Browse      (Desktop, Mobile)
│   ├── S3 Timeline    (Desktop, Mobile)
│   ├── S4 Result      (Desktop, Mobile)
│   └── S5 Widget      (Desktop only)
└── 📐 Prototypes
    ├── Chat flow
    ├── Widget toggle
    └── Mobile tab navigation
```

All components use **Figma Variables** (not styles) so that color and spacing tokens auto-update across the entire file when changed at the token level.

---

## 13. Handoff Checklist

Before marking any screen ready for development:

- [ ] All colors use token names, zero hardcoded hex values
- [ ] All spacing values are multiples of 4px
- [ ] All interactive states designed: default, hover, focus, active, disabled
- [ ] Dark mode tested (the only mode, but verify no light bleed)
- [ ] Mobile breakpoint designed for all screens
- [ ] Empty states designed for all data-driven components
- [ ] Error states designed for all async operations
- [ ] Loading states designed (skeleton screens preferred over spinners)
- [ ] Accessibility annotations added (ARIA roles, focus order, alt text)
- [ ] Motion specs documented in component notes
- [ ] Dev mode redline enabled in Figma with all specs visible

---

*Lumeo Design System — maintained by Barly Design / Uxerflow*  
*Questions: reference the Figma file or open a design review request*
