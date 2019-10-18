import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
# import User

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class User(db.Model):
    enrolment = db.Column(db.String(20), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    batch = db.Column(db.String(10), nullable=False)

    def __init__(self, enrolment, name, password, batch):
        self.enrolment = enrolment
        self.name = name
        self.password = password
        self.batch = batch


@app.route('/add', methods=['POST'])
def demo():
    json = request.json
    user = User(json['enrolment'],json['name'],json['password'],json['batch'])
    db.session.add(user)
    db.session.commit()
    return jsonify("Success")

if __name__ == '__main__':
    app.run(debug=True)