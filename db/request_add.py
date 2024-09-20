import requests
import json

url = "http://localhost:8000/api/recipes"
headers = {"Content-Type": "application/json"}
data = {
    "Title": "Pasta Carbonara",
    "Subtitle": "Classic Italian Dish",
    "Summary": "Creamy pasta with eggs and bacon",
    "Ingredients": "pasta, eggs, bacon, cheese",
    "Steps": "1. Cook pasta\n2. Fry bacon\n3. Mix eggs and cheese\n4. Combine all ingredients",
    "Prep_Time": 15,
    "Time_to_Ready": 30,
    "Kitchenware": {"pot": 1, "pan": 1, "bowl": 1},
    "Ethnicity": "Italian",
    "Meat_type": "Bacon",
    "Main_volume": "Pasta",
    "Difficulty": "Easy",
    "Raw_text": "Full recipe text here..."
}

response = requests.post(url, headers=headers, data=json.dumps(data))
print(response.status_code)
print(response.json())