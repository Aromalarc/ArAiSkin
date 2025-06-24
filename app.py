# from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# import numpy as np
# import pandas as pd
# import pickle
# import os

# load_dotenv()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# with open("skin_disease_rf_model.pkl", "rb") as f:
#     model = pickle.load(f)

# class Patient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     age = db.Column(db.Integer)
#     disease = db.Column(db.String(100))
#     cream = db.Column(db.String(100))
#     readable_disease = db.Column(db.Text)
#     readable_cream = db.Column(db.Text)
#     usage = db.Column(db.String(200))

# with app.app_context():
#     db.create_all()

# feature_names = [
#     "erythema", "scaling", "definite_borders", "itching", "koebner_phenomenon",
#     "polygonal_papules", "follicular_papules", "oral_mucosal_involvement",
#     "knee_and_elbow_involvement", "scalp_involvement", "family_history",
#     "melanin_incontinence", "eosinophils_infiltrate", "PNL_infiltrate",
#     "fibrosis_papillary_dermis", "exocytosis", "acanthosis", "hyperkeratosis",
#     "parakeratosis", "clubbing_rete_ridges", "elongation_rete_ridges",
#     "thinning_suprapapillary_epidermis", "spongiform_pustule", "munro_microabcess",
#     "focal_hypergranulosis", "disappearance_granular_layer",
#     "vacuolisation_damage_basal_layer", "spongiosis", "saw_tooth_appearance_retes",
#     "follicular_horn_plug", "perifollicular_parakeratosis",
#     "inflammatory_mononuclear_infiltrate", "band_like_infiltrate", "age"
# ]

# symptom_labels = {
#     "erythema": "Redness of skin",
#     "scaling": "Dry, flaky skin",
#     "definite_borders": "Well-defined rash edges",
#     "itching": "Itching sensation",
#     "koebner_phenomenon": "Rash formation after skin trauma",
#     "polygonal_papules": "Flat-topped bumps",
#     "follicular_papules": "Bumps around hair follicles",
#     "oral_mucosal_involvement": "Involvement of mouth lining",
#     "knee_and_elbow_involvement": "Affects knees and elbows",
#     "scalp_involvement": "Scalp affected",
#     "family_history": "Family history of skin condition",
#     "melanin_incontinence": "Pigment leaks into lower skin",
#     "eosinophils_infiltrate": "Eosinophil cell buildup",
#     "PNL_infiltrate": "Polymorphonuclear leukocytes present",
#     "fibrosis_papillary_dermis": "Thickening of upper skin layer",
#     "exocytosis": "White blood cell movement into skin",
#     "acanthosis": "Skin thickening",
#     "hyperkeratosis": "Thick outer skin layer",
#     "parakeratosis": "Retained nuclei in skin layers",
#     "clubbing_rete_ridges": "Swollen epidermal ridges",
#     "elongation_rete_ridges": "Extended epidermal ridges",
#     "thinning_suprapapillary_epidermis": "Thin skin between ridges",
#     "spongiform_pustule": "Fluid-filled skin lesion",
#     "munro_microabcess": "White cell collection in skin",
#     "focal_hypergranulosis": "Thickened granular skin spots",
#     "disappearance_granular_layer": "Missing granular layer",
#     "vacuolisation_damage_basal_layer": "Damage to skin base",
#     "spongiosis": "Skin swelling between cells",
#     "saw_tooth_appearance_retes": "Saw-toothed ridges",
#     "follicular_horn_plug": "Blocked hair follicles",
#     "perifollicular_parakeratosis": "Disorder around hair follicles",
#     "inflammatory_mononuclear_infiltrate": "Single-nucleus immune cells in skin",
#     "band_like_infiltrate": "Flat area of immune cells"
# }

