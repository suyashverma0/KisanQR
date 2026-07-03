from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import qrcode

app = Flask(__name__)

# ================= CONFIG =================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
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

    kisan_id_1 = db.Column(db.String(100))
    kisan_id_2 = db.Column(db.String(100))

    pm_kisan_id = db.Column(db.String(100))

    account_number = db.Column(db.String(50))
    bank_name = db.Column(db.String(100))
    ifsc_code = db.Column(db.String(20))
    branch_name = db.Column(db.String(100))

    photo = db.Column(db.String(200))
    qr_code = db.Column(db.String(200))


# ================= HOME =================
@app.route('/')
def home():
    return render_template('index.html')


# ================= REGISTER =================
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        # ===== GET FORM DATA =====
        name = request.form['name']
        father_name = request.form['father_name']
        mother_name = request.form['mother_name']

        address = request.form['address']

        mobile = request.form['mobile']

        aadhaar = request.form['aadhaar']
        pan = request.form['pan']

        kisan_id_1 = request.form['kisan_id_1']
        kisan_id_2 = request.form['kisan_id_2']

        pm_kisan_id = request.form['pm_kisan_id']

        account_number = request.form['account_number']
        bank_name = request.form['bank_name']
        ifsc_code = request.form['ifsc_code']
        branch_name = request.form['branch_name']

        # ===== PHOTO UPLOAD =====
        photo_file = request.files['photo']

        filename = secure_filename(photo_file.filename)

        upload_path = os.path.join(
            'static/uploads/farmer_photos',
            filename
        )

        photo_file.save(upload_path)

        # ===== SAVE TO DATABASE =====
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
            photo=filename
        )

        db.session.add(farmer)
        db.session.commit()

        # ===== QR GENERATE =====
        profile_url = f"http://127.0.0.1:5000/profile/{farmer.id}"

        qr = qrcode.make(profile_url)

        qr_filename = f"farmer_{farmer.id}.png"

        qr_path = os.path.join(
            'static/qr_codes',
            qr_filename
        )

        qr.save(qr_path)

        # SAVE QR NAME
        farmer.qr_code = qr_filename

        db.session.commit()

        return redirect(url_for('success', farmer_id=farmer.id))

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


# ================= MAIN =================
if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)