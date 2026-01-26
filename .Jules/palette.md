# Palette's Journal

## 2025-05-15 - Accessibility in Data Dashboards
**Learning:** Data-heavy dashboards often neglect navigation accessibility in favor of visual density.
**Action:** Always check sidebar navigation for `aria-current` and keyboard focus states, as these are critical for screen reader users to understand where they are.

## 2024-05-23 - Chart Definition Accessibility
**Learning:** Tooltips that appear only on hover are a major accessibility barrier in data visualization. Users relying on keyboards or touch screens cannot access critical context like metric definitions.
**Action:** Always pair hover-based tooltips with a persistent, focusable trigger (like an info icon button) to ensure definitions are discoverable and accessible to all users.

## 2024-05-27 - Mobile Navigation in Fixed Sidebar Dashboards
**Learning:** Dashboards with fixed sidebars often break completely on mobile, becoming unusable. Simply hiding the sidebar is not a responsiveness strategy.
**Action:** Implement a lightweight mobile toggle (hamburger menu) that exposes the existing sidebar structure without needing a complete mobile redesign.

## 2025-02-14 - Scroll Progress Indicator
**Learning:** Adding a visual scroll progress indicator to the "Back to Top" button provides immediate context about the user's position in long reports without needing a separate progress bar. It turns a reactive utility (back to top) into a proactive information element.
**Action:** When designing for long-form content, consider combining "position" indicators with "navigation" actions to save screen real estate and provide dual value. Always ensure the progress value is exposed to screen readers (e.g., via `aria-label`).

## 2025-05-24 - Semantic Structure in Visual Reports
**Learning:** Visual reports often use styled `span` or `div` elements for section headers to achieve specific looks, breaking document outline navigation for screen readers.
**Action:** Use semantic heading tags (`h1`-`h6`) even for visually small headers, relying on CSS (e.g., Tailwind classes) to reset styles to match the design. This preserves the document outline without compromising the visual design.

## 2025-05-24 - Visual Anchors for Abstract Dimensions
**Learning:** In text-heavy "white paper" dashboards, abstract dimensions (like "Structure", "Efficiency") are cognitively expensive to distinguish quickly.
**Action:** Use consistent iconography as visual anchors in navigation to reduce cognitive load and improve scannability when switching between abstract data views.

## 2025-05-26 - Actionable Empty States
**Learning:** Empty states that only say "No data" are dead ends for users, creating frustration.
**Action:** Transform empty states into navigational opportunities by providing a clear explanation and a primary action to recover (e.g., "Clear filters" or "View all"), using illustrations to reduce visual friction.
## 2025-05-28 - Chart Container Accessibility
**Learning:** Complex SVG charts (like Recharts) are often opaque to screen readers. Providing a semantic wrapper with `role="figure"` and a descriptive `aria-label` provides essential context that the chart internals often miss.
**Action:** Wrap all chart components in a semantic container that identifies the chart's purpose/title to screen readers before they navigate into the complex data visualization.