# skindisease_prediction_with_creams = {
#     1: ("Psoriasis", "Betamethasone", "Apply thinly once daily"),
#     2: ("Seborrheic Dermatitis", "Clobetasol", "Apply twice daily for 2 weeks"),
#     3: ("Lichen Planus", "Hydrocortisone", "Apply 2-3 times daily"),
#     4: ("Pityriasis Rosea", "Tacrolimus", "Apply once daily"),
#     5: ("Chronic Dermatitis", "Mometasone", "Apply once daily at night"),
# }

# disease_fullnames = {
#     "Psoriasis": "Psoriasis – a chronic autoimmune skin condition",
#     "Lichen Planus": "Lichen Planus – itchy, purple-colored rashes",
#     "Chronic Dermatitis": "Chronic Dermatitis – persistent skin inflammation",
#     "Seborrheic Dermatitis": "Seborrheic Dermatitis – oily, flaky patches on scalp/face",
#     "Pityriasis Rosea": "Pityriasis Rosea – a self-limiting skin rash often shaped like a Christmas tree"
# }

# cream_details = {
#     "Betamethasone": "Betamethasone – a strong corticosteroid to reduce inflammation",
#     "Hydrocortisone": "Hydrocortisone – mild steroid for rashes and itching",
#     "Mometasone": "Mometasone – steroid for eczema and chronic dermatitis",
#     "Clobetasol": "Clobetasol – very potent corticosteroid for severe skin conditions",
#     "Tacrolimus": "Tacrolimus – a non-steroidal anti-inflammatory cream for sensitive skin areas"
# }

# @app.route('/')
# def index():
#     return render_template('index.html', symptoms=feature_names[:-1], symptom_labels=symptom_labels)

# @app.route('/add', methods=['POST'])
# def add_patient():
#     name = request.form['name']
#     age = int(request.form['age'])

#     input_vector = []
#     for feat in feature_names[:-1]:
#         val = int(request.form.get(f"symptoms[{feat}]", 0))
#         input_vector.append(val)
#     input_vector.append(age)

#     input_df = pd.DataFrame([input_vector], columns=feature_names)
#     pred = model.predict(input_df)[0]

#     disease, cream, usage = skindisease_prediction_with_creams.get(pred, ("Unknown", "Consult Dermatologist", "N/A"))
#     readable_disease = disease_fullnames.get(disease, disease)
#     readable_cream = cream_details.get(cream, cream)

#     patient = Patient(
#         name=name,
#         age=age,
#         disease=disease,
#         cream=cream,
#         readable_disease=readable_disease,
#         readable_cream=readable_cream,
#         usage=usage
#     )
#     db.session.add(patient)
#     db.session.commit()
#     return redirect('/records')

# @app.route('/records')
# def show_records():
#     patients = Patient.query.all()
#     return render_template('records.html', patients=patients)

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5000)

#2

# from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from dotenv import load_dotenv
# import numpy as np
# import pandas as pd
# import pickle
# import os

# load_dotenv()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# with open("skin_disease_rf_model.pkl", "rb") as f:
#     model = pickle.load(f)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# class Patient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     name = db.Column(db.String(100))
#     age = db.Column(db.Integer)
#     disease = db.Column(db.String(100))
#     cream = db.Column(db.String(100))
#     readable_disease = db.Column(db.Text)
#     readable_cream = db.Column(db.Text)
#     usage = db.Column(db.String(200))

# with app.app_context():
#     db.create_all()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# feature_names = [
#     "erythema", "scaling", "definite_borders", "itching", "koebner_phenomenon",
#     "polygonal_papules", "follicular_papules", "oral_mucosal_involvement",
#     "knee_and_elbow_involvement", "scalp_involvement", "family_history",
#     "melanin_incontinence", "eosinophils_infiltrate", "PNL_infiltrate",
#     "fibrosis_papillary_dermis", "exocytosis", "acanthosis", "hyperkeratosis",
#     "parakeratosis", "clubbing_rete_ridges", "elongation_rete_ridges",
#     "thinning_suprapapillary_epidermis", "spongiform_pustule", "munro_microabcess",
#     "focal_hypergranulosis", "disappearance_granular_layer",
#     "vacuolisation_damage_basal_layer", "spongiosis", "saw_tooth_appearance_retes",
#     "follicular_horn_plug", "perifollicular_parakeratosis",
#     "inflammatory_mononuclear_infiltrate", "band_like_infiltrate", "age"
# ]

