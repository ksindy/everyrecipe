import asyncpg
import json
from typing import Dict, Any

async def connect_to_db():
    return await asyncpg.connect(database='allplates')

async def add_recipe(recipe_data: Dict[str, Any]):
    conn = await connect_to_db()
    try:
        query = '''
        INSERT INTO recipes (
            title, subtitle, summary, ingredients, steps, prep_time, 
            time_to_ready, kitchenware, ethnicity, meat_type, main_volume, 
            difficulty, raw_text, sauce, side_dishes
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        RETURNING id
        '''
        
        recipe_id = await conn.fetchval(query,
            recipe_data['Title'],
            recipe_data['Subtitle'],
            recipe_data['Summary'],
            recipe_data['Ingredients'].split(', '),  # Convert string to list
            recipe_data['Steps'].split('\n'),  # Convert string to list
            recipe_data['Prep_Time'],
            recipe_data['Time_to_Ready'],
            json.dumps(recipe_data['Kitchenware']),  # Convert dict to JSON string
            recipe_data['Ethnicity'],
            recipe_data['Meat_type'],
            recipe_data['Main_volume'],
            recipe_data['Difficulty'],
            recipe_data['Raw_text'],
            recipe_data['Sauce'],
            recipe_data['Side_dishes']
        )
        
        return recipe_id
    except Exception as e:
        print(f"Error adding recipe to database: {e}")
        return None
    finally:
        await conn.close()

async def get_recipe(recipe_id: int):
    conn = await connect_to_db()
    try:
        query = 'SELECT * FROM recipes WHERE id = $1'
        row = await conn.fetchrow(query, recipe_id)
        if row:
            recipe = dict(row)
            recipe['kitchenware'] = json.loads(recipe['kitchenware'])
            return recipe
        return None
    except Exception as e:
        print(f"Error retrieving recipe from database: {e}")
        return None
    finally:
        await conn.close()
