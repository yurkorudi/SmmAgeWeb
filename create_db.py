from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://superuser:yolkipalki220@146.190.65.79/data?charset=utf8mb4"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class ContactRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    business = db.Column(db.String(180))
    category = db.Column(db.String(80))
    budget = db.Column(db.String(80))
    timeline = db.Column(db.String(80))
    channels = db.Column(db.String(255))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class ProjectExample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_slug = db.Column(db.String(80), nullable=False, index=True)
    title = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(120))
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    result = db.Column(db.String(180))
    link = db.Column(db.String(500))
    is_featured = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


with app.app_context():
    db.create_all()

print("Database tables created!")