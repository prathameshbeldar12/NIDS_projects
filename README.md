# NIDS_projects
CYBERSECURITY

# 🚨 Network Intrusion Detection System (NIDS)

A Cybersecurity-focused **AI-powered Network Intrusion Detection System** built using **Django, Machine Learning, and Real-time Alerting**.

This system detects malicious network activity, classifies attacks, and sends real-time alerts via email with severity and confidence scoring.

---

## 🔥 Project Overview

The Network Intrusion Detection System (NIDS) monitors incoming network traffic data, analyzes it using a trained Machine Learning model, and detects potential cyber attacks such as:

* DoS (Denial of Service)
* Probe Attacks
* R2L (Remote to Local)
* U2R (User to Root)
* Normal Traffic Classification

Detected attacks are logged into a secure dashboard and trigger automated email alerts to administrators.

---

## 🛠 Tech Stack

**Backend:**

* Python
* Django
* Django ORM
* Gunicorn

**Machine Learning:**

* Scikit-learn
* Pandas
* NumPy

**Database:**

* SQLite (Development)
* PostgreSQL (Production Ready)

**Deployment:**

* GitHub
* Render
* Whitenoise

**Security Features:**

* OTP-based Password Reset
* Email Attack Alerts
* Role-based Authentication
* Secure Session Handling

---

## 🚀 Features

✅ AI-based attack detection
✅ Real-time attack logging
✅ Email alert system for detected attacks
✅ Confidence score for each prediction
✅ Severity classification (Low / Medium / High / Critical)
✅ Admin dashboard with analytics
✅ CSV file upload for traffic analysis
✅ Secure authentication system
✅ Production-ready deployment setup

---

## 📊 System Architecture

User → Upload Network Data (CSV)
↓
ML Model Prediction
↓
Attack Classification
↓
Database Storage
↓
Dashboard Display + Email Alert

---

## 📂 Project Structure

```
nids_project/
│
├── nids_dashboard/
│   ├── models.py
│   ├── views.py
│   ├── alerts.py
│   ├── templates/
│
├── static/
├── manage.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/nids-project.git
cd nids-project
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Apply Migrations

```bash
python manage.py migrate
```

### 5️⃣ Run Server

```bash
python manage.py runserver
```

Visit:

```
http://127.0.0.1:8000/
```

---

## 📧 Email Alert System

When an attack is detected:

* Attack Type
* Severity Level
* Confidence Score
* Detection Timestamp

Are automatically emailed to the registered user.

---

## 🌐 Deployment

This project is deployment-ready on:

* Render (Recommended)
* Railway
* PythonAnywhere

Includes:

* Gunicorn configuration
* PostgreSQL support
* Environment variable setup
* Production security settings

---

## 📈 Future Enhancements

* Real-time packet sniffing integration
* Deep Learning model (LSTM / CNN)
* SIEM integration
* Docker containerization
* API version for mobile app
* Role-based SOC Analyst panel

---

## 🎯 Career Objective

This project demonstrates:

* Cybersecurity knowledge
* Intrusion Detection concepts
* Machine Learning implementation
* Django backend development
* Secure system design
* Production deployment skills

---

## 👨‍💻 Author

**Prathamesh Beldar**
Cybersecurity Enthusiast | SOC Analyst Aspirant

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub and connect with me for collaboration!
