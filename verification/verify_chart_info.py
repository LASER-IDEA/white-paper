from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:3000")

    # Wait for the main page to load
    page.wait_for_selector('h1', timeout=60000)

    # Find the button with aria-label="查看指标定义"
    info_button = page.get_by_label("查看指标定义").first

    # Scroll to it
    info_button.scroll_into_view_if_needed()

    # Focus the button
    info_button.focus()

    # Wait for tooltip to be visible
    tooltip = page.get_by_role("tooltip").first
    expect(tooltip).to_be_visible()

    # Take screenshot of the tooltip
    page.screenshot(path="verification/chart_info_tooltip.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
