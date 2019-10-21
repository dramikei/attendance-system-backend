import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    enrolment = db.Column(db.String(20), nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    batch = db.Column(db.String(10))
    timetable = db.relationship("TimeTable", backref="User")

    def __init__(self, enrolment, name, password, batch):
        self.enrolment = enrolment
        self.name = name
        self.password = password
        self.batch = batch

class TimeTable(db.Model):
    __tablename__ = 'timetable'
    day = db.Column(db.String(10), nullable = False)
    batch = db.Column(db.String(10), primary_key=True)
    teacherName = db.Column(db.String(255), nullable = False)
    hallName = db.Column(db.String(40), nullable = False)
    time = db.Column(db.String(25), nullable = False)
    subject = db.Column(db.String(30), nullable = False)
    enrolment = db.Column(db.String(20), db.ForeignKey('user.enrolment'))
    hall = db.relationship("LectureHall", backref="TimeTable")

    def __init__(self,day,batch,teacherName,hallName,time,subject):
        self.day = day
        self,batch = batch
        self.teacherName = teacherName
        self.hallName = hallName
        self.time = time
        self.subject = subject

class LectureHall(db.Model):
    __tablename__ = 'lecturehall'
    name = db.Column(db.String(40), primary_key = True)
    macAddress = db.Column(db.Text, nullable = False)
    batch = db.Column(db.String(10), db.ForeignKey('timetable.batch'))

    def __init__(self,name,address):
        self.name = name
        self.macAddress = address


# @app.route('/add', methods=['POST'])
# def demo():
#     json = request.json
#     user = User(json['enrolment'],json['name'],json['password'],json['batch'])
#     db.session.add(user)
#     db.session.commit()
#     return jsonify({"Success"})

if __name__ == '__main__':
    app.run(debug=True)