# ⚙️ Backend

Backend implementation of the **Cloud Policy Cost and Security Simulator**, a Digital Twin platform designed to simulate cloud infrastructure, governance, FinOps, and cybersecurity workflows in a safe educational environment.

---

## 🚀 Overview

The backend is built using **Flask** and serves as the core engine of the simulator. It manages cloud resources, user authentication, organizations, telemetry generation, AI-assisted threat detection, governance validation, reporting, and PostgreSQL database operations.

---

# ✨ Core Features

- 🔐 Authentication & Authorization
- 🏢 Organization & Tenant Management
- 🖥️ Virtual Machine Simulation
- 🗄️ Database Simulation
- 📊 Synthetic Telemetry Generation
- 🤖 AI-Assisted Threat Detection
- 🛡️ Governance Policy Validation
- 📈 Resource Monitoring
- 💰 Cost Management
- 📄 Report Generation
- 🌐 RESTful API
- 🗃️ PostgreSQL Integration

---

# 📁 Directory Structure

```text
backend/
│
├── app/
│   ├── ai_models/
│   ├── data_sources/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
├── data/
├── migrations/
├── scripts/
│
├── requirements.txt
├── run.py
└── wsgi.py
```

---

# 🛠️ Technology Stack

| Category | Technology |
|-----------|------------|
| Backend Framework | Flask |
| Language | Python |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| API | REST |
| AI | Machine Learning Models |

---

# ▶️ Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Backend

```bash
python run.py
```

---

# 📌 Current Development Status

| Module | Status |
|---------|:------:|
| Authentication | ✅ |
| Organization Manager | ✅ |
| Data Generator | ✅ |
| Resource Simulator | ✅ |
| Resource Viewer | ✅ |
| Threat Detector | ✅ |
| Policy Engine | 🚧 |
| Cost Forecaster | 🚧 |
| Report Generator | 🚧 |
| Remediation Agent | 🚧 |
| Audit Trail | 🚧 |
| User Settings | 🚧 |

---

# 🎯 Project Goal

The objective of this backend is to provide a reusable cloud simulation environment that enables students, researchers, and beginner cloud professionals to safely explore cloud governance, infrastructure monitoring, FinOps, and cybersecurity concepts without relying on production cloud platforms.

---

# 📄 License

This project is licensed under the **MIT License**.
