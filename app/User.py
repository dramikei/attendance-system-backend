from app import db
class User(db.Model):
    enrolment = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    batch = db.Column(db.String(10), nullable=False)