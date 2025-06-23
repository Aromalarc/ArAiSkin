from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import pickle
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load ML model
with open("skin_disease_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

# Database model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    disease = db.Column(db.String(100))
    cream = db.Column(db.String(100))
    readable_disease = db.Column(db.Text)
    readable_cream = db.Column(db.Text)
    usage = db.Column(db.String(200))

# Create DB tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Example features — replace with your actual features
feature_names = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'age']
symptom_labels = {
    'itching': 'Itching',
    'skin_rash': 'Skin Rash',
    'nodal_skin_eruptions': 'Nodal Skin Eruptions'
}
skindisease_prediction_with_creams = {
    0: ("psoriasis", "betamethasone", "Apply twice daily"),
    1: ("acne", "clindamycin", "Apply once at night"),
    2: ("eczema", "hydrocortisone", "Apply in thin layer twice daily")
}
disease_fullnames = {
    "psoriasis": "Psoriasis",
    "acne": "Acne Vulgaris",
    "eczema": "Atopic Dermatitis"
}
cream_details = {
    "betamethasone": "Betamethasone Dipropionate 0.05%",
    "clindamycin": "Clindamycin Phosphate Gel 1%",
    "hydrocortisone": "Hydrocortisone Cream 1%"
}

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

    patient = Patient(
        name=name,
        age=age,
        disease=disease,
        cream=cream,
        readable_disease=readable_disease,
        readable_cream=readable_cream,
        usage=usage
    )
    db.session.add(patient)
    db.session.commit()
    return redirect('/records')

@app.route('/records')
def show_records():
    patients = Patient.query.all()
    return render_template('records.html', patients=patients)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