# symptom_labels = {
#     "erythema": "Redness of skin",
#     "scaling": "Dry, flaky skin",
#     "definite_borders": "Well-defined rash edges",
#     "itching": "Itching sensation",
#     "koebner_phenomenon": "Rash formation after skin trauma",
#     "polygonal_papules": "Flat-topped bumps",
#     "follicular_papules": "Bumps around hair follicles",
#     "oral_mucosal_involvement": "Involvement of mouth lining",
#     "knee_and_elbow_involvement": "Affects knees and elbows",
#     "scalp_involvement": "Scalp affected",
#     "family_history": "Family history of skin condition",
#     "melanin_incontinence": "Pigment leaks into lower skin",
#     "eosinophils_infiltrate": "Eosinophil cell buildup",
#     "PNL_infiltrate": "Polymorphonuclear leukocytes present",
#     "fibrosis_papillary_dermis": "Thickening of upper skin layer",
#     "exocytosis": "White blood cell movement into skin",
#     "acanthosis": "Skin thickening",
#     "hyperkeratosis": "Thick outer skin layer",
#     "parakeratosis": "Retained nuclei in skin layers",
#     "clubbing_rete_ridges": "Swollen epidermal ridges",
#     "elongation_rete_ridges": "Extended epidermal ridges",
#     "thinning_suprapapillary_epidermis": "Thin skin between ridges",
#     "spongiform_pustule": "Fluid-filled skin lesion",
#     "munro_microabcess": "White cell collection in skin",
#     "focal_hypergranulosis": "Thickened granular skin spots",
#     "disappearance_granular_layer": "Missing granular layer",
#     "vacuolisation_damage_basal_layer": "Damage to skin base",
#     "spongiosis": "Skin swelling between cells",
#     "saw_tooth_appearance_retes": "Saw-toothed ridges",
#     "follicular_horn_plug": "Blocked hair follicles",
#     "perifollicular_parakeratosis": "Disorder around hair follicles",
#     "inflammatory_mononuclear_infiltrate": "Single-nucleus immune cells in skin",
#     "band_like_infiltrate": "Flat area of immune cells"
# }

# skindisease_prediction_with_creams = {
#     1: ("Psoriasis", "Betamethasone", "Apply thinly once daily"),
#     2: ("Seborrheic Dermatitis", "Clobetasol", "Apply twice daily for 2 weeks"),
#     3: ("Lichen Planus", "Hydrocortisone", "Apply 2-3 times daily"),
#     4: ("Pityriasis Rosea", "Tacrolimus", "Apply once daily"),
#     5: ("Chronic Dermatitis", "Mometasone", "Apply once daily at night"),
# }

# disease_fullnames = {
#     "Psoriasis": "Psoriasis – a chronic autoimmune skin condition",
#     "Lichen Planus": "Lichen Planus – itchy, purple-colored rashes",
#     "Chronic Dermatitis": "Chronic Dermatitis – persistent skin inflammation",
#     "Seborrheic Dermatitis": "Seborrheic Dermatitis – oily, flaky patches on scalp/face",
#     "Pityriasis Rosea": "Pityriasis Rosea – a self-limiting skin rash often shaped like a Christmas tree"
# }

# cream_details = {
#     "Betamethasone": "Betamethasone – a strong corticosteroid to reduce inflammation",
#     "Hydrocortisone": "Hydrocortisone – mild steroid for rashes and itching",
#     "Mometasone": "Mometasone – steroid for eczema and chronic dermatitis",
#     "Clobetasol": "Clobetasol – very potent corticosteroid for severe skin conditions",
#     "Tacrolimus": "Tacrolimus – a non-steroidal anti-inflammatory cream for sensitive skin areas"
# }

# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html', symptoms=feature_names[:-1], symptom_labels=symptom_labels)

# @app.route('/add', methods=['POST'])
# @login_required
# def add_patient():
#     name = request.form['name']
#     age = int(request.form['age'])

#     input_vector = []
#     for feat in feature_names[:-1]:
#         val = int(request.form.get(f"symptoms[{feat}]", 0))
#         input_vector.append(val)
#     input_vector.append(age)

#     input_df = pd.DataFrame([input_vector], columns=feature_names)
#     pred = model.predict(input_df)[0]

#     disease, cream, usage = skindisease_prediction_with_creams.get(pred, ("Unknown", "Consult Dermatologist", "N/A"))
#     readable_disease = disease_fullnames.get(disease, disease)
#     readable_cream = cream_details.get(cream, cream)

#     patient = Patient(
#         user_id=current_user.id,
#         name=name,
#         age=age,
#         disease=disease,
#         cream=cream,
#         readable_disease=readable_disease,
#         readable_cream=readable_cream,
#         usage=usage
#     )
#     db.session.add(patient)
#     db.session.commit()
#     return redirect('/records')

# @app.route('/records')
# @login_required
# def show_records():
#     patients = Patient.query.filter_by(user_id=current_user.id).all()
#     return render_template('records.html', patients=patients)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = generate_password_hash(request.form['password'])

#         if User.query.filter_by(username=username).first():
#             return "Username already exists!"

#         new_user = User(username=username, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect('/login')

#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()

#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             return redirect('/')
#         else:
#             return "Invalid credentials!"

#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/login')

# if __name__ == '__main__':
#     app.run(debug=True, host="0.0.0.0", port=5000)

#3  
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with open("skin_disease_rf_model.pkl", "rb") as f:
    model = pickle.load(f)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    disease = db.Column(db.String(100))
    cream = db.Column(db.String(100))
    readable_disease = db.Column(db.Text)
    readable_cream = db.Column(db.Text)
    usage = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
}

disease_fullnames = {
    "Psoriasis": "Psoriasis – a chronic autoimmune skin condition",
    "Lichen Planus": "Lichen Planus – itchy, purple-colored rashes",
    "Chronic Dermatitis": "Chronic Dermatitis – persistent skin inflammation",
    "Seborrheic Dermatitis": "Seborrheic Dermatitis – oily, flaky patches on scalp/face",
    "Pityriasis Rosea": "Pityriasis Rosea – a self-limiting skin rash often shaped like a Christmas tree"
}

cream_details = {
    "Betamethasone": "Betamethasone – a strong corticosteroid to reduce inflammation",
    "Hydrocortisone": "Hydrocortisone – mild steroid for rashes and itching",
    "Mometasone": "Mometasone – steroid for eczema and chronic dermatitis",
    "Clobetasol": "Clobetasol – very potent corticosteroid for severe skin conditions",
    "Tacrolimus": "Tacrolimus – a non-steroidal anti-inflammatory cream for sensitive skin areas"
}


@app.route('/')
@login_required
def index():
    return render_template('index.html', symptoms=feature_names[:-1], symptom_labels=symptom_labels)

