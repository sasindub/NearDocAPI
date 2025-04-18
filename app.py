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
        "isAvailableToday": True,
        "email": "doctor@example.com",
        "password": "doctor123",
        "profileImage": "doctor1"
    },
    {
        "id": "2",
        "name": "Dr. Sarah Johnson",
        "specialization": "Heart Center",
        "hospital": "CardioHealth Hospital",
        "rating": 4.8,
        "availability": "Tues, Wed, Thurs",
        "time": "09:00 AM - 3:00 PM",
        "isAvailableToday": False,
        "email": "sarah@example.com",
        "password": "sarah123",
        "profileImage": "doctor2"
    },
    {
        "id": "3",
        "name": "Dr. Michael Chen",
        "specialization": "Neurology",
        "hospital": "Brain & Spine Center",
        "rating": 4.7,
        "availability": "Mon, Wed, Fri",
        "time": "11:00 AM - 6:00 PM",
        "isAvailableToday": True,
        "email": "michael@example.com",
        "password": "michael123",
        "profileImage": "doctor3"
    },
    {
        "id": "4",
        "name": "Dr. James Wilson",
        "specialization": "Cardiology",
        "hospital": "Heart & Vascular Institute",
        "rating": 4.9,
        "availability": "Mon, Tues, Wed, Thurs, Fri",
        "time": "08:00 AM - 4:00 PM",
        "isAvailableToday": True,
        "email": "james@example.com",
        "password": "james123",
        "profileImage": "doctor4"
    }
]

# Generate some patients
patients = [
    {
        "id": "1",
        "name": "Sarah Johnson",
        "age": 28,
        "gender": "Female",
        "email": "sarah.patient@example.com",
        "phone": "123-456-7890",
        "address": "123 Main St, Medical City",
        "profileImage": "patient1"
    },
    {
        "id": "2",
        "name": "Michael Smith",
        "age": 35,
        "gender": "Male",
        "email": "michael.patient@example.com",
        "phone": "234-567-8901",
        "address": "456 Oak St, Medical City",
        "profileImage": "patient2"
    },
    {
        "id": "3",
        "name": "Emma Davis",
        "age": 42,
        "gender": "Female",
        "email": "emma.patient@example.com",
        "phone": "345-678-9012",
        "address": "789 Pine St, Medical City",
        "profileImage": "patient3"
    },
    {
        "id": "4", 
        "name": "Sara Miller",
        "age": 31,
        "gender": "Female",
        "email": "sara.miller@example.com",
        "phone": "456-789-0123",
        "address": "101 Elm St, Medical City",
        "profileImage": "patient4"
    },
    {
        "id": "5",
        "name": "John Cooper",
        "age": 45,
        "gender": "Male",
        "email": "john.cooper@example.com",
        "phone": "567-890-1234",
        "address": "202 Maple St, Medical City",
        "profileImage": "patient5"
    }
]

