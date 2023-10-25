from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class RecipeForm(FlaskForm):
    input_text = StringField('Enter Something:')
    submit = SubmitField('Submit')
