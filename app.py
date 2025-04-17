from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Static data for the app
doctors = [
    {
        "id": "1",
        "name": "Dr. John Smith",
        "specialization": "Medicine Center",
        "hospital": "MedicalOne Center",
        "rating": 4.5,
        "availability": "Mon, Tues, Wed",
        "time": "10:00 AM - 5:00 PM",
        "isAvailableToday": True
    },
    {
        "id": "2",
        "name": "Dr. Sarah Johnson",
        "specialization": "Heart Center",
        "hospital": "CardioHealth Hospital",
        "rating": 4.8,
        "availability": "Tues, Wed, Thurs",
        "time": "09:00 AM - 3:00 PM",
        "isAvailableToday": False
    },
    {
        "id": "3",
        "name": "Dr. Michael Chen",
        "specialization": "Neurology",
        "hospital": "Brain & Spine Center",
        "rating": 4.7,
        "availability": "Mon, Wed, Fri",
        "time": "11:00 AM - 6:00 PM",
        "isAvailableToday": True
    },
    {
        "id": "4",
        "name": "Dr. Susan Taylor",
        "specialization": "Dermatology",
        "hospital": "SkinCare Clinic",
        "rating": 4.2,
        "availability": "Mon, Thurs, Fri",
        "time": "09:30 AM - 4:30 PM",
        "isAvailableToday": True
    },
    {
        "id": "5",
        "name": "Dr. Saman Kumara",
        "specialization": "Dermatology",
        "hospital": "SkinCare Clinic",
        "rating": 4.2,
        "availability": "Mon, Thurs, Fri",
        "time": "09:30 AM - 4:30 PM",
        "isAvailableToday": True
    }
]

# Generate some appointments
today = datetime.now()
appointments = [
    {
        "id": "1",
        "doctorId": "1",
        "doctorName": "Dr. John Smith",
        "specialization": "Medicine Center",
        "hospital": "MedicalOne Center",
        "date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
        "time": "10:30 AM",
        "status": "upcoming",
        "fee": 100.00
    },
    {
        "id": "2",
        "doctorId": "2",
        "doctorName": "Dr. Sarah Johnson",
        "specialization": "Heart Center",
        "hospital": "CardioHealth Hospital",
        "date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
        "time": "02:15 PM",
        "status": "upcoming",
        "fee": 150.00
    }
]

notifications = [
    {
        "id": "1",
        "title": "Your appointment is confirmed",
        "message": "Your appointment with Dr. John Smith on April 22, 2025 is confirmed.",
        "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "isRead": True
    },
    {
        "id": "2",
        "title": "Reminder: Your turn is approaching",
        "message": "Please be at the MedicalOne Center in the next 30 minutes.",
        "date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        "isRead": False
    },
    {
        "id": "3",
        "title": "Prescription updated",
        "message": "Dr. Richard Wilson has updated your prescription. Check medications.",
        "date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
        "isRead": False
    },
    {
        "id": "4",
        "title": "Payment successful",
        "message": "Your payment of LKR120 for appointment with Dr. Susan Taylor has been received.",
        "date": (today - timedelta(days=4)).strftime("%Y-%m-%d"),
        "isRead": True
    }
]

medications = [
    {
        "id": "1",
        "name": "Amoxicillin",
        "dosage": "500mg",
        "schedule": "Every 8 hours",
        "startDate": (today - timedelta(days=7)).strftime("%Y-%m-%d"),
        "endDate": (today + timedelta(days=7)).strftime("%Y-%m-%d")
    },
    {
        "id": "2",
        "name": "Ibuprofen",
        "dosage": "200mg",
        "schedule": "Every 6 hours as needed",
        "startDate": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
        "endDate": (today + timedelta(days=3)).strftime("%Y-%m-%d")
    },
    {
        "id": "3",
        "name": "Vitamin D",
        "dosage": "1000 IU",
        "schedule": "Once daily",
        "startDate": (today - timedelta(days=30)).strftime("%Y-%m-%d"),
        "endDate": (today + timedelta(days=30)).strftime("%Y-%m-%d")
    }
]

# Users for login
users = [
    {
        "email": "patient@example.com",
        "password": "password123",
        "token": "sample-token-12345"
    }
]

# API Routes
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    for user in users:
        if user['email'] == email and user['password'] == password:
            return jsonify({
                "success": True,
                "token": user['token'],
                "message": "Login successful"
            })
    
    return jsonify({
        "success": False,
        "token": "",
        "message": "Invalid credentials"
    }), 401

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    return jsonify({
        "success": True,
        "token": "new-user-token-67890",
        "message": "Registration successful"
    })

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    return jsonify(appointments)

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    new_appointment = {
        "id": str(len(appointments) + 1),
        "doctorId": data.get('doctorId'),
        "doctorName": next((d['name'] for d in doctors if d['id'] == data.get('doctorId')), "Unknown Doctor"),
        "specialization": next((d['specialization'] for d in doctors if d['id'] == data.get('doctorId')), "Unknown Specialization"),
        "hospital": next((d['hospital'] for d in doctors if d['id'] == data.get('doctorId')), "Unknown Hospital"),
        "date": data.get('date'),
        "time": data.get('time'),
        "status": "upcoming",
        "fee": 120.00
    }
    
    appointments.append(new_appointment)
    
    return jsonify({
        "success": True,
        "appointmentId": new_appointment['id'],
        "message": "Appointment booked successfully"
    })

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    return jsonify(notifications)

@app.route('/api/medications', methods=['GET'])
def get_medications():
    return jsonify(medications)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
