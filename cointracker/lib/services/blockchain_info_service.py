import logging
from http import HTTPStatus
from typing import List

from requests import Session

from cointracker.lib.decorators.http_request import HTTPRequest, get_retryable_session

logger = logging.getLogger(__name__)

RETRYABLE_STATUS_CODES = [
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
]


class BlockchainInfoService:
    """
    Service handles retrieving data from BlockchainInfo API endpoints.
    """

    session: Session

    def __init__(self):
        self.host = "https://blockchain.info"
        self.session = get_retryable_session()

    @HTTPRequest()
    def get_wallet_address_balance(self, wallet_addresses: List[str]):
        path = "/balance"
        parameters = {"active": "|".join(wallet_addresses)}
        url = self.host + path
        return self.session.get(url=url, params=parameters)

    @HTTPRequest()
    def get_wallet_address_transactions(
        self,
        wallet_address: str,
        limit: int = 50,
        offset: int = 0,
    ):
        path = f"/rawaddr/{wallet_address}"
        parameters = {
            "limit": limit,
            "offset": offset,
        }
        url = self.host + path
        return self.session.get(url=url, params=parameters)


blockchain_info_service = BlockchainInfoService()
