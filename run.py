from app import app
from app.routes import routes

app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)




