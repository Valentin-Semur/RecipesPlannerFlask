from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
db = SQLAlchemy(app)

class RECIPE_INFO(db.Model):
    ID = db.Column(db.String, primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    FLAG_MAIN = db.Column(db.Integer)

    def __repr__(self):
        return '<Recipe %r>' % self.ID



@app.route('/', methods=['POST', 'GET'])
def index():
    recipes = RECIPE_INFO.query.filter_by(FLAG_MAIN = 1).all()
    return render_template('index.html', recipes=recipes)

@app.route('/new_recipe/', methods=['POST', 'GET'])
def add_recipe():
    if request.method == 'POST':
        recipe_to_add = request.form['content']
        return render_template('new_recipe.html', recipe_to_add = recipe_to_add)        
    else:
        return render_template('new_recipe.html')


if __name__ == "__main__":
    app.run(debug=True)

