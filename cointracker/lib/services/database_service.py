import logging
from typing import List

import psycopg2

from cointracker.lib.models.transaction import Transaction
from cointracker.lib.models.user import User
from config import config

logger = logging.getLogger(__name__)


class DatabaseService:
    """
    Service handles executing operations against the database.
    """

    @staticmethod
    def execute_sql(sql_command: str):
        """Connect to the PostgreSQL database server"""
        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            cur.execute(sql_command)
            conn.commit()
            response = cur.fetchall()
            cur.close()

            return response
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error(error)
        finally:
            if conn is not None:
                conn.close()
                logger.debug("Database connection closed.")

    @staticmethod
    def get_user(id: int) -> User:
        command = f"SELECT id, name, email, signup_date FROM users WHERE id = {id}"
        response = DatabaseService.execute_sql(command)
        if len(response) < 0:
            raise ValueError(f"Could not find user with id, {id}")

        data = response[0]
        id = int(data[0])
        name = str(data[1])
        email = str(data[2])
        created_at = data[3]

        return User(id=id, name=name, email=email, created_at=created_at)

    @staticmethod
    def get_user_wallet_addresses(user_id: int) -> List[str]:
        command = f"SELECT address FROM wallet_addresses WHERE user_id = {user_id}"
        response = DatabaseService.execute_sql(command)
        if not response:
            return []

        return [e[0] for e in response if e[0]]

    @staticmethod
    def insert_user_wallet_address(user_id: int, wallet_address: str):
        command = f"INSERT INTO wallet_addresses(user_id, address) VALUES({user_id}, '{wallet_address}')"
        DatabaseService.execute_sql(command)

    @staticmethod
    def delete_user_wallet_address(user_id: int, wallet_address: str):
        command = f"DELETE FROM wallet_addresses WHERE user_id = {user_id} and address = '{wallet_address}'"
        DatabaseService.execute_sql(command)

    @staticmethod
    def bulk_insert_transactions(transactions: List[Transaction]):
        for i in range(0, len(transactions), 50):
            current_set = transactions[i:50]
            values = ",".join(
                [
                    f"('{e.timestamp}','{e.transaction_hash}','{e.wallet_address}',{e.incoming_raw_value},{e.outgoing_raw_value},{e.incoming_value_in_btc},{e.outgoing_value_in_btc})"
                    for e in current_set
                ]
            )
            command = f"""
                INSERT INTO transactions(
                    timestamp,
                    transaction_hash,
                    wallet_address,
                    incoming_raw_value,
                    outgoing_raw_value,
                    incoming_value_in_btc,
                    outgoing_value_in_btc
                ) VALUES {values}
            """
            DatabaseService.execute_sql(command)

    @staticmethod
    def get_wallet_address_transactions(
        wallet_address: str,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Transaction]:
        command = f"""
        SELECT
            timestamp,
            transaction_hash,
            wallet_address,
            incoming_raw_value,
            outgoing_raw_value,
            incoming_value_in_btc,
            outgoing_value_in_btc
        FROM transactions
        WHERE wallet_address = '{wallet_address}'
        ORDER BY timestamp DESC
        LIMIT {limit}
        OFFSET {offset};
        """
        response = DatabaseService.execute_sql(command)
        if len(response) < 0:
            return []

        result = []
        for data in response:
            timestamp = data[0]
            transaction_hash = str(data[1])
            wallet_address = str(data[2])
            incoming_raw_value = int(data[3])
            outgoing_raw_value = int(data[4])
            incoming_value_in_btc = float(data[5])
            outgoing_value_in_btc = float(data[6])

            record = Transaction(
                wallet_address=wallet_address,
                epoch_timestamp=0,
                timestamp=timestamp,
                transaction_hash=transaction_hash,
                incoming_raw_value=incoming_raw_value,
                outgoing_raw_value=outgoing_raw_value,
                incoming_value_in_btc=incoming_value_in_btc,
                outgoing_value_in_btc=outgoing_value_in_btc,
            )
            result.append(record)

        return result
