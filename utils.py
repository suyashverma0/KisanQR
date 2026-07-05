import os
import re
import uuid

import qrcode
from werkzeug.utils import secure_filename

ALLOWED_PHOTO_EXTENSIONS = {"jpg", "jpeg", "png"}

AADHAAR_PATTERN = re.compile(r"^\d{12}$")
PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")
MOBILE_PATTERN = re.compile(r"^[6-9]\d{9}$")
IFSC_PATTERN = re.compile(r"^[A-Z]{4}0[A-Z0-9]{6}$")


def allowed_file(filename):
    """Check the uploaded file has an allowed image extension."""
    if not filename or "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in ALLOWED_PHOTO_EXTENSIONS


def save_photo(photo_file, upload_folder):
    """
    Save an uploaded photo with a unique, collision-free filename.
    Returns the saved filename (not the full path).
    """
    os.makedirs(upload_folder, exist_ok=True)

    original_name = secure_filename(photo_file.filename)
    ext = original_name.rsplit(".", 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"

    photo_file.save(os.path.join(upload_folder, unique_name))
    return unique_name


def generate_qr(data, qr_folder, farmer_id):
    """Generate a QR code image for the given data and return its filename."""
    os.makedirs(qr_folder, exist_ok=True)

    qr_filename = f"farmer_{farmer_id}.png"
    qr_path = os.path.join(qr_folder, qr_filename)

    img = qrcode.make(data)
    img.save(qr_path)

    return qr_filename


def mask_middle(value, keep_start=0, keep_end=4, mask_char="•"):
    """Mask the middle of a sensitive string, keeping a few edge characters visible."""
    if not value:
        return ""

    value = str(value)
    length = len(value)

    if length <= keep_start + keep_end:
        return mask_char * length

    start = value[:keep_start]
    end = value[-keep_end:] if keep_end else ""
    middle = mask_char * (length - keep_start - keep_end)

    return f"{start}{middle}{end}"


def mask_aadhaar(value):
    """Show only the last 4 digits of an Aadhaar number, e.g. •••• •••• 1234."""
    masked = mask_middle(value, keep_start=0, keep_end=4)
    # group into 4s for readability where possible
    if len(masked) == 12:
        return f"{masked[0:4]} {masked[4:8]} {masked[8:12]}"
    return masked


def mask_account_number(value):
    """Show only the last 4 digits of a bank account number."""
    return mask_middle(value, keep_start=0, keep_end=4)


def mask_pan(value):
    """Show only the last 3 characters of a PAN number."""
    return mask_middle(value, keep_start=0, keep_end=3)


def validate_farmer_form(form):
    """
    Validate submitted registration form data.
    Returns a list of human-readable error messages (empty list = valid).
    """
    errors = []

    required_fields = {
        "name": "Full Name",
        "father_name": "Father Name",
        "mother_name": "Mother Name",
        "address": "Address",
        "mobile": "Mobile Number",
        "aadhaar": "Aadhaar Number",
        "pan": "PAN Number",
        "account_number": "Account Number",
        "bank_name": "Bank Name",
        "ifsc_code": "IFSC Code",
        "branch_name": "Branch Name",
    }

    for field, label in required_fields.items():
        if not form.get(field, "").strip():
            errors.append(f"{label} is required.")

    mobile = form.get("mobile", "").strip()
    if mobile and not MOBILE_PATTERN.match(mobile):
        errors.append("Mobile number must be a valid 10-digit Indian mobile number.")

    aadhaar = form.get("aadhaar", "").strip()
    if aadhaar and not AADHAAR_PATTERN.match(aadhaar):
        errors.append("Aadhaar number must be exactly 12 digits.")

    pan = form.get("pan", "").strip().upper()
    if pan and not PAN_PATTERN.match(pan):
        errors.append("PAN number must be in the format ABCDE1234F.")

    ifsc = form.get("ifsc_code", "").strip().upper()
    if ifsc and not IFSC_PATTERN.match(ifsc):
        errors.append("IFSC code must be in the format SBIN0004587.")

    # At least one farmer ID (Kisan ID 1 / Kisan ID 2 / PM Kisan ID) must be provided.
    kisan_id_1 = form.get("kisan_id_1", "").strip()
    kisan_id_2 = form.get("kisan_id_2", "").strip()
    pm_kisan_id = form.get("pm_kisan_id", "").strip()

    if not (kisan_id_1 or kisan_id_2 or pm_kisan_id):
        errors.append(
            "Please provide at least one Farmer ID (Kisan ID 1, Kisan ID 2, or PM Kisan ID)."
        )

    return errors
