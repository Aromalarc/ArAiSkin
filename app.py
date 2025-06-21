from flask import Flask, render_template, request, redirect
import numpy as np
import pandas as pd
import pickle
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load env vars
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)

# 🔌 Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["skin_disease_app"]
patients_collection = db["patients"]

# Load model
with open("skin_disease_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

# Symptoms, labels, and details (same as yours)
feature_names = [ ... ]  # Keep your existing list
symptom_labels = { ... }
skindisease_prediction_with_creams = { ... }
disease_fullnames = { ... }
cream_details = { ... }

@app.route('/')
def index():
    return render_template('index.html', symptoms=feature_names[:-1], symptom_labels=symptom_labels)

@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = int(request.form['age'])

    input_vector = []
    for feat in feature_names[:-1]:
        val = int(request.form.get(f"symptoms[{feat}]", 0))
        input_vector.append(val)
    input_vector.append(age)

    input_df = pd.DataFrame([input_vector], columns=feature_names)
    pred = model.predict(input_df)[0]

    disease, cream, usage = skindisease_prediction_with_creams.get(pred, ("Unknown", "Consult Dermatologist", "N/A"))
    readable_disease = disease_fullnames.get(disease, disease)
    readable_cream = cream_details.get(cream, cream)

    patient_data = {
        'name': name,
        'age': age,
        'disease': disease,
        'cream': cream,
        'readable_disease': readable_disease,
        'readable_cream': readable_cream,
        'usage': usage
    }

    patients_collection.insert_one(patient_data)
    return redirect('/records')

@app.route('/records')
def show_records():
    patients = list(patients_collection.find())
    return render_template('records.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
