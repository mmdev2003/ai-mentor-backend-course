create_account = """
INSERT INTO accounts (login, password, created_at, updated_at)
VALUES (:login, :password, NOW(), NOW())
RETURNING id;
"""

get_account_by_login = """
SELECT id, login, password, created_at, updated_at 
FROM accounts
WHERE login = :login;
"""

get_account_by_id = """
SELECT id, login, password, created_at, updated_at 
FROM accounts
WHERE id = :account_id;
"""

update_account_password = """
UPDATE accounts
SET password = :password, updated_at = NOW()
WHERE id = :account_id;
"""

delete_account = """
DELETE FROM accounts
WHERE id = :account_id;
"""