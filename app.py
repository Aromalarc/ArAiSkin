from flask import Flask, render_template, request, redirect, flash
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from dotenv import load_dotenv
import pandas as pd
import pickle
import os
from datetime import datetime
import logging

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database connection with error handling
def get_db_connection():
    try:
        client = MongoClient(
            os.getenv('MONGODB_URI', "mongodb+srv://aromalsbabu507:Aromal0292@skincare.fw5axg4.mongodb.net/?retryWrites=true&w=majority&appName=Skincare"),
            connectTimeoutMS=10000,
            socketTimeoutMS=None,
            serverSelectionTimeoutMS=5000
        )
        client.admin.command('ping')  # Test connection
        db = client["skin_diagnosis"]
        return db
    except (ConnectionFailure, OperationFailure) as e:
        logger.error(f"Database connection failed: {e}")
        return None

# Load ML model with error handling
try:
    with open("skin_disease_rf_model.pkl", "rb") as f:
        model = pickle.load(f)
    logger.info("ML model loaded successfully")
except Exception as e:
    logger.error(f"Error loading model: {e}")
    model = None

# Constants (moved to top for better organization)
FEATURE_NAMES = [
    "erythema", "scaling", "definite_borders", "itching", "koebner_phenomenon",
    # ... (rest of your feature names)
    "age"
]

SYMPTOM_LABELS = {
    "erythema": "Redness of skin",
    # ... (rest of your symptom labels)
}

# ... (rest of your constants like skindisease_prediction_with_creams, etc.)

@app.route('/')
def index():
    if not model:
        flash("Diagnosis system is currently unavailable", "error")
    return render_template('index.html', symptoms=FEATURE_NAMES[:-1], symptom_labels=SYMPTOM_LABELS)

@app.route('/add', methods=['POST'])
def add_patient():
    if not model:
        flash("Diagnosis system is currently unavailable", "error")
        return redirect('/')
    
    try:
        # Input validation
        name = request.form.get('name', '').strip()
        if not name or len(name) > 100:
            flash("Please enter a valid name (1-100 characters)", "error")
            return redirect('/')
        
        try:
            age = int(request.form.get('age', 0))
            if not (1 <= age <= 120):
                raise ValueError
        except ValueError:
            flash("Please enter a valid age (1-120)", "error")
            return redirect('/')

        # Process symptoms
        input_vector = []
        for feat in FEATURE_NAMES[:-1]:  # exclude age
            val = int(request.form.get(f"symptoms[{feat}]", 0))
            input_vector.append(val)
        input_vector.append(age)

        # Make prediction
        input_df = pd.DataFrame([input_vector], columns=FEATURE_NAMES)
        pred = model.predict(input_df)[0]

        # Get treatment info
        disease, cream, usage = skindisease_prediction_with_creams.get(
            pred, ("Unknown", "Consult Dermatologist", "N/A"))
        
        # Store patient data
        patient_data = {
            'name': name,
            'age': age,
            'disease': disease,
            'cream': cream,
            'readable_disease': disease_fullnames.get(disease, disease),
            'readable_cream': cream_details.get(cream, cream),
            'usage': usage,
            'created_at': datetime.utcnow()
        }

        db = get_db_connection()
        if db:
            db.patients.insert_one(patient_data)
            flash("Patient record added successfully!", "success")
        else:
            flash("Database connection failed", "error")

        return redirect('/records')

    except Exception as e:
        logger.error(f"Error in add_patient: {e}")
        flash("An error occurred while processing your request", "error")
        return redirect('/')

@app.route('/records')
def show_records():
    try:
        db = get_db_connection()
        if db:
            patients = list(db.patients.find().sort("created_at", -1).limit(100))
            return render_template('records.html', patients=patients)
        else:
            flash("Database connection failed", "error")
            return render_template('records.html', patients=[])
    except Exception as e:
        logger.error(f"Error in show_records: {e}")
        flash("An error occurred while retrieving records", "error")
        return render_template('records.html', patients=[])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
