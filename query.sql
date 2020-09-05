-- Q1?
-- View product for account# 168
SELECT ast.account_id, gpa.group_id, gpa.product_id
FROM account_state_transitions AS ast
JOIN accounts AS a ON ast.account_id = a.id
	JOIN group_product_associations AS gpa ON gpa.group_id=a.group_id
	JOIN products AS p ON gpa.product_id=p.id
	WHERE ast.account_id=168;
-- group 13, product 10, paid 106 ~ 9hrs
	
SELECT *
FROM payments
WHERE account_id = 168
ORDER BY effective_when DESC;
-- end q1?

-- START Q2
SELECT started_when, account_id, from_state, to_state
FROM account_state_transitions
WHERE account_id=5
ORDER BY started_when DESC;