# Generate some appointments
today = datetime.now()
appointments = [
    {
        "id": "1",
        "doctorId": "4",
        "doctorName": "Dr. John Smith",
        "patientId": "1",
        "patientName": "Sarah Johnson",
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
        "patientId": "1",
        "patientName": "Michael Smith",
        "specialization": "Heart Center",
        "hospital": "CardioHealth Hospital",
        "date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
        "time": "02:15 PM",
        "status": "upcoming",
        "fee": 150.00
    },
    {
        "id": "3",
        "doctorId": "4",
        "doctorName": "Dr. James Wilson",
        "patientId": "1",
        "patientName": "Sarah Johnson",
        "specialization": "Cardiology",
        "hospital": "Heart & Vascular Institute",
        "date": (today).strftime("%Y-%m-%d"),
        "time": "11:00 AM",
        "status": "in progress",
        "fee": 200.00
    },
    {
        "id": "4",
        "doctorId": "4",
        "doctorName": "Dr. Michael Chen",
        "patientId": "3",
        "patientName": "Emma Davis",
        "specialization": "Neurology",
        "hospital": "Brain & Spine Center",
        "date": (today + timedelta(days=0)).strftime("%Y-%m-%d"),
        "time": "03:30 PM",
        "status": "upcoming",
        "fee": 180.00
    },
    {
        "id": "4",
        "doctorId": "4",
        "doctorName": "Dr. Michael Chen",
        "patientId": "3",
        "patientName": "Emma Davis",
        "specialization": "Neurology",
        "hospital": "Brain & Spine Center",
        "date": (today + timedelta(days=0)).strftime("%Y-%m-%d"),
        "time": "03:30 PM",
        "status": "upcoming",
        "fee": 180.00
    },
    {
        "id": "4",
        "doctorId": "4",
        "doctorName": "Dr. Michael Chen",
        "patientId": "3",
        "patientName": "Emma Davis",
        "specialization": "Neurology",
        "hospital": "Brain & Spine Center",
        "date": (today + timedelta(days=0)).strftime("%Y-%m-%d"),
        "time": "03:30 PM",
        "status": "in progress",
        "fee": 180.00
    },
    {
        "id": "5",
        "doctorId": "4",
        "doctorName": "Dr. James Wilson",
        "patientId": "4",
        "patientName": "Sara Miller",
        "specialization": "Cardiology",
        "hospital": "Heart & Vascular Institute",
        "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "time": "09:45 AM",
        "status": "completed",
        "fee": 120.00
    },
    {
        "id": "6",
        "doctorId": "4",
        "doctorName": "Dr. John Smith",
        "patientId": "5",
        "patientName": "John Cooper",
        "specialization": "Medicine Center",
        "hospital": "MedicalOne Center",
        "date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        "time": "01:30 PM",
        "status": "completed",
        "fee": 90.00
    }
]

