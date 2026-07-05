# ================= BASE IMAGE =================

FROM python:3.11-slim

# ================= WORK DIRECTORY =================

WORKDIR /app

# ================= COPY FILES =================

COPY requirements.txt .

# ================= INSTALL DEPENDENCIES =================

RUN pip install --no-cache-dir -r requirements.txt

# ================= COPY PROJECT =================

COPY . .

# ================= CREATE REQUIRED FOLDERS =================

RUN mkdir -p static/uploads/farmer_photos
RUN mkdir -p static/qr_codes

# ================= EXPOSE PORT =================

EXPOSE 5000

# ================= ENV VARIABLES =================

ENV PORT=5000

# ================= START COMMAND =================

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]