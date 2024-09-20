import asyncpg

async def create_recipes_table():
    conn = await asyncpg.connect(database='allplates')
    try:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                subtitle TEXT,
                summary TEXT,
                ingredients TEXT[],
                steps TEXT[],
                prep_time INTEGER,
                time_to_ready INTEGER,
                kitchenware JSONB,
                ethnicity TEXT,
                meat_type TEXT,
                main_volume TEXT,
                difficulty TEXT,
                raw_text TEXT,
                sauce TEXT,
                side_dishes TEXT
            )
        ''')
        print("Table 'recipes' created successfully.")
    finally:
        await conn.close()

# Call this function during your app startup