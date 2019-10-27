import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


############### Setup ###############

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "attendance.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)


############### Models ###############

class User(db.Model):
    __tablename__ = 'user'
    enrolment = db.Column(db.String(20), nullable=False, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    batch = db.Column(db.String(10))
    # timetable = db.relationship("TimeTable", backref="User")

    def __init__(self, enrolment, name, password, batch):
        self.enrolment = enrolment
        self.name = name
        self.password = password
        self.batch = batch
    def serialize(self):
        return {
            'enrolment': self.enrolment, 
            'name': self.name,
            'batch': self.batch
            # 'timetable':self.timetable
        }

class TimeTable(db.Model):
    __tablename__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(10), nullable = False)
    batch = db.Column(db.String(10))
    teacherName = db.Column(db.String(255), nullable = False)
    hallName = db.Column(db.String(40), nullable = False)
    time = db.Column(db.String(25), nullable = False)
    subject = db.Column(db.String(30), nullable = False)
    enrolment = db.Column(db.String(20), db.ForeignKey('user.enrolment'))
    # hall = db.relationship("LectureHall", backref="TimeTable")

    def __init__(self,day,batch,teacherName,hallName,time,subject):
        self.day = day
        self.batch = batch
        self.teacherName = teacherName
        self.hallName = hallName
        self.time = time
        self.subject = subject

    def serialize(self):
        return {
            'day': self.day, 
            'batch': self.batch,
            'teacherName': self.teacherName,
            'hallName': self.hallName,
            'time': self.time,
            'subject': self.subject
        }

class LectureHall(db.Model):
    __tablename__ = 'lecturehall'
    name = db.Column(db.String(40), primary_key = True)
    macAddress = db.Column(db.Text, nullable = False)
    table_id = db.Column(db.String(10), db.ForeignKey('timetable.id'))

    def __init__(self,name,address):
        self.name = name
        self.macAddress = address
    def serialize(self):
        return {
            'name': self.name,
            'macaddress': self.macAddress
        }

############### Routes ###############
# Routes required: getTimeTable(), login, 

@app.route('/timetable', methods=['POST'])
def getTimeTable():
    json = request.json
    enrolment = json['enrolment']
    data = db.session.query(TimeTable).join(User, enrolment == User.enrolment).all()
    print("length: ",len(data))
    response = []
    for row in data:
        response.append(row.serialize())
    return jsonify(response)


@app.route('/login', methods=['POST'])
def login():
    # TODO: add authorization
    json = request.json
    enrolment = json['enrolment']
    password = json['password']
    isValid = False
    data = db.session.query(User).filter(User.enrolment == enrolment).all()
    for user in data:
        if user.password == password:
            isValid = True
            break
    return jsonify(isValid)

@app.route('/markAttendance', methods=['POST'])
def markAttendance():
    json = request.json
    enrolment = json['enrolment']
    macAddress = json['macaddress']
    subject = json['subject']
    data = db.session.query(TimeTable).filter(TimeTable.enrolment == enrolment, TimeTable.subject == subject).all()
    for timetable in data:
        print(timetable)
    return jsonify("Testing")

if __name__ == '__main__':
    app.run(debug=True)