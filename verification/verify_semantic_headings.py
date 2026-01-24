from playwright.sync_api import Page, expect, sync_playwright

def test_semantic_headings(page: Page):
    try:
        page.goto("http://localhost:3000/white-paper/")
        expect(page.get_by_role("heading", level=1, name="低空经济")).to_be_visible(timeout=5000)
    except:
        page.goto("http://localhost:3000/")

    # Click on the sidebar button for "规模与增长"
    # This should hide the cover page and show the report pages for this dimension
    page.get_by_role("button", name="规模与增长").click()

    # Wait for content to load
    # We look for "指标定义" which should now be a heading level 3

    # Check for "指标定义" heading
    definition_heading = page.get_by_role("heading", level=3, name="指标定义").first
    expect(definition_heading).to_be_visible()

    # Scroll it into view
    definition_heading.scroll_into_view_if_needed()

    # Check for "数据洞察" heading
    insight_heading = page.get_by_role("heading", level=3, name="数据洞察").first
    expect(insight_heading).to_be_visible()

    # Check for "策略建议" heading
    suggestion_heading = page.get_by_role("heading", level=3, name="策略建议").first
    expect(suggestion_heading).to_be_visible()

    # Take a screenshot of the visible report page
    page.screenshot(path="verification/verification.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_semantic_headings(page)
            print("Verification passed!")
        except Exception as e:
            print(f"Verification failed: {e}")
            try:
                page.screenshot(path="verification/verification_failed.png")
            except:
                pass
        finally:
            browser.close()
