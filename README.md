# PulseCheck 🩺
### Automated Data Quality Observability Platform for CDC Health Data

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Snowflake](https://img.shields.io/badge/Snowflake-Cloud%20DB-lightblue)
![dbt](https://img.shields.io/badge/dbt-Transformations-orange)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 🔍 What is PulseCheck?

PulseCheck is a production-grade data quality monitoring platform that ingests real CDC (Centers for Disease Control) health data, transforms it through a multi-layer pipeline, validates quality automatically, and fires email alerts the moment something fails. Built to simulate the kind of observability tooling used at companies like Netflix, Airbnb, and CVS Health.

---

## 🏗️ Architecture
CDC API (Real Government Data)
↓
Python Ingestion Layer (cdc_fetcher.py)
↓
Snowflake Cloud Database (RAW_DATA schema)
↓
dbt Transformations (staging → facts)
↓
Quality Checks (quality_checker.py)
↓
Email Alert System (alert_system.py)
↓
Automated Daily Runs (Windows Task Scheduler)
---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Ingestion | Python, Requests |
| Storage | Snowflake |
| Transformation | dbt |
| Quality Checks | Custom Python framework |
| Alerting | Python SMTP / Gmail |
| Orchestration | Windows Task Scheduler |
| Version Control | Git / GitHub |

---

## 📊 Data Quality Checks

PulseCheck automatically validates:
- ✅ **Row count** — ensures expected volume of records
- ✅ **Null check** — flags columns exceeding 10% null threshold
- ✅ **Duplicate check** — detects and reports duplicate records

When any check fails, an email alert fires automatically with the check that failed, the exact value that triggered it, and the timestamp of the failure.

---

## 🗄️ dbt Transformation Layers
RAW_OBESITY (raw CDC data)
↓
stg_obesity (cleaned + typed)
↓
fct_obesity_trends (aggregated by state, year, demographics)
---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/snehithasri/pulsecheck.git

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your credentials to .env
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_app_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password

# 5. Run the pipeline
python src/cdc_fetcher.py
python src/snowflake_loader.py
python src/quality_checker.py
python alert_system.py
```

---

## 📁 Project Structure
pulsecheck/
├── src/
│   ├── config.py              # settings + thresholds
│   ├── cdc_fetcher.py         # fetches CDC data
│   ├── snowflake_connector.py # Snowflake connection
│   ├── snowflake_loader.py    # loads data to Snowflake
│   └── quality_checker.py    # quality validation
├── pulsecheck_dbt/
│   ├── models/
│   │   ├── staging/           # stg_obesity.sql
│   │   └── marts/             # fct_obesity_trends.sql
│   └── dbt_project.yml
├── alert_system.py            # email alert system
├── run_pulsecheck.bat         # automation script
├── .env                       # credentials (not in GitHub)
└── README.md
---

## 👩‍💻 Author

**Snehitha Sri**  
Data Engineer | Python • Snowflake • dbt • PySpark • Airflow  
[GitHub](https://github.com/snehithasri)

---

*Built as part of a portfolio to demonstrate production-grade data engineering skills.*