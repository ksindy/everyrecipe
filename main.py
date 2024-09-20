import uvicorn
from typing import Union, Optional
from fastapi import FastAPI, Query, HTTPException, UploadFile, File, Request, Form, Body
from pydantic import BaseModel, ValidationError
from typing import List, Dict
from db.init_db import create_recipes_table
from contextlib import asynccontextmanager
from db.db_operations import add_recipe, get_recipe
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic here
    try:
        await create_recipes_table()
        print("Database table created successfully")
    except Exception as e:
        print(f"Error creating database table: {e}")
    yield
    # Shutdown logic here

app = FastAPI(lifespan=lifespan)

class Recipe(BaseModel):
    id: Optional[int] = None
    title: str
    subtitle: str
    summary: str
    ingredients: List[str]
    steps: List[str]
    prep_time: int
    time_to_ready: int
    kitchenware: Dict[str, int]
    ethnicity: str
    meat_type: str
    main_volume: str
    difficulty: str
    raw_text: str
    sauce: Optional[str] = None
    side_dishes: Optional[str] = None
    is_sauce: Optional[bool] = None
    is_side: Optional[bool] = None
    image: Optional[str] = None
    flagged: Optional[bool] = None

class RecipeInput(BaseModel):
    Title: str
    Subtitle: str
    Summary: str
    Ingredients: str
    Steps: str
    Prep_Time: int
    Time_to_Ready: int
    Kitchenware: Dict[str, int]
    Ethnicity: str
    Meat_type: str
    Main_volume: str
    Difficulty: str
    Raw_text: str
    Sauce: Optional[str] = None
    Side_dishes: Optional[str] = None

@app.get("/api/recipes/search")
async def search_recipes(
    term: str = Query(None, min_length=1),
    ethnicity: Optional[str] = None,
    meat_type: Optional[str] = None,
    difficulty: Optional[str] = None,
    min_prep_time: int = 0,
    max_prep_time: int = 120,
    min_time_to_ready: int = 0,
    max_time_to_ready: int = 240,
    recipe_type: Optional[str] = None,
    min_kitchenware_count: int = 0,
    max_kitchenware_count: int = 10
) -> List[Recipe]:
    if not term:
        return []
    # Implement your search logic here using the term variable
    # Example: search_results = query_database(term, ethnicity, meat_type, difficulty, ...)
    # Return a list of Recipe objects
    pass

@app.post("/api/recipes")
async def create_recipe(recipe: RecipeInput):
    print("Entering create_recipe function")
    print(f"Received recipe: {recipe}")

    try:
        recipe_id = await add_recipe(recipe.dict())
        if recipe_id:
            return {"id": recipe_id, "message": "Recipe added successfully"}
        raise HTTPException(status_code=500, detail="Failed to add recipe")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/api/recipes/{recipe_id}")
async def read_recipe(recipe_id: int):
    recipe = await get_recipe(recipe_id)
    if recipe:
        return recipe
    raise HTTPException(status_code=404, detail="Recipe not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)