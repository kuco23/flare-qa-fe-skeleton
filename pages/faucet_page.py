from playwright.sync_api import Page

from pages.base_page import BasePage


class FaucetPage(BasePage):
    """Page object for the Flare Faucet."""

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)
        self.request_c2flr_button = page.locator("button", has_text="Request C2FLR")
        self.address_input = page.get_by_placeholder("Flare address")

    def navigate(self, path: str = ""):
        super().navigate(path)
        self.wait_for_load()

    def request_c2flr(self, address: str):
        self.address_input.wait_for(state="visible")
        self.address_input.fill(address)
        self.request_c2flr_button.click()

    def get_success_message(self, timeout: int = 30_000) -> str | None:
        """Wait for and return the success message text, or None if not found."""
        msg = self.page.get_by_text("Tokens sent")
        try:
            msg.wait_for(state="visible", timeout=timeout)
            return msg.text_content()
        except TimeoutError:
            return None
