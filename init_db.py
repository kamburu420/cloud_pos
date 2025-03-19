from app import create_app, db

# Create an application instance
app = create_app()

# Create the tables in the database
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")
