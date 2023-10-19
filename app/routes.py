from flask import Blueprint, render_template, request
from app.models import RECIPE_INFO

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['POST', 'GET'])
def index():
    recipes = RECIPE_INFO.query.filter_by(FLAG_MAIN = 1).all()
    return render_template('index.html', recipes=recipes)

@routes.route('/new_recipe/', methods=['POST', 'GET'])
def add_recipe():
    if request.method == 'POST':
        recipe_to_add = request.form['content']
        return render_template('new_recipe.html', recipe_to_add = recipe_to_add)        
    else:
        return render_template('new_recipe.html')
