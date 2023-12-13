from datetime import datetime
from typing import List, Optional

from cointracker.lib.utils.util import satoshis_to_bitcoin


class Transaction(object):
    timestamp: datetime
    transaction_hash: str
    incoming_raw_value: int
    incoming_value_in_btc: float
    outgoing_raw_value: int
    outgoing_value_in_btc: float

    def __init__(
        self,
        wallet_address: str,
        epoch_timestamp: int,
        transaction_hash: str,
        incoming_raw_value: int,
        outgoing_raw_value: int,
        incoming_value_in_btc: Optional[float] = None,
        outgoing_value_in_btc: Optional[float] = None,
        timestamp: Optional[datetime] = None,
    ):
        self.wallet_address = wallet_address
        self.timestamp = (
            timestamp
            if timestamp is not None
            else datetime.utcfromtimestamp(epoch_timestamp)
        )
        self.transaction_hash = transaction_hash
        self.incoming_raw_value = incoming_raw_value
        self.incoming_value_in_btc = (
            incoming_value_in_btc
            if incoming_value_in_btc is not None
            else satoshis_to_bitcoin(incoming_raw_value)
        )
        self.outgoing_raw_value = outgoing_raw_value
        self.outgoing_value_in_btc = (
            outgoing_value_in_btc
            if outgoing_value_in_btc is not None
            else satoshis_to_bitcoin(outgoing_raw_value)
        )

    def __str__(self):
        return f"Txn(timestamp={self.timestamp}, hash={self.transaction_hash}, wallet_address={self.wallet_address}, incoming_value_in_btc={self.incoming_value_in_btc}, outgoing_value_in_btc={self.outgoing_value_in_btc})"
