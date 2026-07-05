# What changed

## Bugs fixed
- **Public PII exposure (privacy bug):** the `/profile/<id>` page is reachable by anyone who scans a QR code, but it was showing full Aadhaar, PAN, and bank account numbers. These are now masked (`•••• •••• 1234`, `•••••••34F`, `••••5678`) via `utils.py`.
- **QR codes pointed at `127.0.0.1`:** every QR baked in `http://127.0.0.1:5000/...`, so it only ever worked on the developer's own machine. Now built with `url_for(..., _external=True)`, so it uses whatever host actually serves the app.
- **Photo filename collisions:** two farmers uploading a photo with the same original filename (e.g. `IMG_0001.jpg`) would silently overwrite each other. Photos are now saved under a random unique name.
- **No server-side validation:** the form used `required` and JS formatting, but nothing stopped bad data (e.g. a 3-digit Aadhaar, invalid PAN format, missing photo) from being saved once JS was bypassed. Added real server-side validation in `utils.py` with field-specific error messages.
- **Confirm Account Number did nothing:** the "Confirm Account Number" field only changed border color; the form could still be submitted with mismatched account numbers. Submission is now blocked client-side and mismatches are shown clearly.
- **`/scan` route was missing:** `templates/qr_scan.html` existed but wasn't wired to any Flask route, so the QR scanner page was unreachable. Added `/scan`.
- **Oversized/invalid uploads crashed with a raw error:** added a 2MB upload limit with a friendly error message instead of a stack trace, plus client-side type/size checks before upload.
- **`models.py` / `utils.py` were empty placeholder files** even though the project structure implied they'd be used. Moved the `Farmer` model into `models.py` and added real helper functions to `utils.py`.
- **Confusing duplicate database files:** a stray empty `database.db` sat next to the real `instance/database.db` because of Flask-SQLAlchemy's default instance-folder behavior. The DB path is now explicit and absolute, so there's exactly one database file.
- **Debug mode hardcoded on:** `app.run(debug=True)` is now controlled by an env var (`FLASK_DEBUG`), off by default, so it isn't accidentally left on in production.
- **No secret key set:** added `SECRET_KEY` config (needed for flash messages / sessions to work at all).

## UI improvements
- Added a shared `base.html` layout with a sticky navbar (Home / Register / Scan QR / Farmers) and a consistent footer on every page — previously the footer only appeared on the registration page.
- Added flash-message banners (success/error) that show validation errors and confirmations instead of failing silently or with a Flask error page.
- Added a home page with a feature overview and live farmer count.
- Added a new **Farmers directory** page (`/farmers`) with search by name, mobile, or Kisan ID — there was previously no way to browse farmers without already having their QR code.
- Added a proper 404 page instead of Flask's default error page.
- Reworked the registration form: inline validation hints, drag-and-drop photo upload, live valid/invalid field highlighting, and a disabled submit button while saving.
- Added a privacy notice on the profile page explaining that sensitive fields are masked.
- General visual polish: button variants (primary/outline), consistent spacing, mobile nav toggle, smoother responsive breakpoints.

## Notes
- `database.db` and uploaded photos/QR codes are now git-ignored — they're generated at runtime, not project source.
- Run `pip install -r requirements.txt --break-system-packages` (or in a venv) and then `python app.py` to start the app; it will create the SQLite database and required folders automatically on first run.
