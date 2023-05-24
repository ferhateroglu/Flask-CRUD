import os
from flask import Flask, render_template, redirect, url_for, jsonify, request
import requests

from database.models import Meeting, db
from utlis.validation_schema import validate_body, validate_id
from utlis.serialization import meeting_schema, meetings_schema
from sqlalchemy import desc

basedir = os.path.abspath(os.path.dirname(__file__))
database_dir = os.path.join(basedir, 'database')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(database_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def home():

    # meetings rout'una istek atma
    meetings = requests.get("http://localhost:5000/meetings")
    meetings = meetings.json()

    return render_template("index.html", meetings=meetings)

# id'ye göre Meeting listeleme
@app.route('/meetings/<int:id>', methods=['GET'])
def get_meeting(id):
    try:
        # request verilerini doğrulama
        validation_errors = validate_id(id)
        if validation_errors:
            return jsonify(validation_errors), 400

        # Meeting nesnesini veritabanından çekme
        meeting = Meeting.query.get(id)
        if meeting:
            result = meeting_schema.dump(meeting)
            # participants değerini diziye dönüştürme
            participants = result['participants']
            result['participants'] = participants.split(", ")
            return jsonify(result)
        else:
            return jsonify(error='Meeting not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500
    
# Tüm Meetingleri listeleme
@app.route('/meetings', methods=['GET'])
def get_meetings():
    try:
        # Tüm meetingleri veritabanından çekme
        meetings = Meeting.query.order_by(desc(Meeting.id)).all()
        result = meetings_schema.dump(meetings)
        # participants değerlerini diziye dönüştürme
        for meeting_data in result:
            participants = meeting_data['participants']
            meeting_data['participants'] = participants.split(", ")
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 500

# Meeting ekleme
@app.route('/meetings', methods=['POST'])
def create_meeting():
    try:
        # request verilerini doğrulama
        validation_errors = validate_body(request, "create_meeting_schema")
        if validation_errors:
            return jsonify(validation_errors), 400

        # Meeting nesnesini oluşturma
        data = request.get_json()
        topic = data['topic']
        date_ = data['date']
        start_time = data['start_time']
        end_time = data['end_time']
        participants = ", ".join(data['participants'])

        # Meeting nesnesini veritabanına ekleme
        meeting = Meeting(topic=topic, date=date_, start_time=start_time, end_time=end_time, participants=participants)
        db.session.add(meeting)
        db.session.commit()

        return redirect(url_for('get_meeting', id=meeting.id))
    except Exception as e:
        return jsonify(error=str(e)), 500

# id'ye göre Meeting güncelleme
@app.route('/meetings/<int:id>', methods=['PUT'])
def update_meeting(id):
    try:

        # request verilerini doğrulama
        validation_errors = validate_id(id)
        if validation_errors:
            return jsonify(validation_errors), 400
        
        validation_errors = validate_body(request, "update_meeting_schema")
        if validation_errors:
            return jsonify(validation_errors), 400
        
        # Meeting nesnesi varsa güncelleme
        meeting = Meeting.query.get(id)
        data = request.get_json()
        if meeting:
            meeting.topic = data['topic']
            meeting.date_ = data['date']
            meeting.start_time = data['start_time']
            meeting.end_time = data['end_time']
            meeting.participants = ", ".join(data['participants'])
            db.session.commit()
            updated_meeting = meeting_schema.dump(meeting)  # Meeting nesnesini schema kullanarak dönüştür
            return jsonify(updated_meeting), 200
        else:
            return jsonify(error='Meeting not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# id'ye göre Meeting silme
@app.route('/meetings/<int:id>', methods=['DELETE'])
def delete_meeting(id):
    try:

        # request verilerini doğrulama
        validation_errors = validate_id(id)
        if validation_errors:
            return jsonify(validation_errors), 400
        
        # Meeting nesnesi varsa silme
        meeting = Meeting.query.get(id)
        if meeting:
            db.session.delete(meeting)
            db.session.commit()
            deleted_meeting = meeting_schema.dump(meeting)  # Meeting nesnesini schema kullanarak dönüştür
            return jsonify(deleted_meeting), 200
        else:
            return jsonify(error='Meeting not found'), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

# 404 route'u
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': 'Not found'}), 404

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
