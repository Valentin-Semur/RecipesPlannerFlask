from app import db

class RECIPE_INFO(db.Model):
    ID = db.Column(db.String(24), primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    FLAG_MAIN = db.Column(db.Integer)

    def __repr__(self):
        return '<RecipeInfo %r>' % self.ID
    
    
class RECIPE_URLS(db.Model):
    ID = db.Column(db.String(24), primary_key=True, unique=True, nullable=False)
    URL = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<RecipeURL %r>' % self.ID
    

class INGREDIENT_QUANTITIES(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    RECIPE_ID = db.Column(db.String(24), nullable=False)
    INGREDIENT = db.Column(db.String(100), nullable=False)
    QUANTITY_VALUE = db.Column(db.Float, nullable=False)
    QUANTITY_UNIT = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<IngredientQuantity %r>' % self.ID
    

class SHOPPING_LIST(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    INGREDIENT = db.Column(db.String(100), nullable=False)
    QUANTITY_VALUE = db.Column(db.Float, nullable=False)
    QUANTITY_UNIT = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<ShoppingList %r>' % self.ID
    

class RECIPE_TAGS(db.Model):
    ID = db.Column(db.String(24), primary_key=True, nullable=False)
    TAG = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<RecipeTag %r>' % self.ID
    

class RAW_INGREDIENTS(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    RECIPE_ID = db.Column(db.String(24), nullable=False)
    INGREDIENT = db.Column(db.String(100), nullable=False)
    QUANTITY = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<RawIngredient %r>' % self.ID
