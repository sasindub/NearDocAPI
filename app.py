from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import uuid
import os
import urllib.parse  # For URL encoding

app = Flask(__name__)

# --- MongoDB Connection Setup ---
username = "sasindulakshithabandara"
password = "Abc@123456789"  # Your original password with special characters

# URL-encode the password
encoded_password = urllib.parse.quote_plus(password)

# Build the MongoDB connection string with TLS parameter for testing
MONGO_URI = (
    f"mongodb+srv://{username}:{encoded_password}@neardoc.qgveabw.mongodb.net/NearDoc"
    "?retryWrites=true&w=majority&appName=NearDoc&tlsAllowInvalidCertificates=true"
)
client = MongoClient(MONGO_URI)
db = client['NearDoc']

# --- Collections ---
patients_col = db['patients']
doctors_col = db['doctors']
medical_centres_col = db['medical_centres']
appointments_col = db['appointments']

# --- Helper Function to Convert ObjectIds ---
def convert_objectids(document):
    """
    Recursively convert any ObjectId in a document (or a list of documents) to its string representation.
    """
    if isinstance(document, list):
        return [convert_objectids(item) for item in document]
    elif isinstance(document, dict):
        new_doc = {}
        for key, value in document.items():
            if isinstance(value, ObjectId):
                new_doc[key] = str(value)
            elif isinstance(value, (dict, list)):
                new_doc[key] = convert_objectids(value)
            else:
                new_doc[key] = value
        return new_doc
    else:
        return document

# --- Fake Data Insertion Function ---
def insert_fake_data():
    # Insert fake Medical Centres if the collection is empty
    if medical_centres_col.count_documents({}) == 0:
        fake_medical_centres = [
            {"_id": "mc1", "name": "Health First Clinic", "address": "123 Main St"},
            {"_id": "mc2", "name": "City Care Hospital", "address": "456 Broadway"},
            {"_id": "mc3", "name": "Wellness Center", "address": "789 Park Ave"}
        ]
        medical_centres_col.insert_many(fake_medical_centres)
        print("Inserted fake Medical Centres.")

    # Insert fake Doctors if collection is empty
    if doctors_col.count_documents({}) == 0:
        fake_doctors = [
            {
                "name": "Dr. Alice",
                "address": "10 Doctor Lane",
                "phone": "1111111111",
                "password": "alice123",
                "age": 40,
                "gender": "Female",
                "zip_code": "10001",
                "dispensary_name": "Health First Clinic",
                "registration_id": "REG001",
                "verification_details": "Verified",
                "medical_centre": {"id": "mc1", "name": "Health First Clinic"},
                "morningTime": {"start_time": "09:00", "end_time": "12:00", "available": True},
                "eveningTime": {"start_time": "14:00", "end_time": "18:00", "available": True}
            },
            {
                "name": "Dr. Bob",
                "address": "20 Medic Way",
                "phone": "2222222222",
                "password": "bob123",
                "age": 45,
                "gender": "Male",
                "zip_code": "10002",
                "dispensary_name": "City Care Hospital",
                "registration_id": "REG002",
                "verification_details": "Verified",
                "medical_centre": {"id": "mc2", "name": "City Care Hospital"},
                "morningTime": {"start_time": "08:30", "end_time": "11:30", "available": True},
                "eveningTime": {"start_time": "15:00", "end_time": "19:00", "available": True}
            },
            {
                "name": "Dr. Carol",
                "address": "30 Health Blvd",
                "phone": "3333333333",
                "password": "carol123",
                "age": 38,
                "gender": "Female",
                "zip_code": "10003",
                "dispensary_name": "Wellness Center",
                "registration_id": "REG003",
                "verification_details": "Verified",
                "medical_centre": {"id": "mc3", "name": "Wellness Center"},
                "morningTime": {"start_time": "10:00", "end_time": "13:00", "available": True},
                "eveningTime": {"start_time": "16:00", "end_time": "20:00", "available": True}
            }
        ]
        doctors_col.insert_many(fake_doctors)
        print("Inserted fake Doctors.")

    # Insert fake Patients if collection is empty (optional)
    if patients_col.count_documents({}) == 0:
        fake_patients = [
            {
                "name": "Patient One",
                "address": "1 First St",
                "phone": "4444444444",
                "password": "patient1",
                "age": 30,
                "gender": "Male",
                "zip_code": "20001",
                "appointments": []
            },
            {
                "name": "Patient Two",
                "address": "2 Second St",
                "phone": "5555555555",
                "password": "patient2",
                "age": 25,
                "gender": "Female",
                "zip_code": "20002",
                "appointments": []
            }
        ]
        patients_col.insert_many(fake_patients)
        print("Inserted fake Patients.")

