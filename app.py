from flask import Flask, render_template, request, redirect
import numpy as np
import pickle

app = Flask(__name__)
patients = []

# Load model
with open("skin_disease_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

# Symptom feature list (ordered)
feature_names = [
    "erythema", "scaling", "definite_borders", "itching", "koebner_phenomenon",
    "polygonal_papules", "follicular_papules", "oral_mucosal_involvement",
    "knee_and_elbow_involvement", "scalp_involvement", "family_history",
    "melanin_incontinence", "eosinophils_infiltrate", "PNL_infiltrate",
    "fibrosis_papillary_dermis", "exocytosis", "acanthosis", "hyperkeratosis",
    "parakeratosis", "clubbing_rete_ridges", "elongation_rete_ridges",
    "thinning_suprapapillary_epidermis", "spongiform_pustule", "munro_microabcess",
    "focal_hypergranulosis", "disappearance_granular_layer",
    "vacuolisation_damage_basal_layer", "spongiosis", "saw_tooth_appearance_retes",
    "follicular_horn_plug", "perifollicular_parakeratosis",
    "inflammatory_mononuclear_infiltrate", "band_like_infiltrate", "age"
]

# Human-readable labels for symptoms
symptom_labels = {
    "erythema": "Redness of skin",
    "scaling": "Dry, flaky skin",
    "definite_borders": "Well-defined rash edges",
    "itching": "Itching sensation",
    "koebner_phenomenon": "Rash formation after skin trauma",
    "polygonal_papules": "Flat-topped bumps",
    "follicular_papules": "Bumps around hair follicles",
    "oral_mucosal_involvement": "Involvement of mouth lining",
    "knee_and_elbow_involvement": "Affects knees and elbows",
    "scalp_involvement": "Scalp affected",
    "family_history": "Family history of skin condition",
    "melanin_incontinence": "Pigment leaks into lower skin",
    "eosinophils_infiltrate": "Eosinophil cell buildup",
    "PNL_infiltrate": "Polymorphonuclear leukocytes present",
    "fibrosis_papillary_dermis": "Thickening of upper skin layer",
    "exocytosis": "White blood cell movement into skin",
    "acanthosis": "Skin thickening",
    "hyperkeratosis": "Thick outer skin layer",
    "parakeratosis": "Retained nuclei in skin layers",
    "clubbing_rete_ridges": "Swollen epidermal ridges",
    "elongation_rete_ridges": "Extended epidermal ridges",
    "thinning_suprapapillary_epidermis": "Thin skin between ridges",
    "spongiform_pustule": "Fluid-filled skin lesion",
    "munro_microabcess": "White cell collection in skin",
    "focal_hypergranulosis": "Thickened granular skin spots",
    "disappearance_granular_layer": "Missing granular layer",
    "vacuolisation_damage_basal_layer": "Damage to skin base",
    "spongiosis": "Skin swelling between cells",
    "saw_tooth_appearance_retes": "Saw-toothed ridges",
    "follicular_horn_plug": "Blocked hair follicles",
    "perifollicular_parakeratosis": "Disorder around hair follicles",
    "inflammatory_mononuclear_infiltrate": "Single-nucleus immune cells in skin",
    "band_like_infiltrate": "Flat area of immune cells"
}

skindisease_prediction_with_creams = {
    1: ("Psoriasis", "Betamethasone", "Apply thinly once daily"),
    2: ("Seborrheic Dermatitis", "Clobetasol", "Apply twice daily for 2 weeks"),
    3: ("Lichen Planus", "Hydrocortisone", "Apply 2-3 times daily"),
    4: ("Pityriasis Rosea", "Tacrolimus", "Apply once daily"),
    5: ("Chronic Dermatitis", "Mometasone", "Apply once daily at night"),
    # ...
}

# ✅ Add readable disease descriptions
disease_fullnames = {
    "Psoriasis": "Psoriasis – a chronic autoimmune skin condition",
    "Lichen Planus": "Lichen Planus – itchy, purple-colored rashes",
    "Chronic Dermatitis": "Chronic Dermatitis – persistent skin inflammation",
    "Seborrheic Dermatitis": "Seborrheic Dermatitis – oily, flaky patches on scalp/face"
}

# ✅ Add readable cream descriptions
cream_details = {
    "Betamethasone": "Betamethasone – a strong corticosteroid to reduce inflammation",
    "Hydrocortisone": "Hydrocortisone – mild steroid for rashes and itching",
    "Mometasone": "Mometasone – steroid for eczema and chronic dermatitis",
    "Clobetasol": "Clobetasol – very potent corticosteroid for severe skin conditions"
}

@app.route('/')
def index():
    return render_template('index.html', symptoms=feature_names[:-1], symptom_labels=symptom_labels)

@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = int(request.form['age'])
    symptoms_raw = request.form.getlist('symptoms')

    # Ensure all symptoms are collected from form
    input_vector = []
    for feat in feature_names[:-1]:  # exclude age
        val = int(request.form.get(f"symptoms[{feat}]", 0))
        input_vector.append(val)
    input_vector.append(age)

    pred = model.predict([input_vector])[0]
    disease, cream, usage = skindisease_prediction_with_creams.get(pred, ("Unknown", "Consult Dermatologist", "N/A"))

    readable_disease = disease_fullnames.get(disease, disease)
    readable_cream = cream_details.get(cream, cream)

    patient_data = {
        'id': len(patients) + 1,
        'name': name,
        'age': age,
        'disease': disease,
        'cream': cream,
        'readable_disease': readable_disease,
        'readable_cream': readable_cream,
        'usage': usage
    }

    patients.append(patient_data)
    return redirect('/records')

@app.route('/records')
def show_records():
    return render_template('records.html', patients=patients)

if __name__ == '__main__':
    app.run(debug=True)
