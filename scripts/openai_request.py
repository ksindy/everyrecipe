from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from extract_text import extract_text_from_pdf

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def parse_recipe_with_openai(raw_text):
    prompt = f"""
    Extract the following details from the provided recipe text. 
    I have given directions on what to do next to each entry.
    if the conditional subjects (sauce and side) ore not there you can put "none".:

    Required:
    - Title (text): As close to original as possible
    - Subtitle (text): As close to original as possible
    - Summary (text): Based on text please make a short summary.
    - Ingredients (text): As close to original as possible
    - Steps (text): As close to original as possible
    - Prep_Time (int): As close to original as possible
    - Time_to_Ready (int): As close to original as possible
    - Kitchenware (dict): approximate number (int only)and type of dishes/pans/bowls used in this recipe.
    - Ethnicity (text): ethnicity of meal or broad category
    - Meat_type (text): please describe if it has meat and if can be adapted to vegetarian easily or not and if meat can be easily added
    - Main volume (text): what is the volume of the meal mostly made of? Meat and potatos, Rice and vegetables?
    - Difficulty (text): Please choose from Easy, Moderate, Hard based on recipe

    Conditional:
    - Sauce (text): These are sauces that have instructions to be made. Please use None if none and include multiple if ther are multiple sauces.
    - Side_dishes (text): None if none and include multiple if ther are multiple side dishes. A side dish is something that is added on or next to the main dish.

    If any required field is missing, throw an error.
    Please return in json format. Please properly escape newline characters with \\n. Please properly concatenate multiline strings or write as a single line.
    """

    # Use ChatCompletion for the prompt
    response = client.chat.completions.create(
        model="gpt-4",  # Replace with "gpt-3.5-turbo" if necessary
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts recipe data from text and uses inference to create fields about text."},
            {"role": "user", "content": prompt + "\n\n" + raw_text}
        ],
        max_tokens=1500
    )

    # Access the response correctly as an object
    parsed_text = response.choices[0].message.content.strip()

    try:
        # Parse response as JSON
        parsed_json = json.loads(parsed_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}\nParsed text: {parsed_text}")

    # Validate required fields
    required_fields = [
        "Title", "Subtitle", "Summary", "Ingredients", "Steps", 
        "Prep_Time", "Time_to_Ready", "Kitchenware", "Ethnicity", "Meat_type", "Main_volume", "Difficulty"
    ]

    for field in required_fields:
        if field not in parsed_json:
            raise ValueError(f"Missing required field: {field}")

    # Add default values for conditional fields if not present
    if "Sauce" not in parsed_json:
        parsed_json["Sauce"] = "none"
    if "Side dishes" not in parsed_json:
        parsed_json["Side_dishes"] = "none"
    print(parsed_json)
    return parsed_json

# Function to save JSON locally
def save_json(json_data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

# Main function to process PDFs
def process_pdfs(input_directory, output_directory):
    for index, filename in enumerate(os.listdir(input_directory)):
        if index == 3 and filename.endswith(".pdf"):
            pdf_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.json")

            # Extract text from the PDF
            raw_text = extract_text_from_pdf(pdf_path)

            # Use OpenAI to parse the recipe
            try:
                parsed_json = parse_recipe_with_openai(raw_text)
                parsed_json["Raw_text"] = raw_text  # Ensure raw text is included

                # Save the JSON file
                save_json(parsed_json, output_path)
                print(f"Processed and saved JSON for {filename}")
            except ValueError as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    input_directory = "/Users/karlysindy/Desktop/EveryPlate"
    output_directory = "/Users/karlysindy/Desktop/everyplate_output"
    
    process_pdfs(input_directory, output_directory)