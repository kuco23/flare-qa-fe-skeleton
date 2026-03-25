from playwright.sync_api import Page


class BasePage:
    """Base page object that all page objects inherit from."""

    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def navigate(self, path: str = ""):
        self.page.goto(f"{self.base_url}/{path}".rstrip("/"))

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")
