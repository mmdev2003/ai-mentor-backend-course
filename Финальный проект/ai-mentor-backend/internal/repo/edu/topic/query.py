# Topics queries
create_topic = """
INSERT INTO topics (name, intro_file_id, edu_plan_file_id, created_at, updated_at)
VALUES (:name, :intro_file_id, :edu_plan_file_id, NOW(), NOW())
RETURNING id;
"""

get_topic_by_id = """
SELECT id, name, intro_file_id, edu_plan_file_id, created_at, updated_at
FROM topics
WHERE id = :topic_id;
"""

get_all_topics = """
SELECT id, name, intro_file_id, edu_plan_file_id, created_at, updated_at
FROM topics
ORDER BY id ASC;
"""

update_topic = """
UPDATE topics
SET name = :name, intro_file_id = :intro_file_id, edu_plan_file_id = :edu_plan_file_id, updated_at = NOW()
WHERE id = :topic_id;
"""

# Blocks queries
create_block = """
INSERT INTO blocks (topic_id, name, content_file_id, created_at, updated_at)
VALUES (:topic_id, :name, :content_file_id, NOW(), NOW())
RETURNING id;
"""

get_block_by_id = """
SELECT id, topic_id, name, content_file_id, created_at, updated_at
FROM blocks
WHERE id = :block_id;
"""

get_blocks_by_topic_id = """
SELECT id, topic_id, name, content_file_id, created_at, updated_at
FROM blocks
WHERE topic_id = :topic_id
ORDER BY id ASC;
"""

get_all_blocks = """
SELECT id, topic_id, name, content_file_id, created_at, updated_at
FROM blocks
ORDER BY topic_id ASC, id ASC;
"""

update_block = """
UPDATE blocks
SET name = :name, content_file_id = :content_file_id, updated_at = NOW()
WHERE id = :block_id;
"""

# Chapters queries
create_chapter = """
INSERT INTO chapters (topic_id, block_id, name, content_file_id, created_at, updated_at)
VALUES (:topic_id, :block_id, :name, :content_file_id, NOW(), NOW())
RETURNING id;
"""

get_chapter_by_id = """
SELECT id, topic_id, block_id, name, content_file_id, created_at, updated_at
FROM chapters
WHERE id = :chapter_id;
"""

get_chapters_by_block_id = """
SELECT id, topic_id, block_id, name, content_file_id, created_at, updated_at
FROM chapters
WHERE block_id = :block_id
ORDER BY id ASC;
"""

get_all_chapters = """
SELECT id, topic_id, block_id, name, content_file_id, created_at, updated_at
FROM chapters
ORDER BY topic_id ASC, block_id ASC, id ASC;
"""

update_chapter = """
UPDATE chapters
SET name = :name, content_file_id = :content_file_id, updated_at = NOW()
WHERE id = :chapter_id;
"""

# Student progress updates
update_current_topic = """
UPDATE students
SET current_topic = jsonb_build_object(:topic_id::text, :topic_name), updated_at = NOW()
WHERE id = :student_id;
"""

update_current_block = """
UPDATE students
SET current_block = jsonb_build_object(:block_id::text, :block_name), updated_at = NOW()
WHERE id = :student_id;
"""

update_current_chapter = """
UPDATE students
SET current_chapter = jsonb_build_object(:chapter_id::text, :chapter_name), updated_at = NOW()
WHERE id = :student_id;
"""