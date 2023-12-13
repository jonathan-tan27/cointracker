from typing import Dict, List

from cointracker.lib.models.transaction import Transaction
from cointracker.lib.models.wallet_metadata import WalletMetadata
from cointracker.lib.services.database_service import DatabaseService
from cointracker.lib.services.wallet_address_service import WalletAddressService


class UserService:
    """
    Service handles operations performed against users.
    """

    @staticmethod
    def add_wallet_address(user_id: int, wallet_address: str):
        # Update Database
        DatabaseService.insert_user_wallet_address(
            user_id=user_id, wallet_address=wallet_address
        )

        # Synchronize transactions for wallet address
        WalletAddressService.synchronize_transactions(wallet_address=wallet_address)

    @staticmethod
    def remove_wallet_address(user_id: int, wallet_address: str):
        DatabaseService.delete_user_wallet_address(
            user_id=user_id, wallet_address=wallet_address
        )

    @staticmethod
    def get_wallet_addresses(user_id: int) -> List[str]:
        return DatabaseService.get_user_wallet_addresses(user_id=user_id)

    @staticmethod
    def get_wallet_metadata(user_id: int) -> Dict[str, WalletMetadata]:
        wallet_addresses = UserService.get_wallet_addresses(user_id=user_id)

        return WalletAddressService.get_metadata(wallet_addresses=wallet_addresses)

    @staticmethod
    def get_transactions(
        user_id: int,
        limit: int = 50,
        offset: int = 0,
    ) -> Dict[str, List[Transaction]]:
        wallet_addresses = UserService.get_wallet_addresses(user_id=user_id)

        result = {}
        for address in wallet_addresses:
            transactions = WalletAddressService.get_transactions(
                wallet_address=address, limit=limit, offset=offset
            )
            if transactions:
                result[address] = transactions

        return result

    @staticmethod
    def synchronize_transactions(user_id: int, limit: int = 100):
        wallet_addresses = UserService.get_wallet_addresses(user_id=user_id)

        for address in wallet_addresses:
            WalletAddressService.synchronize_transactions(
                wallet_address=address,
                limit=limit,
            )
