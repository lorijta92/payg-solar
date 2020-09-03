-- acct_id: accounts, a_s_t, payments

CREATE TABLE account_state_transitions (
    id BIGINT PRIMARY KEY,
    created_when TIMESTAMP,
    started_when TIMESTAMP,
    account_id INT,
    from_state TEXT,
    to_state TEXT,
    previous_state_transition_id BIGINT
);

CREATE TABLE accounts (
    id BIGINT PRIMARY KEY,
    group_id BIGINT,
    organization_id BIGINT,
    registration_date TIMESTAMP,
    is_written_off BOOLEAN,
    is_unlocked BOOLEAN
);

CREATE TABLE group_product_associations (
    id BIGINT PRIMARY KEY,
    group_id BIGINT,
    product_id BIGINT
);

CREATE TABLE groups (
    id BIGINT PRIMARY KEY,
    name TEXT,
    price_upfront INT,
    price_unlock INT,
    price_clock_hour INT,
    minimum_payment INT
);

CREATE TABLE payments (
    id BIGINT PRIMARY KEY,
    effective_when TIMESTAMP,
    account_id BIGINT,
    currency TEXT,
    amount INT
);

CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name TEXT,
    type TEXT
);