// ================= PHOTO PREVIEW + VALIDATION =================

const photoInput = document.getElementById("photo");
const preview = document.getElementById("preview");
const fileNameLabel = document.getElementById("fileName");
const uploadBox = document.getElementById("uploadBox");

const MAX_PHOTO_BYTES = 2 * 1024 * 1024; // 2MB
const ALLOWED_PHOTO_TYPES = ["image/jpeg", "image/jpg", "image/png"];

function handlePhotoFile(file) {
    if (!file) return;

    if (!ALLOWED_PHOTO_TYPES.includes(file.type)) {
        alert("Please upload a JPG, JPEG, or PNG image.");
        photoInput.value = "";
        return;
    }

    if (file.size > MAX_PHOTO_BYTES) {
        alert("Photo is too large. Please choose a file under 2MB.");
        photoInput.value = "";
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        preview.src = e.target.result;
        preview.style.display = "block";
    };
    reader.readAsDataURL(file);

    if (fileNameLabel) {
        fileNameLabel.textContent = `Selected: ${file.name}`;
    }
}

if (photoInput) {
    photoInput.addEventListener("change", function () {
        handlePhotoFile(this.files[0]);
    });
}

// Drag & drop support for the upload box.
if (uploadBox && photoInput) {
    ["dragenter", "dragover"].forEach((eventName) => {
        uploadBox.addEventListener(eventName, function (e) {
            e.preventDefault();
            uploadBox.classList.add("drag-over");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        uploadBox.addEventListener(eventName, function (e) {
            e.preventDefault();
            uploadBox.classList.remove("drag-over");
        });
    });

    uploadBox.addEventListener("drop", function (e) {
        const file = e.dataTransfer.files[0];
        if (file) {
            photoInput.files = e.dataTransfer.files;
            handlePhotoFile(file);
        }
    });
}

// ================= DIGIT-ONLY FIELDS =================

function restrictToDigits(input, maxLength) {
    if (!input) return;
    input.addEventListener("input", function () {
        this.value = this.value.replace(/[^0-9]/g, "");
        if (maxLength) this.value = this.value.slice(0, maxLength);
    });
}

restrictToDigits(document.getElementById("mobile"), 10);
restrictToDigits(document.getElementById("aadhaar"), 12);

// ================= PAN / IFSC AUTO-UPPERCASE =================

["pan", "ifsc_code"].forEach((id) => {
    const el = document.getElementById(id);
    if (el) {
        el.addEventListener("input", function () {
            this.value = this.value.toUpperCase();
        });
    }
});

// ================= LIVE FIELD VALIDATION =================

const VALIDATORS = {
    mobile: (v) => /^[6-9]\d{9}$/.test(v),
    aadhaar: (v) => /^\d{12}$/.test(v),
    pan: (v) => /^[A-Z]{5}[0-9]{4}[A-Z]$/.test(v),
    ifsc_code: (v) => /^[A-Z]{4}0[A-Z0-9]{6}$/.test(v),
};

Object.keys(VALIDATORS).forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;

    el.addEventListener("blur", function () {
        if (!this.value) {
            this.classList.remove("valid", "invalid");
            return;
        }
        const isValid = VALIDATORS[id](this.value);
        this.classList.toggle("valid", isValid);
        this.classList.toggle("invalid", !isValid);
    });
});

// ================= AT LEAST ONE FARMER ID REQUIRED =================

const farmerIdInputs = ["kisan_id_1", "kisan_id_2", "pm_kisan_id"]
    .map((id) => document.getElementById(id))
    .filter(Boolean);
const farmerIdHint = document.getElementById("farmerIdHint");

function hasAnyFarmerId() {
    return farmerIdInputs.some((el) => el.value.trim() !== "");
}

function refreshFarmerIdState() {
    const filled = hasAnyFarmerId();

    farmerIdInputs.forEach((el) => {
        el.classList.remove("invalid");
    });

    if (farmerIdHint) {
        farmerIdHint.textContent = filled
            ? "Farmer ID provided ✓"
            : "At least one Farmer ID is required.";
        farmerIdHint.style.color = filled ? "var(--accent-soft)" : "var(--text-soft)";
    }

    return filled;
}

farmerIdInputs.forEach((el) => {
    el.addEventListener("input", refreshFarmerIdState);
});

// ================= ACCOUNT NUMBER MATCH =================

const accountInput = document.getElementById("account_number");
const confirmAccountInput = document.getElementById("confirm_account_number");
const accountMatchHint = document.getElementById("accountMatchHint");

function checkAccountMatch() {
    if (!accountInput || !confirmAccountInput) return true;

    if (!confirmAccountInput.value) {
        confirmAccountInput.classList.remove("valid", "invalid");
        if (accountMatchHint) accountMatchHint.textContent = "";
        return false;
    }

    const matches = accountInput.value === confirmAccountInput.value;
    confirmAccountInput.classList.toggle("valid", matches);
    confirmAccountInput.classList.toggle("invalid", !matches);

    if (accountMatchHint) {
        accountMatchHint.textContent = matches
            ? "Account numbers match ✓"
            : "Account numbers do not match";
        accountMatchHint.style.color = matches ? "var(--accent-soft)" : "var(--danger)";
    }

    return matches;
}

if (confirmAccountInput) {
    confirmAccountInput.addEventListener("keyup", checkAccountMatch);
    accountInput.addEventListener("keyup", checkAccountMatch);
}

// ================= FORM SUBMISSION =================

const form = document.getElementById("registerForm");

if (form) {
    form.addEventListener("submit", function (e) {
        if (!refreshFarmerIdState()) {
            e.preventDefault();
            if (farmerIdHint) {
                farmerIdHint.style.color = "var(--danger)";
                farmerIdHint.textContent = "Please fill in at least one Farmer ID before submitting.";
            }
            farmerIdInputs[0].focus();
            farmerIdInputs[0].scrollIntoView({ behavior: "smooth", block: "center" });
            return;
        }

        const accountsMatch = checkAccountMatch();

        if (!accountsMatch) {
            e.preventDefault();
            confirmAccountInput.focus();
            confirmAccountInput.scrollIntoView({ behavior: "smooth", block: "center" });
            return;
        }

        let firstInvalid = null;
        Object.keys(VALIDATORS).forEach((id) => {
            const el = document.getElementById(id);
            if (el && el.value && !VALIDATORS[id](el.value)) {
                el.classList.add("invalid");
                if (!firstInvalid) firstInvalid = el;
            }
        });

        if (firstInvalid) {
            e.preventDefault();
            firstInvalid.focus();
            firstInvalid.scrollIntoView({ behavior: "smooth", block: "center" });
            return;
        }

        const button = form.querySelector(".submit-btn");
        if (button) {
            button.innerHTML = "Please wait...";
            button.disabled = true;
        }
    });
}
