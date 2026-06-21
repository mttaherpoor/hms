# 🏥 HMS - Hospital Management System

A full-featured **Hospital Management System (HMS)** built with modern backend architecture using **Django**, containerized with **Docker**, and designed for scalable deployment using **Nginx**.

---

## 🚀 Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-brightgreen?logo=nginx)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📦 Features

- 👨‍⚕️ Doctor & Patient Management
- 📅 Appointment Booking System
- 💳 Payment Integration (Stripe / PayPal)
- 📧 Email Notifications
- 📊 Dashboard for Doctors & Patients
- 🔐 Custom Authentication System
- 📄 Medical Records & Lab Tests
- 🧾 Billing System
- 🐳 Dockerized Deployment
- ⚡ CI/CD via GitHub Actions

---

## 🏗️ Project Architecture


backend/
│── accounts/ # Custom user & authentication
│── doctor/ # Doctor dashboard & logic
│── patient/ # Patient dashboard & logic
│── base/ # Core shared services
│── config/ # Django settings & ASGI/WSGI


---

## 🐳 Run with Docker

### 1. Clone repository
```bash
git clone https://github.com/your-username/hms.git
cd hms
2. Create environment file
cp .env.example .env
3. Run containers
docker-compose up --build
⚙️ Environment Variables

Create .env file:

SECRET_KEY=your_secret
DEBUG=True
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
🌐 Nginx Setup (Production)
Acts as reverse proxy
Handles static/media files
Routes traffic to Django via Gunicorn
🧪 CI/CD

This project uses GitHub Actions for:

Running tests
Lint checks
Docker build validation

Workflow located at:

.github/workflows/ci.yml
📁 Templates

Includes prebuilt UI templates:

Authentication pages
Doctor dashboard
Patient dashboard
Email templates
Static landing pages
🧑‍💻 Development Setup (Without Docker)
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
📌 Notes
Uses custom user model (accounts.CustomUser)
Modular app structure
Designed for scalability and microservice transition
📄 License

This project is licensed under the MIT License.

⭐ Author

Built with ❤️ by Mohamad Taher Taherpoor


---

If you want, I can next upgrade this into:

- 🔥 :contentReference[oaicite:0]{index=0}
- 🚀 :contentReference[oaicite:1]{index=1}
- 🧪 :contentReference[oaicite:2]{index=2}
- 🌍 :contentReference[oaicite:3]{index=3}

Just tell me.
