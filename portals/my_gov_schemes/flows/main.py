import re
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def run_scheme_discovery(page, profile):
    results = {}

    # -------------------------
    # Homepage load
    # -------------------------

    start = time.perf_counter()

    page.goto(
        "https://www.myscheme.gov.in/",
        wait_until="domcontentloaded",
        timeout=240_000,
    )
    find_schemes_button = page.get_by_role(
        "button",
        name="Find Schemes For You",
    )
    find_schemes_button.wait_for(state="visible")

    results["homepage_load"] = time.perf_counter() - start

    # -------------------------
    # Start workflow
    # -------------------------

    workflow_start = time.perf_counter()
    find_schemes_button.click()

    # Gender
    gender_option = page.locator("label").filter(
        has_text=re.compile(f"^{profile['gender']}$")
    )
    try:
        gender_option.wait_for(state="visible", timeout=5_000)
    except PlaywrightTimeoutError:
        # The button can be rendered before its client-side click handler is
        # attached. Retry only when the expected workflow transition did not
        # occur; this adds no fixed delay.
        find_schemes_button.click()
        gender_option.wait_for(state="visible")
    gender_option.click()

    # Age
    page.get_by_role("combobox").nth(0).select_option(
        str(profile["age"])
    )

    page.get_by_role("button", name="Next").click()

    # State
    page.get_by_role("combobox").nth(1).select_option(
        profile["state"]
    )

    # Location - urban or Rural
    page.locator("label").filter(
        has_text=profile["location"]
    ).click()

    page.get_by_role("button", name="Next").click()

    # Social category
    page.locator("label").filter(
        has_text=profile["category"]
    ).click()

    page.get_by_role("button", name="Next").click()

    # Disability
    disability = "Yes" if profile["disability"] else "No"

    page.locator(
        f'label[for="answer{disability}_disability"]'
    ).click()

    # Minority
    minority = "Yes" if profile["minority"] else "No"

    page.locator(
        f'label[for="answer{minority}_minority"]'
    ).click()

    page.get_by_role("button", name="Next").click()

    # Student
    student = "Yes" if profile["student"] else "No"

    page.locator(
        f'label[for="answer{student}_isStudent"]'
    ).click()

    page.get_by_role("button", name="Next").click()

    # BPL
    bpl = "Yes" if profile["bpl"] else "No"

    page.locator(
        f'label[for="answer{bpl}_isBpl"]'
    ).click()

    # Income
    page.locator(
        'h2:has-text("What is your family\'s annual income?") + div input'
    ).fill(
        str(profile["family_income"])
    )

    page.locator(
        'h2:has-text("What is your parent / guardian\'s annual income?") + div input'
    ).fill(
        str(profile["parent_income"])
    )

    page.get_by_role("button", name="Next").click()

    page.locator("#scheme-name-0").wait_for()

    results["workflow_time"] = time.perf_counter() - workflow_start

    # -------------------------
    # Open first recommended scheme
    # -------------------------

    start = time.perf_counter()

    page.locator("#scheme-name-0 a").click()
    page.wait_for_load_state("domcontentloaded")

    results["scheme_load"] = time.perf_counter() - start

    # -------------------------
    # Total
    # -------------------------

    results["total_time"] = (
        results["homepage_load"]
        + results["workflow_time"]
        + results["scheme_load"]
    )

    results["success"] = True

    return results