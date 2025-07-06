create_chat = """
INSERT INTO chats (student_id, created_at, updated_at)
VALUES (:student_id, NOW(), NOW())
RETURNING id;
"""

get_chat_by_student_id = """
SELECT id, student_id, created_at, updated_at
FROM chats
WHERE student_id = :student_id
ORDER BY created_at DESC
LIMIT 1;
"""

get_chat_by_id = """
SELECT id, student_id, created_at, updated_at
FROM chats
WHERE id = :chat_id;
"""

create_message = """
INSERT INTO messages (chat_id, role, text, created_at, updated_at)
VALUES (:chat_id, :role, :text, NOW(), NOW())
RETURNING id;
"""

get_messages_by_chat_id = """
SELECT id, chat_id, text, role, created_at, updated_at
FROM messages
WHERE chat_id = :chat_id
ORDER BY created_at ASC;
"""

get_message_by_id = """
SELECT id, chat_id, text, role, created_at, updated_at
FROM messages
WHERE id = :message_id;
"""

delete_chat = """
DELETE FROM chats
WHERE id = :chat_id;
"""

delete_message = """
DELETE FROM messages
WHERE id = :message_id;
"""