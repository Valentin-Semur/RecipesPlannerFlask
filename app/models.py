from app import db

class RECIPE_INFO(db.Model):
    ID = db.Column(db.String, primary_key=True)
    NAME = db.Column(db.String(100), nullable=False)
    FLAG_MAIN = db.Column(db.Integer)

    def __repr__(self):
        return '<Recipe %r>' % self.ID