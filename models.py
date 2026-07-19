from datetime import datetime

from extentions import db


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


class MainProjectExample(db.Model):
    __tablename__ = 'main_projects_example'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    project_type = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    duration = db.Column(db.String(80), nullable=False)
    budget = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(500))
    image = db.Column(db.String(300))
    

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
