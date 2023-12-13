CREATE TABLE users
(
    "id" SERIAL PRIMARY KEY,
    "name" VARCHAR(128),
    "email" VARCHAR(128),
    "created_at" TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE wallet_addresses
(
    "id" SERIAL PRIMARY KEY,
    "user_id" INTEGER REFERENCES users(id),
    "address" VARCHAR(256),
    "created_at" TIMESTAMP NOT NULL DEFAULT NOW()
)

CREATE TABLE transactions
(
    "wallet_address" VARCHAR(256) NOT NULL,
    "transaction_hash" VARCHAR(512) NOT NULL,
    "timestamp" TIMESTAMP NOT NULL,
    "incoming_raw_value" INTEGER,
    "outgoing_raw_value" INTEGER,
    "incoming_value_in_btc" FLOAT,
    "outgoing_value_in_btc" FLOAT,
    PRIMARY KEY ("wallet_address", "transaction_hash")
)