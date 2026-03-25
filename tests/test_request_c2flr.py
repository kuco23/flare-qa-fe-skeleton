import time

import pytest
from eth_account import Account
from playwright.sync_api import Page

from chain import ChainClient
from pages.faucet_page import FaucetPage


@pytest.fixture
def evm_address():
    account = Account.create()
    return account.address


@pytest.fixture
def faucet_page(page: Page, base_url: str):
    faucet = FaucetPage(page, base_url)
    faucet.navigate()
    return faucet


def test_request_c2flr(
    faucet_page: FaucetPage,
    chain_client: ChainClient,
    evm_address: str,
):
    """Spec: specs/faucet/request-c2flr.md

    1. Generate an EVM address
    2. Navigate to the Flare Faucet
    3. Enter the EVM address in the address field
    4. Click the "Request C2FLR" button
    """
    assert chain_client.get_balance(evm_address) == 0

    faucet_page.request_c2flr(evm_address)
    success_message = faucet_page.get_success_message()
    assert success_message is not None, "Expected 'Tokens sent' success message"

    deadline = time.time() + 60
    while time.time() < deadline:
        if chain_client.get_balance(evm_address) > 0:
            break
        time.sleep(5)

    balance = chain_client.get_balance_ether(evm_address)
    assert balance > 0, f"No C2FLR received within 1 minute (balance: {balance})"
