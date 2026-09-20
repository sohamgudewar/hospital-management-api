# Hospital Management System API with ML Insurance Prediction

<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.126.0-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-SQLAlchemy-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

**Hospital Management REST API with role-based JWT/OAuth2 authentication, PostgreSQL persistence, and an ML pipeline for insurance premium classification.**

</div>

---

## Overview

A modular healthcare REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**, paired with a **Streamlit** dashboard and a pre-trained **Scikit-learn** machine learning pipeline for real-time insurance premium tier classification (Low, Medium, High).

### Key Features

- **Role-Based Access Control & JWT**: Secure admin authentication using OAuth2 password flow and bcrypt password hashing.
- **Relational Persistence**: SQLAlchemy 2 models for doctors, patients, and administrative users with automated schema initialization.
- **Machine Learning Inference Pipeline**: Automated feature engineering (BMI, age grouping, lifestyle risk scoring, city tiers) and multi-class insurance premium prediction with class probabilities.
- **Interactive Streamlit UI**: Doctor/patient directory management, dashboard analytics, and insurance risk assessment forms.
- **Containerized**: Production-ready Docker configuration for straightforward deployment.

---

## Architecture

```text
Streamlit Dashboard / Frontend
          |
    (HTTP / REST)
          v
FastAPI Application (main.py)
   |-- /admin              -> JWT token generation & admin registration
   |-- /patients           -> Patient CRUD operations
   |-- /doctors            -> Doctor CRUD operations
   `-- /insurance_premium  -> Scikit-learn inference pipeline
          |
    +-----+--------------------+
    |                          |
    v                          v
PostgreSQL Database       model/model1.pkl (Random Forest Pipeline)
(Patients, Doctors, Admins)
```

---

## Tech Stack

- **Backend Framework**: FastAPI 0.126.0
- **Frontend Dashboard**: Streamlit 1.39.0
- **Database & ORM**: PostgreSQL, SQLAlchemy 2
- **Authentication**: JWT (`python-jose`), `passlib` with bcrypt
- **Machine Learning**: `scikit-learn`, `pandas`, `numpy`, `joblib`
- **ASGI Server**: Uvicorn

---

## Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Git

### 1. Clone & Set Up Virtual Environment

```bash
git clone https://github.com/sohamgudewar/hospital-management-api.git
cd hospital-management-api

python -m venv env
# Windows:
env\Scripts\activate
# Linux/macOS:
source env/bin/activate

pip install -r requirements.txt
```

### 2. Configure Database Connection

In `database.py`, update `SQLALCHEMY_DATABASE_URL` with your PostgreSQL credentials:

```python
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost:5432/hospital_management"
```

Tables are automatically created on startup via SQLAlchemy metadata.

### 3. Run FastAPI Backend

```bash
uvicorn main:app --reload
```

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 4. Run Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

Opens at `http://localhost:8501`.

---

## API Surface

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API status check |
| `GET` | `/check-connection` | Verify database connectivity |
| `POST` | `/admin/add` | Register an admin user |
| `POST` | `/admin/token` | Obtain JWT access token |
| `POST` | `/patients/patient/` | Create a patient record |
| `GET` | `/patients/patient/{id}`| Retrieve a patient record |
| `GET` | `/patients/patients_list/{limit}` | List patients with limit |
| `PUT` | `/patients/patient_id/{id}` | Update patient record |
| `DELETE`| `/patients/patient_id/{id}` | Remove patient record |
| `POST` | `/doctors/doctor/` | Create a doctor record |
| `GET` | `/doctors/doctor/{id}` | Retrieve doctor record |
| `PUT` | `/doctors/doctor_id/{id}` | Update doctor record |
| `DELETE`| `/doctors/doctor_id/{id}` | Remove doctor record |
| `GET` | `/insurance_premium/health` | Model health status and version |
| `POST` | `/insurance_premium/predict` | Predict insurance premium category |

---

## Machine Learning Pipeline

The prediction service evaluates applicant risk and assigns premium categories (`Low`, `Medium`, `High`).

### Automated Feature Engineering

- **BMI Calculation**: $\text{BMI} = \frac{\text{weight (kg)}}{(\text{height (m)})^2}$
- **Lifestyle Risk**: Evaluated dynamically based on smoking status and BMI threshold:
  - `High`: Smoker with $\text{BMI} > 30$
  - `Medium`: Smoker or $\text{BMI} > 27$
  - `Low`: Non-smoker with $\text{BMI} \le 27$
- **Age Grouping**: Categorized into `young` (<25), `adult` (25–44), `middle_aged` (45–59), and `senior` (60+)
- **City Tier**: Normalized into Tier 1, Tier 2, or Tier 3 metropolitan classifications

### Example Request

```bash
curl -X POST "http://localhost:8000/insurance_premium/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "weight": 75.5,
    "height": 1.75,
    "income_lpa": 12.5,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "Engineer"
  }'
```

### Example Response

```json
{
  "response": {
    "predicted_category": "Low",
    "confidence": 0.84,
    "class_probabilities": {
      "High": 0.0,
      "Low": 0.84,
      "Medium": 0.16
    }
  }
}
```

---

## Project Structure

```text
hospital-management-api/
|-- main.py                 # FastAPI application entry point
|-- streamlit_app.py        # Streamlit frontend application
|-- database.py             # Database engine & city classification
|-- schemas.py              # Pydantic validation & SQLAlchemy models
|-- requirements.txt        # Python dependencies
|-- Indian_Insurance_Data.csv # Training and benchmark dataset
|-- router/
|   |-- auth.py             # Admin authentication routes
|   |-- patients.py         # Patient management routes
|   |-- doctors.py          # Doctor management routes
|   `-- insurance.py        # Insurance prediction routes
`-- model/
    |-- model1.pkl          # Trained Scikit-learn pipeline
    `-- predict.py          # Preprocessing & inference logic
```

---

## Author

**Soham Gudewar**  
- GitHub: [@sohamgudewar](https://github.com/sohamgudewar)  
- LinkedIn: [soham-gudewar-9861561ab](https://www.linkedin.com/in/soham-gudewar-9861561ab)  
- Email: [sohamgudewar10@gmail.com](mailto:sohamgudewar10@gmail.com)
