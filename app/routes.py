from flask import Blueprint, render_template, request
from app.models import RECIPE_INFO, RECIPE_URLS
from app.utils import ProcessNewRecipes
from app.forms import RecipeForm
from app import db

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['POST', 'GET'])
def index():
    recipes = RECIPE_INFO.query.filter_by(FLAG_MAIN = 1).all()
    return render_template('index.html', recipes=recipes)


@routes.route('/new_recipe/', methods=['POST', 'GET'])
def new_recipe():
    if request.method == 'POST':
        recipe_to_add = request.form['content']
        recipe = RECIPE_URLS(ID=recipe_to_add[-24:],URL=recipe_to_add)

        try:
            db.session.add(recipe)
            db.session.commit()

            ProcessNewRecipes(recipe_to_add)

            return render_template('new_recipe.html', recipe_to_add = recipe_to_add + ' OK')  
        except:
            return 'There was an issue adding your recipe'
    
    else:
        return render_template('new_recipe.html')

@routes.route('/shopping_list/', methods=['POST', 'GET'])
def shopping_list():
    form = RecipeForm()
    search_string = "%%"
    if form.validate_on_submit():
        search_string = "%" + form.input_text.data + "%"
    recipes = RECIPE_INFO.query.filter(RECIPE_INFO.FLAG_MAIN == 1).filter(RECIPE_INFO.NAME.like(search_string)).all()

    selected_recipe = request.form.get('selectedRecipe')
    selectedNumber = request.form.get('selectedNumber')
    print(selectedNumber, selected_recipe)
    
    return render_template('shopping_list.html', form=form, recipes=recipes)

