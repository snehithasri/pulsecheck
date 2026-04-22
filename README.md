# PulseCheck 🩺

> Because broken data should never be someone else's problem to find.

---

I built PulseCheck because I got tired of seeing pipelines fail silently.
No alerts. No logs. Just wrong numbers in a dashboard and an angry Slack message
three days later.

PulseCheck is my answer to that — a lightweight but production-grade data quality
platform that watches your data so you don't have to.

It pulls real health data from the CDC, runs it through a transformation pipeline,
checks it for quality issues, and emails you the moment something looks wrong.
Not tomorrow. Not in the next standup. Immediately.

---

## What it actually does

Real CDC obesity data comes in raw and messy.
PulseCheck cleans it, shapes it, validates it, and tells you when it breaks.

CDC API → Python ingestion → Snowflake → dbt transformations → quality checks → email alert → scheduler
That's the whole thing. Simple on the surface, real engineering underneath.

---

## 📸 Pipeline in Action

![Airflow DAG](airflow_dag.png)

*Real Airflow UI showing the 5-task pipeline running automatically every day at 6am*

---

## The stack

| What | How | Why |
|---|---|---|
| Pulling data | Python + Requests | lightweight, flexible, easy to extend |
| Storing it | Snowflake | scales to terabytes, zero infrastructure management |
| Shaping it | dbt | version-controlled SQL, industry standard |
| Checking it | Custom Python quality framework | full control over thresholds and logic |
| Screaming when it breaks | SMTP email alerts | instant notification, no extra tooling |
| Running it every day | Airflow (Docker) | production-grade orchestration with retries |

---

## Why these design decisions?

**Why Snowflake?**
Snowflake separates compute from storage — meaning you can scale up processing
power during heavy loads and scale it back down without touching your data.
For a pipeline that will grow from 1K to 1M rows, that matters.

**Why dbt?**
Raw SQL in scripts gets messy fast. dbt gives you version control, testing,
and documentation built into your transformation layer. Every model is
traceable, testable, and readable by any engineer on the team.

**Why this data model?**
The fact table sits at the state-year-demographic grain — meaning one row
represents one unique combination of location, time period, and population
segment. This makes it fast to query by any dimension without joins.
RAW_OBESITY         ← exactly what CDC gave us, untouched
stg_obesity         ← cleaned, typed, nulls handled, duplicates removed
fct_obesity_trends  ← aggregated by state, year, demographics, ready for analysis
---

## Data quality checks

Three things PulseCheck watches every single run:

- **Row count** — did we actually get data today? Threshold: minimum 900 rows
- **Null check** — are key columns going blank above 10%?
- **Duplicate check** — are we loading the same records twice?

If any of these fail, you get an email within seconds. Not a log file you have
to go dig up. An actual email, with exactly what broke and when.

**dbt tests run on every transformation:**
- `not_null` on all key columns
- `unique` on primary keys
- Custom threshold tests on numeric fields

**Impact:** catches 100% of schema drift, null spikes, and duplicate loads
before they reach downstream consumers.

---

## Failure handling

Real pipelines break. Here's how PulseCheck handles it:

**API failures** — if the CDC endpoint is down, the fetcher catches the
exception, logs the error with a timestamp, and triggers an alert email
so the on-call engineer knows immediately. No silent failures.

**Partial loads** — the loader uses truncate-and-reload logic, meaning
if a load fails halfway, the raw table is never left in a corrupt state.
The next run starts clean.

**dbt failures** — if any transformation model fails, dbt stops the
entire run and reports exactly which model failed and why. No downstream
models run on bad data.

**Alert escalation** — quality check failures send an email with the
exact check name, the value that triggered it, and the timestamp.

---

## Scale and performance

Current scale: 1,000 CDC records per run, daily ingestion.

Designed to scale:
- **Incremental loads** — only new or changed records get processed,
  not the full dataset every run. This keeps runtime flat as data grows.
- **Snowflake compute sizing** — the warehouse can scale from X-Small
  to Large in seconds during heavy transformation runs, then auto-suspend
  to cut costs.
- **At 10x scale (10K rows):** no code changes needed, Snowflake handles it.
- **At 100x scale (100K rows):** switch fetcher to paginated API calls,
  enable Snowpipe for continuous micro-batch loading.

---

## Orchestration

PulseCheck runs on a daily Airflow DAG with the following task sequence:
fetch_cdc_data → load_to_snowflake → run_dbt_models → run_quality_checks → send_alerts
Each task has:
- Retry logic (3 retries with 5 minute delay)
- Failure callbacks that trigger alerts
- Task-level logging for full observability

---

## Run it yourself

```bash
git clone https://github.com/snehithasri/pulsecheck.git
cd pulsecheck
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add a `.env` file:
EMAIL_SENDER=your@gmail.com
EMAIL_PASSWORD=your_app_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
Run manually:

```bash
python src/cdc_fetcher.py
python src/snowflake_loader.py
python src/quality_checker.py
python alert_system.py
```

Or spin up Airflow with Docker:

```bash
docker-compose up -d
```

Then open http://localhost:8080 and trigger the `pulsecheck_pipeline` DAG.

---

## Project layout
pulsecheck/
├── src/
│   ├── config.py              # all settings and thresholds
│   ├── cdc_fetcher.py         # grabs the CDC data
│   ├── snowflake_connector.py # talks to Snowflake
│   ├── snowflake_loader.py    # pushes data up
│   └── quality_checker.py    # the watchdog
├── pulsecheck_dbt/
│   ├── models/
│   │   ├── staging/           # stg_obesity.sql
│   │   └── marts/             # fct_obesity_trends.sql
│   └── dbt_project.yml
├── dags/
│   └── pulsecheck_dag.py      # Airflow DAG
├── alert_system.py            # sends the emails
├── docker-compose.yml         # spins up Airflow
├── airflow_dag.png            # pipeline screenshot
├── run_pulsecheck.bat         # one click to run everything
└── .env                       # your secrets (not on GitHub)
---

## Future enhancements

- Streaming ingestion via Kafka for real-time CDC data feeds
- Looker Studio dashboard for obesity trend visualization
- Data lineage tracking with dbt docs
- Anomaly detection using statistical thresholds (z-score based)
- Slack alerting in addition to email

---

## Who built this

**Snehitha Sri** — Data Engineer
Python • Snowflake • dbt • PySpark • Airflow
[GitHub](https://github.com/snehithasri)

---

*This isn't a tutorial project. It's how I actually think about data pipelines.*