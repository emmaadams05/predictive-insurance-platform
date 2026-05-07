# Predictive-Insurange-Platform

This is an end-to-end insurance risk assessment workflow application for my _CSE4701: Principles of Database Systems_ class. It combines machine learning, a Flask web application, and an Azure SQL database to generate insurance business recommendations based on health-risk data.

---

# Project Structure

```text
predictive-insurange-platform/
│
├── app/
│   ├── app.py
│   └── templates/
│       ├── index.html
│       └── result.html
│
├── database/
│   └── schema.sql
│
├── health_data/
├── models/
├── output/
│
├── src/
│   ├── data_loader.py
│   ├── decision_tree_model.py
│   ├── kmeans_model.py
│   ├── run_models.py
│   └── retrain_models.py
│
├── requirements.txt
└── README.md
```

---

# Setup

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Create the Azure SQL database

Create an Azure SQL database with:

```text
Database Name:
insurance-risk-db

Server Name:
insurance-risk-db-final-server
```

Run:

```text
database/schema.sql
```

using Azure Query Editor or Azure Data Studio.

---

## 3. Configure the database connection

### Mac/Linux

```bash
export DATABASE_URL="mssql+pyodbc://USERNAME:PASSWORD@insurance-risk-db-final-server.database.windows.net:1433/insurance-risk-db?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
```

### Windows PowerShell

```powershell
$env:DATABASE_URL="mssql+pyodbc://USERNAME:PASSWORD@insurance-risk-db-final-server.database.windows.net:1433/insurance-risk-db?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
```

Replace:

- `USERNAME`
- `PASSWORD`

with your Azure SQL credentials.

---

## 4. Run the machine learning pipeline

```bash
python src/run_models.py
```

This generates:

- trained model files
- business recommendation output data

---

## 5. Run the Flask application

```bash
python app/app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# Application Workflow

```text
Customer submits quote request
→ application generates ML-based recommendation
→ recommendation is stored in Azure SQL
→ recommendation displayed to user
```

---

# Retraining Models

To retrain the models:

```bash
python src/retrain_models.py
```
