from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Farmer(db.Model):
    """Stores a farmer's registration details."""

    id = db.Column(db.Integer, primary_key=True)

    # ---- Personal details ----
    name = db.Column(db.String(100), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)

    # ---- Identity documents ----
    aadhaar = db.Column(db.String(20), nullable=False)
    pan = db.Column(db.String(20), nullable=False)

    # ---- Farmer IDs ----
    kisan_id_1 = db.Column(db.String(100))
    kisan_id_2 = db.Column(db.String(100))
    pm_kisan_id = db.Column(db.String(100))

    # ---- Bank details ----
    account_number = db.Column(db.String(50), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    ifsc_code = db.Column(db.String(20), nullable=False)
    branch_name = db.Column(db.String(100), nullable=False)

    # ---- Media ----
    photo = db.Column(db.String(200))
    qr_code = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<Farmer {self.id} {self.name}>"
