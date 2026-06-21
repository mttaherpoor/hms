# 🏥 HMS — Hospital Management System

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?logo=django)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)
![Nginx](https://img.shields.io/badge/Nginx-Reverse_Proxy-brightgreen?logo=nginx)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A full-featured **Hospital Management System** built with **Django**, containerized with **Docker**, and designed for scalable production deployment behind **Nginx**.

---

## ✨ Features

| Area | Details |
|------|---------|
| 👨‍⚕️ Staff | Doctor & Patient management |
| 📅 Scheduling | Appointment booking system |
| 💳 Payments | Stripe / PayPal integration |
| 📧 Notifications | Email alerts & templates |
| 📊 Dashboards | Separate views for doctors & patients |
| 🔐 Auth | Custom authentication system |
| 📄 Records | Medical records & lab tests |
| 🧾 Billing | Full billing system |
| 🐳 DevOps | Dockerized deployment + CI/CD |

---

## 🏗️ Project Architecture

```
backend/
├── accounts/     # Custom user model & authentication
├── doctor/       # Doctor dashboard & business logic
├── patient/      # Patient dashboard & business logic
├── base/         # Core shared services & utilities
└── config/       # Django settings, ASGI & WSGI config
```

---

## 🐳 Quick Start with Docker

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hms.git
cd hms
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
SECRET_KEY=your_secret_key
DEBUG=True
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
```

### 3. Build and run

```bash
docker-compose up --build
```

The app will be available at `http://localhost`.

---

## 🛠️ Local Development (Without Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🌐 Production — Nginx Setup

Nginx is configured as a **reverse proxy** in front of Gunicorn:

- Routes HTTP traffic to the Django/Gunicorn application
- Serves static and media files directly for performance
- Easily extendable with SSL (Let's Encrypt / Certbot)

---

## ⚙️ CI/CD — GitHub Actions

The pipeline at `.github/workflows/ci.yml` runs automatically on every push:

- ✅ Unit & integration tests
- ✅ Lint checks (flake8 / ruff)
- ✅ Docker image build validation

---

## 📁 UI Templates

Pre-built templates included out of the box:

- Authentication pages (login, register, password reset)
- Doctor dashboard
- Patient dashboard
- Email notification templates
- Static landing pages

---

## 📌 Technical Notes

- Uses a **custom user model** (`accounts.CustomUser`) — set up before first migration
- Modular app structure makes it easy to extend or extract into microservices
- Designed with scalability in mind; ready for a microservice transition

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 👤 Author

Built with ❤️ by **Mohamad Taher Taherpoor**
