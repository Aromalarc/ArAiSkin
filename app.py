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

# PostgreSQL DB connection (edit with your credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:your_password@localhost:5432/skin_diagnosis'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load model
with open("skin_disease_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

# DB model
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    disease = db.Column(db.String(100))
    cream = db.Column(db.String(100))
    readable_disease = db.Column(db.Text)
    readable_cream = db.Column(db.Text)
    usage = db.Column(db.String(200))

# Create tables
@app.before_first_request
def create_tables():
    db.create_all()

# Feature and label definitions
feature_names = [...]
symptom_labels = {...}
skindisease_prediction_with_creams = {...}
disease_fullnames = {...}
cream_details = {...}

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
    app.run(debug=True)
