import yaml

from playwright.sync_api import sync_playwright

from framework.browser import create_browser, create_page
from portals.my_gov_schemes.flows.main import run_scheme_discovery


PROFILE_PATH = "config/profiles/user1.yaml"


def load_profile(path):
    with open(path, "r") as file:
        return yaml.safe_load(file)


def main():

    # Load user profile
    profile = load_profile(PROFILE_PATH)

    with sync_playwright() as p:

        # Create browser
        browser = create_browser(
            p,
            headless=False
        )

        # Create page
        page = create_page(browser)

        # Run myScheme workflow
        results = run_scheme_discovery(
            page,
            profile
        )
        
        print("\nExperiment results:")
        print("------------------")

        for metric, value in results.items():
            if metric == "success":
                print(f"{metric}: {value}")
            else:
                print(f"{metric}: {value:.3f} seconds")

        input("Press Enter to close browser...")

        browser.close()


if __name__ == "__main__":
    main()