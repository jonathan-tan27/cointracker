from cointracker.lib.utils.util import satoshis_to_bitcoin


class WalletMetadata(object):
    wallet_address: str
    raw_balance: int
    balance_in_btc: float

    def __init__(self, wallet_address: str, final_balance: int, **kwargs):
        self.wallet_address = wallet_address
        self.raw_balance = final_balance
        self.balance_in_btc = satoshis_to_bitcoin(final_balance)
