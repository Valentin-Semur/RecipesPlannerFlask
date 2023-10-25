from bs4 import BeautifulSoup
from app.models import RAW_INGREDIENTS, INGREDIENT_QUANTITIES, RECIPE_INFO
from app import db
import requests
import re

def ProcessNewRecipes(URL):
    URL, soup = GetRecipeHTML(URL)
    ProcessIngredients(URL, soup)
    UpdateIngredientQuantities(URL)
    AddRecipeInfo(URL)


def ProcessIngredients(URL, soup): # Get & Insert ingredients 
    ingredient_list, quantity_list = GetIngredients(soup)
    InsertIngredients(URL, ingredient_list, quantity_list)


def GetRecipeHTML(URL): # Get the HTML code once
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    return URL, soup


def GetIngredients(soup):

    ingredients = soup.find_all(class_="sc-5b343ba0-0 czDpDG")
    quantities = soup.find_all('p', class_='sc-5b343ba0-0 bmbggy')

    ingredient_list = [ingredient.text.strip() for ingredient in ingredients]
    quantity_list = [quantity.text.strip() for quantity in quantities]

    return ingredient_list, quantity_list


def InsertIngredients(URL, ingredient_list, quantity_list):
    try:
        for i in range(len(ingredient_list)):
            ingredient_entry = RAW_INGREDIENTS(
                RECIPE_ID=URL[-24:],
                INGREDIENT=ingredient_list[i],
                QUANTITY=quantity_list[i]
            )
            db.session.add(ingredient_entry)

        db.session.commit()
        print("Record created successfully")
    except Exception as e:
        # Rollback in case of any error
        db.session.rollback()
        print(f"Error occurred: {e}")


def UpdateIngredientQuantities(URL):
    # Mapping fraction strings to decimal values
    fraction_to_decimal = {
        "¼": 0.25, "½": 0.5, "¾": 0.75, "⅓": 0.33, "⅔": 0.66, "⅕": 0.20, "⅖": 0.40, "⅗": 0.60, "⅘": 0.80
    }

    # Fetch all raw ingredients
    raw_ingredients = RAW_INGREDIENTS.query.filter_by(RECIPE_ID=URL[-24:]).all()
    for ingredient in raw_ingredients:
        match = re.match(r'(?P<value>[\d¼½¾⅓⅔⅕⅖⅗⅘]*) (?P<unit>.*)', ingredient.QUANTITY.strip())
        if not match:
            print(f"Failed to match quantity format for {ingredient.QUANTITY}.")
            continue
            
        value_str = match.group("value")
        unit_str = match.group("unit")

        # Convert fractional string to decimal, if it exists in the dictionary
        try:
            value_decimal = fraction_to_decimal.get(value_str, value_str)
        except Exception as e:
            print(f"{e}")

        # Insert or update in the INGREDIENT_QUANTITIES table
        entry = INGREDIENT_QUANTITIES.query.get(ingredient.RECIPE_ID)
        if entry:
            entry.QUANTITY_VALUE = value_decimal
            entry.QUANTITY_UNIT = unit_str
        else:
            new_entry = INGREDIENT_QUANTITIES(
                RECIPE_ID=ingredient.RECIPE_ID,
                INGREDIENT=ingredient.INGREDIENT,
                QUANTITY_VALUE=value_decimal,
                QUANTITY_UNIT=unit_str
            )
            db.session.add(new_entry)

    try:
        # code to update the database
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error updating ingredient quantities: {e}")


# To change in the future in order to get the name from the HTML
def AddRecipeInfo(URL):
    # Extracting ID from the URL
    id_start_index = URL.rfind('-') + 1
    recipe_id = URL[id_start_index:]

    # Extracting NAME from the URL
    name_start_index = URL.rfind('recipes/') + 8
    name_end_index = URL.rfind('-')
    name = URL[name_start_index:name_end_index]
    formatted_name = ' '.join([word.capitalize() for word in name.split('-')])

    new_recipe = RECIPE_INFO(
        ID=recipe_id,
        NAME=formatted_name,
        FLAG_MAIN=1
    )

    # Inserting into the database
    db.session.add(new_recipe)
    db.session.commit()


