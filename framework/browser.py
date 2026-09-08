from playwright.sync_api import sync_playwright


def create_browser(playwright, headless=False):
    return playwright.firefox.launch(
        headless=headless
    )

def create_page(browser):
    context = browser.new_context()
    page = context.new_page()
    return page