notifications = [
    {
        "id": "1",
        "title": "Your appointment is confirmed",
        "message": "Your appointment with Dr. John Smith on April 22, 2025 is confirmed.",
        "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "isRead": True,
        "forDoctor": False
    },
    {
        "id": "2",
        "title": "Reminder: Your turn is approaching",
        "message": "Please be at the MedicalOne Center in the next 30 minutes.",
        "date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        "isRead": False,
        "forDoctor": False
    },
    {
        "id": "3",
        "title": "Prescription updated",
        "message": "Dr. Richard Wilson has updated your prescription. Check medications.",
        "date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
        "isRead": False,
        "forDoctor": False
    },
    {
        "id": "4",
        "title": "Payment successful",
        "message": "Your payment of $120 for appointment with Dr. Susan Taylor has been received.",
        "date": (today - timedelta(days=4)).strftime("%Y-%m-%d"),
        "isRead": True,
        "forDoctor": False
    },
    {
        "id": "5",
        "title": "New appointment booked",
        "message": "Sarah Johnson has booked an appointment for April 19, 2025 at 10:30 AM.",
        "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "isRead": False,
        "forDoctor": True
    },
    {
        "id": "6",
        "title": "Appointment #16 completed successfully",
        "message": "Your appointment with Sara Miller has been marked as completed.",
        "date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        "isRead": True,
        "forDoctor": True
    },
    {
        "id": "7",
        "title": "System Update",
        "message": "New features have been added to your doctor portal. Please check.",
        "date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),
        "isRead": False,
        "forDoctor": True
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

# Prescriptions for patients
prescriptions = [
    {
        "id": "1",
        "doctorId": "4",
        "doctorName": "Dr. James Wilson",
        "patientId": "1",
        "patientName": "Sarah Johnson",
        "date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),
        "medications": [
            {
                "name": "Acute Bronchiolitis",
                "dosage": "10 days",
                "instructions": "Take with food"
            }
        ],
        "notes": "Patient should avoid strenuous activity for the next week."
    },
    {
        "id": "2",
        "doctorId": "1",
        "doctorName": "Dr. John Smith",
        "patientId": "2",
        "patientName": "Michael Smith",
        "date": (today - timedelta(days=10)).strftime("%Y-%m-%d"),
        "medications": [
            {
                "name": "Lisinopril",
                "dosage": "10mg",
                "instructions": "Take once daily"
            },
            {
                "name": "Metformin",
                "dosage": "500mg",
                "instructions": "Take twice daily with meals"
            }
        ],
        "notes": "Follow up in 30 days to check blood pressure."
    }
]

# Doctor availability schedule
availability = {
    "1": {  # Dr. John Smith
        "morning": {
            "available": True,
            "startTime": "08:00 AM",
            "endTime": "12:00 PM"
        },
        "evening": {
            "available": True,
            "startTime": "04:00 PM",
            "endTime": "08:00 PM"
        },
        "maxAppointments": 12
    },
    "4": {  # Dr. James Wilson
        "morning": {
            "available": True,
            "startTime": "09:00 AM",
            "endTime": "12:00 PM"
        },
        "evening": {
            "available": True,
            "startTime": "01:00 PM",
            "endTime": "05:00 PM"
        },
        "maxAppointments": 8
    }
}

# Earnings data for doctors
earnings = {
    "4": {  # Dr. James Wilson
        "today": 300.00,
        "total": 3200.00,
        "recent": [
            {
                "patientName": "Sarah Johnson",
                "date": (today).strftime("%Y-%m-%d"),
                "time": "10:30 AM",
                "amount": 120.00
            },
            {
                "patientName": "Michael Smith",
                "date": (today).strftime("%Y-%m-%d"),
                "time": "01:30 PM",
                "amount": 140.00
            },
            {
                "patientName": "Emma Davis",
                "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
                "time": "11:30 AM",
                "amount": 160.00
            }
        ]
    }
}

# Users for login (both patients and doctors)
users = [
    {
        "email": "saman@gmail.com",
        "password": "password123",
        "userType": "patient",
        "token": "patient-token-12345",
        "userId": "1"
    },
    {
        "email": "jon@gmail.com",
        "password": "doctor123",
        "userType": "doctor",
        "token": "doctor-token-67890",
        "userId": "1"
    },
    {
        "email": "jam@gmail.com",
        "password": "jam123",
        "userType": "doctor",
        "token": "doctor-token-james",
        "userId": "4"
    }
]

# API Routes - Patient Routes
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
                "userType": user['userType'],
                "userId": user['userId'],
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
        "userType": "patient",
        "userId": str(len(patients) + 1),
        "message": "Registration successful"
    })

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    # Check if we're filtering by doctor or patient
    doctor_id = request.args.get('doctorId')
    patient_id = request.args.get('patientId')
    status = request.args.get('status')
    
    filtered_appointments = appointments
    
    if doctor_id:
        filtered_appointments = [a for a in filtered_appointments if a['doctorId'] == doctor_id]
    
    if patient_id:
        filtered_appointments = [a for a in filtered_appointments if a['patientId'] == patient_id]
        
    if status:
        filtered_appointments = [a for a in filtered_appointments if a['status'] == status]
        
    return jsonify(filtered_appointments)

