from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    affiliate_link = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(100), default='General')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
