create_student = """
INSERT INTO students (
    account_id, 
    current_expert,
    created_at, 
    updated_at
)
VALUES (:account_id, 'registrator', NOW(), NOW())
RETURNING id;
"""

get_student_by_id = """
SELECT 
    id, account_id, current_expert, current_topic, current_block, current_chapter,
    programming_experience, education_background, learning_goals, career_goals, timeline,
    learning_style, lesson_duration, preferred_difficulty, recommended_topics, recommended_blocks,
    approved_topics, approved_blocks, approved_chapters, assessment_score, strong_areas, weak_areas,
    created_at, updated_at
FROM students
WHERE id = :student_id;
"""

get_student_by_account_id = """
SELECT 
    id, account_id, current_expert, current_topic, current_block, current_chapter,
    programming_experience, education_background, learning_goals, career_goals, timeline,
    learning_style, lesson_duration, preferred_difficulty, recommended_topics, recommended_blocks,
    approved_topics, approved_blocks, approved_chapters, assessment_score, strong_areas, weak_areas,
    created_at, updated_at
FROM students
WHERE account_id = :account_id;
"""

update_student_background = """
UPDATE students
SET 
    programming_experience = COALESCE(:programming_experience, programming_experience),
    education_background = COALESCE(:education_background, education_background),
    learning_goals = COALESCE(:learning_goals, learning_goals),
    career_goals = COALESCE(:career_goals, career_goals),
    timeline = COALESCE(:timeline, timeline),
    learning_style = COALESCE(:learning_style, learning_style),
    lesson_duration = COALESCE(:lesson_duration, lesson_duration),
    preferred_difficulty = COALESCE(:preferred_difficulty, preferred_difficulty),
    recommended_topics = COALESCE(:recommended_topics::jsonb, recommended_topics),
    recommended_blocks = COALESCE(:recommended_blocks::jsonb, recommended_blocks),
    approved_topics = COALESCE(:approved_topics::jsonb, approved_topics),
    approved_blocks = COALESCE(:approved_blocks::jsonb, approved_blocks),
    approved_chapters = COALESCE(:approved_chapters::jsonb, approved_chapters),
    assessment_score = COALESCE(:assessment_score, assessment_score),
    strong_areas = COALESCE(:strong_areas::jsonb, strong_areas),
    weak_areas = COALESCE(:weak_areas::jsonb, weak_areas),
    updated_at = NOW()
WHERE id = :student_id;
"""

change_current_expert = """
UPDATE students
SET current_expert = :expert_name, updated_at = NOW()
WHERE id = :student_id;
"""

add_topic_to_approved = """
UPDATE students
SET 
    approved_topics = COALESCE(approved_topics, '{}'::jsonb) || jsonb_build_object(:topic_id::text, :topic_name),
    updated_at = NOW()
WHERE id = :student_id;
"""

add_block_to_approved = """
UPDATE students
SET 
    approved_blocks = COALESCE(approved_blocks, '{}'::jsonb) || jsonb_build_object(:block_id::text, :block_name),
    updated_at = NOW()
WHERE id = :student_id;
"""

add_chapter_to_approved = """
UPDATE students
SET 
    approved_chapters = COALESCE(approved_chapters, '{}'::jsonb) || jsonb_build_object(:chapter_id::text, :chapter_name),
    updated_at = NOW()
WHERE id = :student_id;
"""