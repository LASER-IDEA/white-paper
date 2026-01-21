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
