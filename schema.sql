-- DROP TABLE IF EXISTS
-- 	account_state_transitions,
-- 	accounts,
-- 	group_product_associations,
-- 	groups,
-- 	payments,
-- 	products;

CREATE TABLE account_state_transitions (
    id BIGINT,
    created_when TIMESTAMP,
    started_when TIMESTAMP,
    account_id INT,
    from_state TEXT,
    to_state TEXT,
    previous_state_transition_id BIGINT
);

CREATE TABLE accounts (
    id BIGINT,
    group_id BIGINT,
    organization_id BIGINT,
    registration_date TIMESTAMP,
    is_written_off BOOLEAN,
    is_unlocked BOOLEAN
);

CREATE TABLE group_product_associations (
    id BIGINT,
    group_id BIGINT,
    product_id BIGINT
);

CREATE TABLE groups (
    id BIGINT,
    name TEXT,
    price_upfront INT,
    price_unlock INT,
    price_clock_hour DECIMAL,
    minimum_payment DECIMAL
);

CREATE TABLE payments (
    id BIGINT,
    effective_when TIMESTAMP,
    account_id BIGINT,
    currency TEXT,
    amount INT
);

CREATE TABLE products (
    id BIGINT,
    name TEXT,
    type TEXT
);