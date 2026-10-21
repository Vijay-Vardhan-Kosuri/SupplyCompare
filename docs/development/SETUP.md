# SupplyCompare — Local Development & Deployment Guide

## 1. Prerequisites

Ensure your development workstation has:
* **Python**: 3.10+ (Tested on Python 3.11 and 3.14)
* **Node.js**: v18+ (Tested on Node v20 and v24)
* **MySQL**: 8.0+ (Running on port 3306)
* **Git**: 2.30+
* **Docker & Docker Compose** (Optional, for containerized execution)

---

## 2. Local Bare-Metal Setup

### Step 1: Clone & Configure Environment
```bash
git clone https://github.com/organization/SupplyCompare.git
cd SupplyCompare

# Copy environment template
cp .env.example .env
```
Ensure your `.env` contains your MySQL credentials:
```env
DB_ENGINE=mysql
DB_NAME=supplycompare_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Step 2: Initialize MySQL Database
```sql
CREATE DATABASE IF NOT EXISTS supplycompare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Step 3: Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed realistic small retail store catalog & quotes
python scripts/seed_data.py
```

### Step 4: Run Backend Server
```bash
python manage.py runserver 0.0.0.0:8000
```
Backend API will be active at `http://localhost:8000/api/v1/health/`.

### Step 5: Frontend Setup
In a new terminal:
```bash
cd SupplyCompare/frontend
npm install
npm run dev
```
Frontend UI will be active at `http://localhost:5173`.

---

## 3. Demo Credentials

| Role | Email | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Retailer** | `retailer@supplycompare.local` | `Retailer@123` | Store procurement, comparison, POs, inventory |
| **Supplier** | `supplier@supplycompare.local` | `Supplier@123` | Fulfillment portal, quotation pricing |
| **Admin** | `admin@supplycompare.local` | `Admin@123` | User governance, platform audits |

---

## 4. Running Automated Tests

Run the full automated test suite (Auth, Comparison Engine, Purchasing, Inventory):
```bash
cd backend
python manage.py test tests
```

---

## 5. Docker Compose Deployment

To boot the entire full-stack system in isolated containers:
```bash
docker-compose up --build -d
```
* React Frontend: `http://localhost:5173`
* Django REST API: `http://localhost:8000`
* MySQL 8.0 Database: `localhost:3307`
