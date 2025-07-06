create_queries = [
    """
    CREATE TABLE IF NOT EXISTS accounts (
        id SERIAL PRIMARY KEY,
        login VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        account_id INTEGER REFERENCES accounts(id) ON DELETE CASCADE,
        
        current_expert VARCHAR(50) DEFAULT 'registrator',
        current_topic JSONB DEFAULT '{}'::jsonb,
        current_block JSONB DEFAULT '{}'::jsonb,
        current_chapter JSONB DEFAULT '{}'::jsonb,
        
        programming_experience TEXT,
        education_background TEXT,
        learning_goals TEXT,
        career_goals TEXT,
        timeline TEXT,
        learning_style TEXT,
        lesson_duration TEXT,
        preferred_difficulty TEXT,
        
        recommended_topics JSONB DEFAULT '{}'::jsonb,
        recommended_blocks JSONB DEFAULT '{}'::jsonb,
        approved_topics JSONB DEFAULT '{}'::jsonb,
        approved_blocks JSONB DEFAULT '{}'::jsonb,
        approved_chapters JSONB DEFAULT '{}'::jsonb,
        
        assessment_score INTEGER CHECK (assessment_score >= 0 AND assessment_score <= 100),
        strong_areas JSONB DEFAULT '[]'::jsonb,
        weak_areas JSONB DEFAULT '[]'::jsonb,
        
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS topics (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        intro_file_id VARCHAR(255),
        edu_plan_file_id VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS blocks (
        id SERIAL PRIMARY KEY,
        topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        content_file_id VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS chapters (
        id SERIAL PRIMARY KEY,
        topic_id INTEGER REFERENCES topics(id) ON DELETE CASCADE,
        block_id INTEGER REFERENCES blocks(id) ON DELETE CASCADE,
        name VARCHAR(255) NOT NULL,
        content_file_id VARCHAR(255),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS chats (
        id SERIAL PRIMARY KEY,
        student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS messages (
        id SERIAL PRIMARY KEY,
        chat_id INTEGER REFERENCES chats(id) ON DELETE CASCADE,
        role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
        text TEXT NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    """,
    # Indexes
    "CREATE INDEX IF NOT EXISTS idx_students_account_id ON students(account_id);",
    "CREATE INDEX IF NOT EXISTS idx_blocks_topic_id ON blocks(topic_id);",
    "CREATE INDEX IF NOT EXISTS idx_chapters_block_id ON chapters(block_id);",
    "CREATE INDEX IF NOT EXISTS idx_chapters_topic_id ON chapters(topic_id);",
    "CREATE INDEX IF NOT EXISTS idx_chats_student_id ON chats(student_id);",
    "CREATE INDEX IF NOT EXISTS idx_messages_chat_id ON messages(chat_id);",
    "CREATE INDEX IF NOT EXISTS idx_accounts_login ON accounts(login);"
]

drop_queries = [
    "DROP TABLE IF EXISTS messages CASCADE;",
    "DROP TABLE IF EXISTS chats CASCADE;",
    "DROP TABLE IF EXISTS chapters CASCADE;",
    "DROP TABLE IF EXISTS blocks CASCADE;",
    "DROP TABLE IF EXISTS topics CASCADE;",
    "DROP TABLE IF EXISTS students CASCADE;",
    "DROP TABLE IF EXISTS accounts CASCADE;"
]