@app.route('/api/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    new_appointment = {
        "id": str(len(appointments) + 1),
        "doctorId": data.get('doctorId'),
        "doctorName": next((d['name'] for d in doctors if d['id'] == data.get('doctorId')), "Unknown Doctor"),
        "patientId": data.get('patientId', "1"),
        "patientName": next((p['name'] for p in patients if p['id'] == data.get('patientId', "1")), "Unknown Patient"),
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
    # Check if we're filtering for doctor or patient notifications
    for_doctor = request.args.get('forDoctor', 'false').lower() == 'true'
    
    if for_doctor:
        return jsonify([n for n in notifications if n.get('forDoctor', False)])
    else:
        return jsonify([n for n in notifications if not n.get('forDoctor', False)])

@app.route('/api/medications', methods=['GET'])
def get_medications():
    return jsonify(medications)

# API Routes - Doctor Specific Routes
@app.route('/api/doctor/<doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = next((d for d in doctors if d['id'] == doctor_id), None)
    if doctor:
        # Remove sensitive information like password
        doctor_info = {k: v for k, v in doctor.items() if k != 'password'}
        return jsonify(doctor_info)
    return jsonify({"error": "Doctor not found"}), 404

@app.route('/api/patients', methods=['GET'])
def get_patients():
    # Optionally filter by doctor
    doctor_id = request.args.get('doctorId')
    
    if doctor_id:
        # Get patients who have appointments with this doctor
        patient_ids = set(a['patientId'] for a in appointments if a['doctorId'] == doctor_id)
        return jsonify([p for p in patients if p['id'] in patient_ids])
    
    return jsonify(patients)

@app.route('/api/patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = next((p for p in patients if p['id'] == patient_id), None)
    if patient:
        return jsonify(patient)
    return jsonify({"error": "Patient not found"}), 404

@app.route('/api/patient-history/<patient_id>', methods=['GET'])
def get_patient_history(patient_id):
    # Get patient's appointments
    patient_appointments = [a for a in appointments if a['patientId'] == patient_id]
    
    # Get patient's prescriptions
    patient_prescriptions = [p for p in prescriptions if p['patientId'] == patient_id]
    
    return jsonify({
        "appointments": patient_appointments,
        "prescriptions": patient_prescriptions
    })

@app.route('/api/update-appointment-status', methods=['POST'])
def update_appointment_status():
    data = request.json
    appointment_id = data.get('appointmentId')
    new_status = data.get('status')
    
    for a in appointments:
        if a['id'] == appointment_id:
            a['status'] = new_status
            return jsonify({
                "success": True,
                "message": f"Appointment status updated to {new_status}"
            })
    
    return jsonify({
        "success": False,
        "message": "Appointment not found"
    }), 404

@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    # Filter by doctor or patient
    doctor_id = request.args.get('doctorId')
    patient_id = request.args.get('patientId')
    
    filtered_prescriptions = prescriptions
    
    if doctor_id:
        filtered_prescriptions = [p for p in filtered_prescriptions if p['doctorId'] == doctor_id]
    
    if patient_id:
        filtered_prescriptions = [p for p in filtered_prescriptions if p['patientId'] == patient_id]
        
    return jsonify(filtered_prescriptions)

@app.route('/api/add-prescription', methods=['POST'])
def add_prescription():
    data = request.json
    
    new_prescription = {
        "id": str(len(prescriptions) + 1),
        "doctorId": data.get('doctorId'),
        "doctorName": next((d['name'] for d in doctors if d['id'] == data.get('doctorId')), "Unknown Doctor"),
        "patientId": data.get('patientId'),
        "patientName": next((p['name'] for p in patients if p['id'] == data.get('patientId')), "Unknown Patient"),
        "date": data.get('date', today.strftime("%Y-%m-%d")),
        "medications": data.get('medications', []),
        "notes": data.get('notes', "")
    }
    
    prescriptions.append(new_prescription)
    
    return jsonify({
        "success": True,
        "prescriptionId": new_prescription['id'],
        "message": "Prescription added successfully"
    })

@app.route('/api/doctor-availability/<doctor_id>', methods=['GET'])
def get_doctor_availability(doctor_id):
    if doctor_id in availability:
        return jsonify(availability[doctor_id])
    return jsonify({"error": "Availability not found for this doctor"}), 404

@app.route('/api/update-availability', methods=['POST'])
def update_availability():
    data = request.json
    doctor_id = data.get('doctorId')
    
    if doctor_id not in availability:
        availability[doctor_id] = {
            "morning": {"available": False, "startTime": "", "endTime": ""},
            "evening": {"available": False, "startTime": "", "endTime": ""},
            "maxAppointments": 10
        }
    
    # Update morning availability
    if 'morning' in data:
        availability[doctor_id]['morning'] = data['morning']
    
    # Update evening availability
    if 'evening' in data:
        availability[doctor_id]['evening'] = data['evening']
    
    # Update max appointments
    if 'maxAppointments' in data:
        availability[doctor_id]['maxAppointments'] = data['maxAppointments']
    
    return jsonify({
        "success": True,
        "message": "Availability updated successfully"
    })

@app.route('/api/doctor-earnings/<doctor_id>', methods=['GET'])
def get_doctor_earnings(doctor_id):
    if doctor_id in earnings:
        return jsonify(earnings[doctor_id])
    
    # Return empty earnings if doctor has no earnings record
    return jsonify({
        "today": 0,
        "total": 0,
        "recent": []
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
