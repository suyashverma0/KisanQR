import os

from flask import Flask, flash, redirect, render_template, request, url_for
from werkzeug.exceptions import RequestEntityTooLarge

from models import Farmer, db
from utils import (
    allowed_file,
    generate_qr,
    mask_aadhaar,
    mask_account_number,
    mask_pan,
    save_photo,
    validate_farmer_form,
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "farmer_photos")
QR_FOLDER = os.path.join(BASE_DIR, "static", "qr_codes")

app = Flask(__name__)

# ================= CONFIG =================
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2 MB upload limit
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["QR_FOLDER"] = QR_FOLDER

db.init_app(app)

# Make sure the folders we save into always exist.
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)


# ================= ERROR HANDLERS =================
@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(_error):
    flash("Photo is too large. Please upload an image under 2MB.", "error")
    return redirect(url_for("register"))


@app.errorhandler(404)
def handle_not_found(_error):
    return render_template("404.html"), 404


# ================= HOME =================
@app.route("/")
def home():
    farmer_count = Farmer.query.count()
    return render_template("index.html", farmer_count=farmer_count)


# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        errors = validate_farmer_form(request.form)

        photo_file = request.files.get("photo")
        if not photo_file or photo_file.filename == "":
            errors.append("Farmer photo is required.")
        elif not allowed_file(photo_file.filename):
            errors.append("Photo must be a JPG, JPEG, or PNG file.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("register.html", form_data=request.form)

        # ===== PHOTO UPLOAD =====
        photo_filename = save_photo(photo_file, app.config["UPLOAD_FOLDER"])

        # ===== SAVE TO DATABASE =====
        farmer = Farmer(
            name=request.form["name"].strip(),
            father_name=request.form["father_name"].strip(),
            mother_name=request.form["mother_name"].strip(),
            address=request.form["address"].strip(),
            mobile=request.form["mobile"].strip(),
            aadhaar=request.form["aadhaar"].strip(),
            pan=request.form["pan"].strip().upper(),
            kisan_id_1=request.form.get("kisan_id_1", "").strip(),
            kisan_id_2=request.form.get("kisan_id_2", "").strip(),
            pm_kisan_id=request.form.get("pm_kisan_id", "").strip(),
            account_number=request.form["account_number"].strip(),
            bank_name=request.form["bank_name"].strip(),
            ifsc_code=request.form["ifsc_code"].strip().upper(),
            branch_name=request.form["branch_name"].strip(),
            photo=photo_filename,
        )

        db.session.add(farmer)
        db.session.commit()

        # ===== QR GENERATE =====
        profile_url = url_for("profile", farmer_id=farmer.id, _external=True)
        farmer.qr_code = generate_qr(profile_url, app.config["QR_FOLDER"], farmer.id)
        db.session.commit()

        flash(f"{farmer.name} was registered successfully!", "success")
        return redirect(url_for("success", farmer_id=farmer.id))

    return render_template("register.html", form_data={})


# ================= SUCCESS PAGE =================
@app.route("/success/<int:farmer_id>")
def success(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    return render_template("success.html", farmer=farmer)


# ================= PROFILE PAGE =================
@app.route("/profile/<int:farmer_id>")
def profile(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    return render_template(
        "profile.html",
        farmer=farmer,
        masked_aadhaar=mask_aadhaar(farmer.aadhaar),
        masked_pan=mask_pan(farmer.pan),
        masked_account=mask_account_number(farmer.account_number),
    )


# ================= QR SCANNER =================
@app.route("/scan")
def scan():
    return render_template("qr_scan.html")


# ================= FARMERS DIRECTORY =================
@app.route("/farmers")
def farmers():
    query = request.args.get("q", "").strip()
    farmers_query = Farmer.query

    if query:
        farmers_query = farmers_query.filter(
            db.or_(
                Farmer.name.ilike(f"%{query}%"),
                Farmer.mobile.ilike(f"%{query}%"),
                Farmer.kisan_id_1.ilike(f"%{query}%"),
            )
        )

    all_farmers = farmers_query.order_by(Farmer.id.desc()).all()
    return render_template("farmers.html", farmers=all_farmers, query=query)


# ================= MAIN =================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(debug=debug_mode)
