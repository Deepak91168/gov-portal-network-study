from playwright.sync_api import sync_playwright
import time

URL = "https://www.google.com"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)

    page = browser.new_page()

    page.on(
        "requestfailed",
        lambda request: print(
            "FAILED:",
            request.url,
            request.failure
        )
    )

    start = time.time()

    try:
        response = page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=300000
        )

        elapsed = time.time() - start

        print("\n=== RESULT ===")
        print("URL:", page.url)
        print("Status:", response.status if response else None)
        print("Title:", page.title())
        print("Time:", round(elapsed, 2), "seconds")

    except Exception as e:
        print("\nERROR:")
        print(e)

    input("Press Enter to close...")
    browser.close()