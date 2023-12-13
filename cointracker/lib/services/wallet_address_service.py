from typing import Dict, List

from cointracker.lib.models.transaction import Transaction
from cointracker.lib.models.wallet_metadata import WalletMetadata
from cointracker.lib.services.blockchain_info_service import blockchain_info_service
from cointracker.lib.services.database_service import DatabaseService


class WalletAddressService:
    """
    Service handles operations performed against wallet addresses.
    """

    @staticmethod
    def get_metadata(wallet_addresses: List[str]) -> Dict[str, WalletMetadata]:
        data = blockchain_info_service.get_wallet_address_balance(
            wallet_addresses=wallet_addresses
        )
        result = {}
        for address in wallet_addresses:
            result[address] = WalletMetadata(wallet_address=address, **data[address])
        return result

    @staticmethod
    def get_transactions(
        wallet_address: str, limit: int = 50, offset: int = 0
    ) -> List[Transaction]:
        return DatabaseService.get_wallet_address_transactions(
            wallet_address=wallet_address,
            limit=limit,
            offset=offset,
        )

    @staticmethod
    def synchronize_transactions(
        wallet_address: str,
        limit: int = 100,
    ) -> List[Transaction]:
        # TODO: This should ideally be ran async. A background worker
        # could download all the transactions and handle inserting
        # them into the database to avoid blocking the caller.
        transactions = []
        api_fetch_limit = 50
        api_fetch_offset = 0

        while True:
            data = blockchain_info_service.get_wallet_address_transactions(
                wallet_address=wallet_address,
                limit=api_fetch_limit,
                offset=api_fetch_offset,
            )
            if "txs" not in data:
                # No more transactions to process
                break

            for txn_data in data["txs"]:
                epoch_timestamp = txn_data["time"]
                txn_hash = txn_data["hash"]
                incoming_raw_value = 0
                outgoing_raw_value = 0

                for input_data in txn_data["inputs"]:
                    metadata = input_data.get("prev_out", {})
                    incoming_raw_value += metadata.get("value", 0)

                for output_data in txn_data["out"]:
                    outgoing_raw_value += output_data.get("value", 0)

                record = Transaction(
                    wallet_address=wallet_address,
                    epoch_timestamp=epoch_timestamp,
                    transaction_hash=txn_hash,
                    incoming_raw_value=incoming_raw_value,
                    outgoing_raw_value=outgoing_raw_value,
                )
                transactions.append(record)

            # Only fetch up to [limit] transactions
            api_fetch_offset += api_fetch_limit
            if api_fetch_offset >= limit:
                break

        DatabaseService.bulk_insert_transactions(transactions=transactions)
        return transactions