# Call the fake data insertion function on startup
insert_fake_data()

# --- Root Endpoint to Test Server ---
@app.route('/')
def index():
    return "Flask app is running!"

# --- Patient Endpoints ---

# 1. Patient Registration
@app.route('/patient/register', methods=['POST'])
def patient_register():
    data = request.get_json()
    required_fields = ["name", "address", "phone", "password", "age", "gender", "zip_code"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if patients_col.find_one({"phone": data["phone"]}):
        return jsonify({"error": "Patient with this phone already exists"}), 400

    patients_col.insert_one(data)
    return jsonify({"message": "Patient registered successfully"}), 201

# 2. Patient Login
@app.route('/patient/login', methods=['POST'])
def patient_login():
    data = request.get_json()
    phone = data.get("phone")
    password = data.get("password")
    if not phone or not password:
        return jsonify({"error": "Missing phone or password"}), 400

    patient = patients_col.find_one({"phone": phone, "password": password})
    if patient:
        return jsonify({"message": "Login successful", "patient_id": str(patient["_id"])}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# 3. Book Appointment
@app.route('/patient/book_appointment', methods=['POST'])
def book_appointment():
    data = request.get_json()
    required_fields = ["patient_id", "doctor_id", "date", "time_slot", "appointmentPrice"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    doctor = doctors_col.find_one({"phone": data["doctor_id"]}) or doctors_col.find_one({"_id": data["doctor_id"]})
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404

    appointment_number = str(uuid.uuid4())[:8]

    appointment = {
        "patient_id": data["patient_id"],
        "patient_name": data.get("patient_name", "Unknown"),
        "doctor_appointment": {
            "doctor_name": doctor["name"],
            "doctor_id": doctor.get("_id", doctor.get("phone")),
            "medical_centre_name": doctor["medical_centre"]["name"],
            "medical_centre_id": doctor["medical_centre"]["id"],
            "medicines": data.get("medicines", []),
            "prescription_details": data.get("prescription_details", ""),
            "prescription_image": data.get("prescription_image", ""),
            "special_note": data.get("special_note", ""),
            "appointment_number": appointment_number
        },
        "status": "upcoming",
        "date": data["date"],
        "time_slot": data["time_slot"],
        "appointmentPrice": data["appointmentPrice"]
    }
    result = appointments_col.insert_one(appointment)
    # Update patient's appointments list with the new appointment ID.
    patients_col.update_one(
        {"_id": ObjectId(data["patient_id"])},
        {"$push": {"appointments": result.inserted_id}}
    )
    return jsonify({"message": "Appointment booked", "appointment_number": appointment_number}), 201

# 4. Get Patient Appointments
@app.route('/patient/appointments', methods=['GET'])
def get_appointments():
    patient_id = request.args.get("patient_id")
    if not patient_id:
        return jsonify({"error": "Patient ID is required"}), 400

    appointments = list(appointments_col.find({"patient_id": patient_id}))
    # Recursively convert all ObjectId values to strings
    appointments = convert_objectids(appointments)
    return jsonify({"appointments": appointments}), 200

# 5. Cancel Appointment
@app.route('/patient/cancel_appointment/<appointment_id>', methods=['PUT'])
def cancel_appointment(appointment_id):
    try:
        result = appointments_col.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"status": "cancelled"}}
        )
    except Exception as e:
        return jsonify({"error": "Invalid appointment ID format"}), 400

    if result.matched_count:
        return jsonify({"message": "Appointment cancelled"}), 200
    else:
        return jsonify({"error": "Appointment not found"}), 404

# --- Run the Flask App ---
if __name__ == '__main__':
    app.run(debug=True)