@app.route('/add', methods=['POST'])
@login_required
def add_patient():
    name = request.form['name']
    age = int(request.form['age'])
    input_vector = [int(request.form.get(f"symptoms[{feat}]", 0)) for feat in feature_names[:-1]]
    total_symptom_score = sum(input_vector)
    input_vector.append(age)

    if total_symptom_score == 0:
        disease = "You are fine"
        cream = "No cream needed"
        usage = "N/A"
        readable_disease = "You are fine. No signs of skin disease detected."
        readable_cream = "No medication required."
    else:
        input_df = pd.DataFrame([input_vector], columns=feature_names)
        pred = model.predict(input_df)[0]
        disease, cream, usage = skindisease_prediction_with_creams.get(pred, ("Unknown", "Consult Dermatologist", "N/A"))
        readable_disease = disease_fullnames.get(disease, disease)
        readable_cream = cream_details.get(cream, cream)

    patient = Patient(
        user_id=current_user.id,
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
@login_required
def show_records():
    patients = Patient.query.filter_by(user_id=current_user.id).all()
    return render_template('records.html', patients=patients)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        if User.query.filter_by(email=email).first():
            return "Email already exists!"

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')
    
    @app.route('/delete/<int:patient_id>', methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.filter_by(id=patient_id, user_id=current_user.id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
    return redirect('/records')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            return "Invalid credentials!"

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

#4
# from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from dotenv import load_dotenv
# from datetime import datetime
# import numpy as np
# import pandas as pd
# import pickle
# import os

# load_dotenv()

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# with open("skin_disease_rf_model.pkl", "rb") as f:
#     model = pickle.load(f)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     password = db.Column(db.String(200), nullable=False)

# class Patient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     name = db.Column(db.String(100))
#     age = db.Column(db.Integer)
#     disease = db.Column(db.String(100))
#     cream = db.Column(db.String(100))
#     readable_disease = db.Column(db.Text)
#     readable_cream = db.Column(db.Text)
#     usage = db.Column(db.String(200))
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

# with app.app_context():
#     db.create_all()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# # Feature list, symptom labels, predictions, cream details unchanged...

# @app.route('/')
# @login_required
# def index():
#     return render_template('index.html', symptoms=feature_names[:-1], symptom_labels=symptom_labels)

# @app.route('/add', methods=['POST'])
# @login_required
# def add_patient():
#     name = request.form['name']
#     age = int(request.form['age'])

#     input_vector = []
#     total_symptom_score = 0

#     for feat in feature_names[:-1]:
#         val = int(request.form.get(f"symptoms[{feat}]", 0))
#         input_vector.append(val)
#         total_symptom_score += val

#     input_vector.append(age)

#     if total_symptom_score == 0:
#         disease = "You are fine"
#         cream = "No cream needed"
#         usage = "N/A"
#         readable_disease = "You are fine. No signs of skin disease detected."
#         readable_cream = "No medication required."
#     else:
#         input_df = pd.DataFrame([input_vector], columns=feature_names)
#         pred = model.predict(input_df)[0]
#         disease, cream, usage = skindisease_prediction_with_creams.get(pred, ("Unknown", "Consult Dermatologist", "N/A"))
#         readable_disease = disease_fullnames.get(disease, disease)
#         readable_cream = cream_details.get(cream, cream)

#     patient = Patient(
#         user_id=current_user.id,
#         name=name,
#         age=age,
#         disease=disease,
#         cream=cream,
#         readable_disease=readable_disease,
#         readable_cream=readable_cream,
#         usage=usage
#     )
#     db.session.add(patient)
#     db.session.commit()
#     return redirect('/records')

# @app.route('/records')
# @login_required
# def show_records():
#     patients = Patient.query.filter_by(user_id=current_user.id).order_by(Patient.created_at.desc()).all()
#     return render_template('records.html', patients=patients)

# @app.route('/delete/<int:patient_id>', methods=['POST'])
# @login_required
# def delete_patient(patient_id):
#     patient = Patient.query.filter_by(id=patient_id, user_id=current_user.id).first()
#     if patient:
#         db.session.delete(patient)
#         db.session.commit()
#     return redirect('/records')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = generate_password_hash(request.form['password'])

#         if User.query.filter_by(email=email).first():
#             return "Email already exists!"

#         new_user = User(email=email, password=password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect('/login')

#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(email=email).first()
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             return redirect('/')
#         else:
#             return "Invalid credentials!"

#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect('/login')

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(debug=True, host="0.0.0.0", port=port)
