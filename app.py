import os
import json
import qrcode

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)

from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# ================= APP CONFIG =================

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    'static',
    'uploads',
    'farmer_photos'
)

QR_FOLDER = os.path.join(
    BASE_DIR,
    'static',
    'qr_codes'
)

# CREATE FOLDERS AUTOMATICALLY

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///farmers.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ================= DATABASE MODEL =================

class Farmer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))

    father_name = db.Column(db.String(100))

    mother_name = db.Column(db.String(100))

    address = db.Column(db.Text)

    mobile = db.Column(db.String(15))

    aadhaar = db.Column(db.String(20))

    pan = db.Column(db.String(20))

    kisan_id_1 = db.Column(db.String(50))

    kisan_id_2 = db.Column(db.String(50))

    pm_kisan_id = db.Column(db.String(50))

    account_number = db.Column(db.String(30))

    bank_name = db.Column(db.String(100))

    ifsc_code = db.Column(db.String(20))

    branch_name = db.Column(db.String(100))

    photo = db.Column(db.String(200))

    qr_code = db.Column(db.String(200))

# CREATE DATABASE

with app.app_context():
    db.create_all()

# ================= HOME PAGE =================

@app.route('/')

def home():

    return render_template('index.html')

# ================= REGISTER PAGE =================

@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        try:

            # ================= GET FORM DATA =================

            name = request.form.get('name')

            father_name = request.form.get('father_name')

            mother_name = request.form.get('mother_name')

            address = request.form.get('address')

            mobile = request.form.get('mobile')

            aadhaar = request.form.get('aadhaar')

            pan = request.form.get('pan')

            kisan_id_1 = request.form.get('kisan_id_1')

            kisan_id_2 = request.form.get('kisan_id_2')

            pm_kisan_id = request.form.get('pm_kisan_id')

            account_number = request.form.get('account_number')

            bank_name = request.form.get('bank_name')

            ifsc_code = request.form.get('ifsc_code')

            branch_name = request.form.get('branch_name')

            # ================= PHOTO UPLOAD =================

            photo = request.files.get('photo')

            photo_filename = ""

            if photo and photo.filename != "":

                filename = secure_filename(photo.filename)

                photo_path = os.path.join(
                    UPLOAD_FOLDER,
                    filename
                )

                photo.save(photo_path)

                photo_filename = filename

            # ================= SAVE FARMER =================

            farmer = Farmer(

                name=name,

                father_name=father_name,

                mother_name=mother_name,

                address=address,

                mobile=mobile,

                aadhaar=aadhaar,

                pan=pan,

                kisan_id_1=kisan_id_1,

                kisan_id_2=kisan_id_2,

                pm_kisan_id=pm_kisan_id,

                account_number=account_number,

                bank_name=bank_name,

                ifsc_code=ifsc_code,

                branch_name=branch_name,

                photo=photo_filename
            )

            db.session.add(farmer)

            db.session.commit()

            # ================= QR DATA =================

            qr_data = {

                "id": farmer.id,

                "name": farmer.name,

                "father_name": farmer.father_name,

                "mobile": farmer.mobile,

                "address": farmer.address
            }

            # ================= GENERATE QR =================

            qr = qrcode.make(json.dumps(qr_data))

            qr_filename = f"farmer_{farmer.id}.png"

            qr_path = os.path.join(
                QR_FOLDER,
                qr_filename
            )

            qr.save(qr_path)

            # ================= SAVE QR IN DATABASE =================

            farmer.qr_code = qr_filename

            db.session.commit()

            return redirect(
                url_for(
                    'success',
                    farmer_id=farmer.id
                )
            )

        except Exception as e:

            return f"ERROR: {str(e)}"

    return render_template('register.html')

# ================= SUCCESS PAGE =================

@app.route('/success/<int:farmer_id>')

def success(farmer_id):

    farmer = Farmer.query.get_or_404(farmer_id)

    return render_template(
        'success.html',
        farmer=farmer
    )

# ================= PROFILE PAGE =================

@app.route('/profile/<int:farmer_id>')

def profile(farmer_id):

    farmer = Farmer.query.get_or_404(farmer_id)

    return render_template(
        'profile.html',
        farmer=farmer
    )

# ================= RUN APP =================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )