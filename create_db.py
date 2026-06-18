from app import app
from extentions import db

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    load_dotenv()

with app.app_context():
    db.create_all()

print("Database tables created.")
