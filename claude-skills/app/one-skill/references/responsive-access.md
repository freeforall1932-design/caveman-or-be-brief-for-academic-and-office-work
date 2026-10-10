# Reflow and real people — mobile layout, accessibility

**Read this when:** breakpoints, overflow, tap targets, contrast, keyboard, focus, states

**Layer:** antislop-layoutmobile + antislop-human

Loaded on demand: the always-on rules live in the skill's `SKILL.md`. The
bodies below are upstream text carried verbatim, with the per-section
provenance and every declared edit listed in `SOURCES.md` beside this file.

| section | from | load |
|---|---|---|
| [antislop-human — contrast, keyboard, focus, states](#antislop-human-contrast-keyboard-focus-states) | `anti-slop` | always |
| [antislop-layoutmobile — breakpoints, scale, grids, overflow, tap targets](#antislop-layoutmobile-breakpoints-scale-grids-overflow-tap-targets) | `anti-slop` | always |

---

## antislop-human — contrast, keyboard, focus, states

> `anti-slop` / `antislop-human` / any shipped interface, before review is complete

> **Merge note.** The contrast checker no longer sits next to a standalone SKILL.md: it is carried at `scripts/contrast-check.py` inside this skill, which is what the command below resolves to.

> Anti Slop: Rules for AI Coding Agents. Human skill

> Part of the antislop system. Read together with `antislop.md` (the core). This skill deep-dives the human concern: the UI must stay usable by people with different eyes, hands, and setups. Contrast, keyboard, focus, states, and the mobile details that exclude people.

### How to use this skill

- Load together with `antislop.md` whenever the task builds or edits UI. The core holds the mechanism (the purpose test, the three tiers, the Delivery Gate); this skill holds the human-side depth: the parts of a UI that exclude people with different eyes, hands, and setups.
- Every entry has the same shape: **Tell** (the pattern), **Why** (who it excludes, and why it reads as unfinished), **Fix** (what to do instead), with the governing core rule cited as R-XX.
- Accessibility is not a checklist of extras bolted on at the end. It is part of the core promise that "the UI holds up" (C-4). The Delivery Gate in the core remains the gate; the "Human Skill Checklist" at the end of this file is the supplement to run alongside it.
- The contrast checker (formula + reference table + script) lives in this skill. Use it for every color pairing you cannot verify by eye.
- This skill keeps only the mobile details that exclude people: zooming, and the on-screen keyboard.

### Color & Contrast

#### Low-Contrast Text

- **Tell:** light grey text on a white or near-white background, thin body text, muted labels chosen because they look "elegant" but are hard to read.
- **Why:** it excludes low-vision users and everyone in bright light. It is a visual choice made without checking the standard, which is exactly the kind of default the filter exists to catch.
- **Fix:** meet WCAG AA minimums (R-25): 4.5:1 for normal text, 3:1 for large text (18px+). Compute the ratio; do not eyeball it.

#### Text Over a Photo or Gradient

- **Tell:** white text placed directly over an image or gradient that is light in some areas, checked at one bright spot only.
- **Why:** contrast is local. Where the image is light, the text drops below 4.5:1 even if the hero still "looks" fine. R-25 requires testing the whole area the text passes over, not a single point.
- **Fix:** add a scrim or a solid color block behind the text, then verify the worst spot, not the best. If any part of the text area fails, the treatment fails.

#### The Grey-on-Grey Hallucination

- **Tell:** "dark grey on black" or "light grey on white" claimed to pass AA without a computation.
- **Why:** this is the most common accessibility hallucination. The eye overestimates contrast on grey pairs, and agents repeat the claim because it sounds plausible. #555555 on black is 2.8:1. It fails.
- **Fix:** never assert a pairing passes. Run the contrast checker (below) or apply the formula. When neither is possible, use the reference table.

#### Non-Text Contrast

- **Tell:** interactive components (buttons, icons, input borders, focus indicators, chart segments) distinguished from their background by less than 3:1.
- **Why:** non-text UI carries information by shape and edge. When the edge is a hair of tint, low-vision users cannot find the control. The same bar applies to states like hover and selected.
- **Fix:** give every component boundary and every status indicator a 3:1 ratio against adjacent colors (WCAG 1.4.11). Pair icons with a text label that meets 4.5:1.

#### The Contrast Checker

The home of the contrast checker. Three layers, from most to least convenient:

**The script.** When a script runtime is available and the file is present, run it instead of computing by hand. The script ships in this skill's folder (`scripts/contrast-check.py`, inside this skill). Run it with `python3` on macOS and Linux, `python` on Windows:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/contrast-check.py" "#FFFFFF" "#777777"
## normal text: FAIL (4.48 < 4.5)
## large text:  PASS (4.48 >= 3.0)
```

If the `${CLAUDE_SKILL_DIR}` variable is not available in this agent, point the script path at `scripts/contrast-check.py` inside this skill directly. The script exists so agents stop hallucinating AA. It takes two hex colors and prints the ratio and the verdict for both text sizes. If the file is missing, the formula and table below are complete on their own. Never block on the script.

**The formula (WCAG 2.x).**

1. Contrast ratio = (L1 + 0.05) / (L2 + 0.05), where L1 is the lighter relative luminance and L2 the darker.
2. Relative luminance L of one color: convert each channel to 0-1 (`c = hex / 255`), then linearize: if `c <= 0.03928`, `c_lin = c / 12.92`; otherwise `c_lin = ((c + 0.055) / 1.055)^2.4`.
3. `L = 0.2126*R + 0.7152*G + 0.0722*B`.
4. Round the ratio to two decimals and compare: 4.5:1 for normal text, 3:1 for large text (18px+, per R-25). The maximum ratio is 21.0 (black on white).

**The reference table** (common pairings, computed with the formula):

| Pairing (text on background) | Ratio | Normal text (4.5) | Large text (3.0) |
|------------------------------|-------|-------------------|------------------|
| Black on white | 21.00 | Pass | Pass |
| White on black | 21.00 | Pass | Pass |
| White on #333333 | 12.63 | Pass | Pass |
| White on #666666 | 5.74 | Pass | Pass |
| #777777 on white | 4.48 | Fail | Pass |
| White on #888888 | 3.54 | Fail | Pass |
| White on #999999 | 2.85 | Fail | Fail |
| #555555 on black | 2.82 | Fail | Fail |

Read the table as a sanity check, not as a substitute. Any pairing not listed, or anything near a threshold, goes through the formula or the script.

### Keyboard

#### Removed Focus Outline

- **Tell:** `outline: none` or `outline: 0` with no replacement focus style.
- **Why:** keyboard users cannot see where they are. It is the fastest way to make a UI unusable without a mouse, and R-32 forbids it outright.
- **Fix:** keep or replace the outline with a visible `:focus-visible` style that meets the same contrast bar (3:1 against its neighbors). Never set `outline: none` without a replacement.

#### Mouse-Only Patterns

- **Tell:** menus that open on hover only, dropdowns that click-open but do not keyboard-open, drag-and-drop with no keyboard fallback.
- **Why:** each one excludes keyboard and assistive-technology users (R-32). If a control cannot be reached and operated by Tab, Enter, or Space, it does not exist for a whole group of people.
- **Fix:** every interactive element is reachable and operable by keyboard (R-32): logical tab order following visual order, activation with Enter or Space, and dialogs closable with Escape (R-26).

#### Broken Tab Order

- **Tell:** focus jumps around the page, skips content, or lands on hidden elements because the DOM order does not match the visual order.
- **Why:** tab order that reads the code order instead of the visual order makes navigation unpredictable (R-32). Users lose their place and the page feels broken.
- **Fix:** keep the source order matching the visual order, add skip links for long pages, and never give real content `tabindex="-1"` unless it is part of a controlled focus trap such as a dialog.

### Focus & States

#### Weak or Invisible Focus Indicator

- **Tell:** a focus ring the same color as the background, a ring that only appears on hover, or an indicator thinner than a 1px border.
- **Why:** the focus indicator is how keyboard users know where they are. If it fails the contrast bar or only shows on hover, keyboard-only use breaks (R-32, R-34).
- **Fix:** a visible focus indicator on every interactive element, 3:1 against adjacent colors, in every theme you ship. Check it in dark and light mode.

#### Color-Only Feedback

- **Tell:** success, error, and status communicated only by color: red error text, green success border, a tinted chip, with no icon, label, or text.
- **Why:** it excludes color-blind and low-vision users, and it disappears entirely in forced-colors mode. A status that depends on seeing hue is not a status (C-4).
- **Fix:** pair every color signal with text, an icon, or a pattern. Error states are text first: "Password must be at least 8 characters", not just a red border.

#### Missing UI States

- **Tell:** a data view with no empty, loading, or error state, or states that exist but are invisible: a spinner with no text, an empty screen with no explanation.
- **Why:** R-27 requires the three states; the accessibility angle is that each must be perceivable and informative, not decorative. A loading spinner with no context reads as a frozen page to screen-reader users.
- **Fix:** every data view has all three states (R-27), each announced or visible: an explicit empty message, a loading state with text, and an error state that says what happened and how to proceed.

### Zoom & Mobile Use

The layout mechanics behind mobile (breakpoints, scale, grids, overflow, tap targets) are the concern of `antislop-layoutmobile`. This section keeps only the mobile details that exclude people: zooming, and the on-screen keyboard.

#### Text That Cannot Zoom

- **Tell:** fixed pixel font sizes, or containers with `overflow: hidden` that clip text at 200% zoom.
- **Why:** users must be able to resize text (WCAG 1.4.4). If zooming to 200% clips the content or forces horizontal scroll, the text is not resizable in practice.
- **Fix:** fluid type that reflows with zoom, no clipping containers on text, and verify the layout holds at 200% zoom on a narrow viewport (R-35).

#### Mobile Keyboard Covers the Form

- **Tell:** inputs at the bottom of the viewport hidden behind the on-screen keyboard, with no scroll-into-view and no room for the input.
- **Why:** a form the user cannot see or reach is a form they cannot complete. It is a mobile-only exclusion (R-03).
- **Fix:** when an input is focused, it scrolls into view above the keyboard, with enough bottom padding that the focused field is never covered. Test with a real device or an emulated keyboard.

### Human Skill Checklist

Run these alongside the core Delivery Gate when the task involves UI. All answers must be **yes**:

- [ ] Is every text and background pairing verified against the contrast checker (formula, table, or script), including text over images and gradients? (R-25)
- [ ] Does every interactive component boundary and status indicator meet 3:1 against its background? (non-text contrast)
- [ ] Is the focus indicator visible, high-contrast, and present on every interactive element in every theme? (R-32, R-34)
- [ ] Is every interactive element reachable and operable by keyboard, with dialogs closable via Escape and no `outline: none` without a replacement? (R-32, R-26)
- [ ] Are the empty, loading, and error states of every data view present and perceivable, not color-only? (R-27, C-4)
- [ ] Can text be resized to 200% without being clipped, and does the mobile keyboard never cover a focused input? (R-35)

## antislop-layoutmobile — breakpoints, scale, grids, overflow, tap targets

> `anti-slop` / `antislop-layoutmobile` / layout that has to reflow phone to desktop

> Anti Slop: Rules for AI Coding Agents. Mobile Layout skill

> Part of the antislop system. Read together with `antislop.md` (the core). This skill deep-dives the responsive layout concern: how a layout must reflow across screen sizes, phone to desktop. Breakpoints, scale, grids, overflow, tap targets, and navigation. It references core rules by number and never duplicates or renumbers them. Load it when the task builds or edits a layout that has to hold up at any screen width.

### How to use this skill

- Load together with `antislop.md` whenever the task is mobile or responsive layout work. The core holds the mechanism (the purpose test, the three tiers, the Delivery Gate); this skill holds mobile-layout depth.
- Every entry has the same shape: **Tell** (the pattern), **Why** (why it reads as slop), **Fix** (what to do instead), with the governing core rule cited as R-XX.
- The principle behind this skill: **mobile layout is a different layout, not the desktop layout at a smaller size.** It must reflow: re-stack, rescale, and re-order with intent. Every pattern below is a way a layout fails to reflow.
- The Delivery Gate in the core remains the gate. The "Layoutmobile Skill Checklist" at the end of this file is the mobile-specific supplement to run alongside it.

### Breakpoints

#### Desktop-Only Layout

- **Tell:** one layout state for every screen; the mobile view is the desktop layout squeezed into a phone.
- **Why:** R-03 requires a mobile layout that is perfect, not an afterthought. A page that only shrinks has no mobile design at all: cards that worked side by side overlap, and text meant for a wide canvas crowds into a narrow one.
- **Fix:** define a real mobile state at the breakpoint where the content stops working. The mobile layout reflows: columns stack, sizes drop, and order changes where the content needs it. If the mobile view is just the desktop view at a smaller width, the layout is not done.

#### Breakpoint Driven by Device List

- **Tell:** breakpoints named after phone widths (375px, 414px, 768px) chosen because "that is the iPhone size", not because the content breaks there.
- **Why:** device widths change every year and every model. A breakpoint is a point where the layout stops holding; forcing it to match a device list makes the layout follow a spec sheet instead of the content (R-03).
- **Fix:** place breakpoints where the content actually breaks: when a column stops being readable, when a row of cards gets too narrow. Test by narrowing the viewport and watching where it snaps, then set the breakpoint there.

#### Mobile Styled Last

- **Tell:** mobile rules bolted on as a trailing override: a long desktop stylesheet with a small media query at the end fixing one or two things.
- **Why:** an override patch is not a mobile design. It fixes the symptom that got reported and leaves the next one, and the base styles stay tuned for a wide screen (R-03).
- **Fix:** treat mobile as a designed state, not an override. Give the narrow viewport its own deliberate sizes and stacking, and verify the whole layout there, not just the patched spots (R-35).

#### Two-State Layout

- **Tell:** a layout with exactly two states: a single stacked column below one breakpoint, and a wide multi-column grid above it, with nothing defined in between. A tablet or small laptop width then inherits whichever state is closest: the phone stack stretched absurdly wide, or the desktop grid crammed into a fraction of its intended canvas.
- **Why:** a page is a continuous range of widths, and R-03 demands it hold up at every one of them, not just two chosen breakpoints. Two states leave the whole middle band of the range (roughly 600 to 1024 px, where tablets and small laptops live) as an accident: content that neither stacks with intent nor sits in a grid that fits. The layout reads as designed only at its two sample points and broken everywhere between.
- **Fix:** define real states at the widths where the content stops working, and let them be as many as the content needs. A typical reflow is three states, not two: single column, then a two-column grid when cards get too wide as a single stack, then the full multi-column grid only when it genuinely fits. Verify by dragging the viewport through the whole range, not by checking two widths and calling it done (R-35).

### Scale & Sizing

#### Desktop-Sized Everything

- **Tell:** padding, gaps, hero heights, and card sizes carried unchanged from desktop to mobile, so every section looks blown up on a phone.
- **Why:** an element sized for a 1440px canvas dominates a 375px one. What reads as confident on desktop becomes oversized on mobile: nothing fits, nothing breathes, and the page feels like it was designed for a screen that is not the one in hand (R-03). Spacing and type should follow the design rhythm (R-05), and that rhythm has a smaller register on mobile.
- **Fix:** give mobile its own size step: a smaller type scale, tighter section padding, smaller gaps. Keep tap targets at their minimum size (see Tap Targets), but shrink everything else with intent at the breakpoint.

#### Fixed Pixel Type

- **Tell:** font sizes in fixed px that never change between desktop and mobile, so headings and body text stay oversized on a phone.
- **Why:** type that does not respond to the viewport is type sized for one screen. R-03 demands the mobile layout hold up, and R-06 requires typography that improves readability. A headline that spans the whole phone width or a body size tuned for a wide line breaks both.
- **Fix:** use fluid type (`clamp()`) so sizes scale with the viewport, or set a smaller type step at the breakpoint. Verify the result at a narrow width (R-35), not just in the desktop preview.

#### 100vh Sections

- **Tell:** hero and section heights set to `100vh`, so a section fills the whole phone screen and pushes everything else below the fold.
- **Why:** a full-viewport section designed for a desktop monitor becomes a giant slab on a phone, and `100vh` includes the browser chrome, so it overflows the visible area on mobile browsers. It dominates the layout instead of introducing it (R-03).
- **Fix:** let sections size to their content (`auto`), or use the dynamic viewport unit (`dvh`) where a real full-height section is intended. Nothing below the fold should be an accident of viewport units.

#### Huge Empty Padding

- **Tell:** desktop-scale section padding (96px, 128px) kept on mobile, creating tall empty gaps between sections on a phone.
- **Why:** padding tuned for a large canvas turns into wasted vertical space on a small one. The page scrolls through emptiness, and the rhythm R-05 calls for becomes a void between every section.
- **Fix:** reduce section padding at the breakpoint to a mobile register (roughly half or less), and check that the page scrolls at a natural density instead of through deserts of space.

### Grids & Stacking

#### Columns That Don't Collapse

- **Tell:** a multi-column grid keeps its side-by-side columns on mobile, so the columns shrink, the text wraps awkwardly, and elements collide.
- **Why:** a grid is a promise about how much width is available. When the viewport narrows and the grid does not re-stack, every column gets a sliver, text becomes unreadable, and cards overlap (R-03). This is the collision failure: desktop's side-by-side becomes mobile's pileup.
- **Fix:** collapse the grid to a single reflowing column at the breakpoint. Side-by-side becomes stacked, and each item gets the full width again. Re-verify at a narrow width (R-35).

#### Fixed-Width Grid

- **Tell:** `grid-template-columns` set in fixed px, or grid areas that cannot reflow, so the grid stays rigid when the viewport shrinks.
- **Why:** a fixed-px track does not care about the viewport; it keeps its width and forces overflow or collision. The layout was built for one canvas and cannot change shape (R-03).
- **Fix:** size tracks with `minmax()` or `auto-fit` and `auto-fill` so columns shrink and wrap with the content, and define grid areas that collapse at the breakpoint. The grid should be fluid by default, rigid only where a fixed size is deliberate.

#### Forced 12-Column

- **Tell:** a 12-column grid forced onto mobile content that needs one or two columns, so spans look arbitrary and the math fights the layout.
- **Why:** a 12-column system is for a wide canvas with many columns of content. Forcing it on a phone makes every element a fraction of an invisible grid the user never sees, and the content gets fitted to the grid instead of the grid to the content (R-03).
- **Fix:** let columns follow the content. On mobile the content usually wants one column, or two at most; the 12-column span only makes sense where the layout genuinely has that many things side by side.

### Overflow

#### Horizontal Scroll Leak

- **Tell:** the page scrolls sideways because some element is wider than the viewport: a table, a code block, an image, a long unbroken string.
- **Why:** horizontal scrolling is a broken promise on mobile. The user cannot see where the page ends, and the layout visibly spills off the screen (R-03). It is the most common overflow slop because the offender is off-screen in the desktop preview and goes unnoticed until a phone opens it.
- **Fix:** find the element wider than the viewport (a table that needs a reflow layout or a scroll container, a code block that wraps, images with `max-width: 100%`), then contain or reflow it. Verify the whole page has zero horizontal scroll at the narrowest target (R-35).

#### Overflow Hidden Clipping

- **Tell:** `overflow: hidden` on a container that clips content at narrow widths, hiding text or controls instead of letting them fit.
- **Why:** clipping is hiding a failure. When a container cuts off its content because the layout cannot fit it, the user loses information and interaction (R-03). The zoom and text-resize angle on this is covered by `antislop-human`.
- **Fix:** let the content reflow instead of clipping: allow the container to grow, wrap its content, or collapse it at the breakpoint. Clip only where cropping is the design intent (like a thumbnail), never where it hides content.

#### Fixed-Width Children

- **Tell:** flex or grid children with a fixed px width or `min-width` that burst out of their parent on a narrow screen.
- **Why:** a child sized in absolute px does not care how much room its parent has. On mobile the parent shrinks and the child stays wide, so it overflows the container and the page (R-03).
- **Fix:** size children with relative units and let them wrap (`flex-wrap`, fluid widths, `min-width: 0` on grid children). A child should be allowed to shrink with its container, not hold a desktop size.

### Tap Targets

#### Under-Sized Targets

- **Tell:** buttons, links, and controls smaller than about 44 x 44 px, easy to hit on desktop with a cursor but hard to hit with a thumb.
- **Why:** a desktop cursor has pixel accuracy; a thumb does not. A target that is fine at 16px becomes an exercise in frustration on a phone, and it fails the promise that the UI is usable on mobile (R-03).
- **Fix:** give interactive targets a minimum touch area of 44 x 44 px, using padding or a larger hit box even when the visual is smaller. Verify the whole set of controls at a phone width (R-35).

#### Targets Too Close

- **Tell:** 44px targets packed together with no gap, so a thumb tap hits the wrong one.
- **Why:** target size matters only with target spacing. Two large controls touching each other behave like one large control: the user cannot reliably pick either (R-03).
- **Fix:** leave a clear gap between adjacent interactive targets, at least a few px and ideally enough that the finger press area does not overlap. Spacing is the other half of tappability.

#### Hover-Only Interactions

- **Tell:** menus, reveals, and tooltips that exist only on hover, so a touch user can never open them.
- **Why:** there is no hover on a touchscreen. An interaction that only responds to hover simply does not exist for mobile users, and any control that relies on it is a dead end (R-03).
- **Fix:** give every hover-only interaction a tap equivalent: a menu that opens on hover also opens on tap, a reveal also shows on click, and interactive elements show visible `:active` feedback so a tap registers. Test by using the UI with touch alone (R-35).

### Mobile Navigation

#### Nav That Stays Desktop

- **Tell:** the desktop top bar with its row of links kept side by side on mobile, so the links crowd, wrap into two rows, or spill past the viewport.
- **Why:** a desktop nav is sized for a wide canvas. Kept as a row on a phone it becomes a mess of cramped links, and it is the first thing a mobile user meets (R-03). Navigation is where reflow matters most: the user has to find where to go before they can go anywhere.
- **Fix:** collapse the nav into a mobile pattern at the breakpoint: a bottom nav for the handful of primary destinations, or a menu for the rest. The links reflow out of the row, and the primary destinations stay one thumb tap away. Verify it holds at a narrow width (R-35).

#### The Bare Hamburger

- **Tell:** everything hidden behind a hamburger icon with no label and no hint, so a user never realizes the menu exists or cannot tell what it opens.
- **Why:** a bare hamburger assumes the user already knows what the icon means and that a menu hides behind it. That is knowledge the mobile user may not have, and on mobile the hidden menu can hold the only way around the app (R-03).
- **Fix:** keep the menu discoverable: label the hamburger ("Menu"), or keep the primary destinations visible and hide only the secondary ones. If a menu is the only way to reach something important, that reachability has to be obvious.

#### Bottom Nav That Eats Content

- **Tell:** a fixed bottom nav bar that sits over the content, covering the last list items, the final button, or the form the user was trying to finish.
- **Why:** a fixed bar takes real space on a small screen. If nothing reserves that space, the content scrolls under it and the user cannot reach what is hidden, especially at the very bottom of the page (R-03).
- **Fix:** reserve the bar's height for the content: scroll padding on the page and safe-area insets where the device needs them, so nothing important is ever hidden behind it. Verify at a narrow width that the last item is reachable (R-35).

#### Sticky Nav Steals the Screen

- **Tell:** a sticky header or tall bottom bar that holds a large fixed height, so a big slice of the phone screen is always taken by navigation.
- **Why:** on a small viewport every fixed pixel of chrome is a pixel of content lost. A tall sticky header turns the visible area into a letterbox and the content into a sliver (R-03).
- **Fix:** keep fixed nav compact: small enough that the content stays dominant, and collapse or shrink it on scroll where appropriate. Navigation should be present, not the main occupant of the screen.

### Layoutmobile Skill Checklist

Run these alongside the core Delivery Gate when the task is mobile or responsive layout work. All answers must be **yes**:

- [ ] Does the layout reflow into a distinct mobile state rather than a squeezed desktop? (R-03)
- [ ] Are there defined states across the width range, not just phone and desktop, so tablet and small-laptop widths are never a stretched stack or a crammed grid? (R-03, R-35)
- [ ] Do sizes (type, padding, gaps, section heights) use a mobile scale, not desktop sizes unchanged? (R-03, R-05)
- [ ] Do multi-column grids collapse and stack instead of colliding? (R-03)
- [ ] Is there no horizontal overflow and nothing clipped? (R-03)
- [ ] Are interactive targets at least 44 x 44 px with spacing between them? (R-03)
- [ ] Do hover-only interactions have a tap equivalent with visible feedback? (R-03)
- [ ] Does the navigation reflow into a mobile pattern (bottom nav or menu) instead of a squeezed desktop row? (R-03)
- [ ] Do fixed nav bars (bottom nav, sticky headers) never cover content and respect safe areas? (R-03)
- [ ] Is the layout verified at mobile breakpoints? (R-35)
