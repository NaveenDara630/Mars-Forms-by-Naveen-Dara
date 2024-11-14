from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()

# Function to create the app
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the database with the app
    db.init_app(app)

    # Import and register the blueprint after initializing the app and db
    from routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    # Ensure database tables are created within the app context
    with app.app_context():
        # Import models explicitly to avoid circular imports and syntax errors
        import models
        db.create_all()

    return app

# Create the app instance
app = create_app()

# Entry point for running the app
if __name__ == "__main__":
    app.run(debug=True)
