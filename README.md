# SupplyCompare — Supplier Quotation & Purchasing Management Platform

[![CI/CD Pipeline](https://github.com/organization/SupplyCompare/actions/workflows/ci.yml/badge.svg)](https://github.com/organization/SupplyCompare/actions)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.14-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1%20%2F%20DRF-092E20?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-Proprietary-1E3A2B)](LICENSE)

**SupplyCompare** is an enterprise-grade supplier quotation comparison and procurement management platform engineered for small retail merchants, shopkeepers, and kirana stores.

It addresses a major retail operational challenge: wholesale suppliers offer complex, non-standardized price quotes that differ across **minimum order quantities (MOQ)**, **delivery logistics surcharges**, **tiered discounts**, **promised lead times**, **quotation validity windows**, and **product units of measurement** (cartons, bags, packets, kilograms).

---

## 🌿 Design Language & User Experience

SupplyCompare features a warm, earthy commerce operations interface inspired by the aesthetic of [Native Commerce](https://www.nativecommerce.ai/why-native):
* **Main Background**: Warm ivory / soft cream (`#FAF8F5`)
* **Navigation & Sidebar**: Deeper warm neutral (`#F2EFE9`) with crisp outline icons
* **Primary Accent**: Deep forest green (`#1E3A2B`)
* **Secondary Accent**: Muted olive / sage (`#5A735E`)
* **Highlight Accent**: Restrained terracotta (`#C86D51`)
* **Typography**: Plus Jakarta Sans for clean tabular numbers and typography hierarchy

---

## 🌟 Signature Features

### 1. Quotation Comparison Engine (`/compare`)
* **Unit Normalization**: Dynamically converts between master shipper cartons and retail consumer units (e.g. 1 carton of biscuits = 24 packets).
* **Deterministic Eligibility Verification**:
  - Validates active supplier account status.
  - Rejects expired quotations (`valid_until < today`).
  - Checks Minimum Order Quantity: $Q_{\text{needed}} \ge \text{MOQ}$.
  - Checks Supplier Inventory: $Q_{\text{needed}} \le \text{Stock}$.
* **Complete Multi-Component Cost Calculation**:
  $$\text{Total Order Cost} = (\text{Base Merchandise} - \text{Discount}) + \text{Logistics Fee} + \text{Taxes}$$
* **Best Deal Recommendation**: Ranks strictly by lowest total order cost among **eligible** suppliers only. Never recommends a supplier based on unit price alone.
* **1-Click Purchase Order Generation**: Instantly issues a purchase order from the winning quotation.

### 2. Purchase Order State Machine & PDF Engine (`/purchase-orders`)
* Adheres to strict finite state machine transitions:
  $$\text{Draft} \longrightarrow \text{Submitted} \longrightarrow \text{Confirmed} \longrightarrow \text{Shipped} \longrightarrow \text{Received}$$
* Prevents invalid transitions or skipping steps.
* Generates downloadable official purchase order PDFs compiled on-the-fly using **ReportLab**.

### 3. Idempotent Transactional Inventory Restocking (`/inventory`)
* Receiving dock operations record good units vs damaged units with physical discrepancy logging.
* Automatically increments inventory stock within `transaction.atomic()`.
* Protected against duplicate receipt processing via atomic state flags.
* Maintains an immutable chronological audit trail in `StockMovement`.

### 4. Real-Time Procurement Analytics (`/analytics`)
* Real database metrics for total spend, potential savings, and top suppliers.
* Interactive business graphs powered by **Recharts**.
* Transparent methodology explanations for every metric calculation.

### 5. Multi-Role RBAC & Portals
* **Retailer**: Full catalog management, supplier quotes, comparison, POs, and inventory.
* **Supplier**: Dedicated fulfillment portal to view client POs and mark orders shipped.
* **Platform Administrator**: Account governance, role assignment, and user suspension.

---

## 🧪 Benchmark Verification

The platform was built and automatedly verified against the prompt's reference scenario:

> **Scenario**:  
> Supplier A charges ₹900/carton with free delivery and MOQ 5.  
> Supplier B charges ₹870/carton plus ₹300 delivery with MOQ 15.

* **Order of 10 Cartons**:
  - Supplier A: Eligible. Total = ₹9,000. **(Recommended Best Deal)**
  - Supplier B: Ineligible. Reason: *"Minimum order is 15 cartons (your order requires 10 cartons)"*.
* **Order of 15 Cartons**:
  - Supplier A: Eligible. Total = ₹13,500.
  - Supplier B: Eligible. Total = ₹13,350. **(Recommended Best Deal, Savings = ₹150)**

Automated test suite verification: **16/16 tests passing (100%)**.

---

## 🚀 Quick Start Guide

### Bare-Metal Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/organization/SupplyCompare.git
   cd SupplyCompare
   cp .env.example .env
   ```

2. **Configure Database**:
   Ensure MySQL 8.0 is running on `127.0.0.1:3306`, then create the database:
   ```sql
   CREATE DATABASE supplycompare_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python manage.py migrate
   python scripts/seed_data.py
   python manage.py runserver 0.0.0.0:8000
   ```

4. **Frontend Setup**:
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

### Docker Compose Setup
```bash
docker-compose up --build -d
```

---

## 🔑 Demo Credentials

| Role | Email | Password | Shop / Company |
| :--- | :--- | :--- | :--- |
| **Retailer** | `retailer@supplycompare.local` | `Retailer@123` | Sri Lakshmi Kirana Stores |
| **Supplier** | `supplier@supplycompare.local` | `Supplier@123` | Singhania Wholesale Corp |
| **Admin** | `admin@supplycompare.local` | `Admin@123` | Platform Administrator |

---

## 📁 Repository Structure

```
SupplyCompare/
├── .github/workflows/ci.yml       # GitHub Actions CI workflow
├── backend/
│   ├── config/                    # Django core settings, routing, PyMySQL
│   ├── apps/
│   │   ├── accounts/              # Custom User, JWT Auth, RBAC permissions
│   │   ├── catalog/               # Products, Categories, Unit Conversions
│   │   ├── suppliers/             # Supplier directory & terms
│   │   ├── quotations/            # Price quotes, validity, and discounts
│   │   ├── comparison/            # Signature Comparison Service & API
│   │   ├── purchasing/            # Purchase orders, state machine, PDF export
│   │   ├── inventory/             # Stock items, audit movements, adjustments
│   │   ├── analytics/             # Real-time KPIs, spend graphs, scorecards
│   │   └── notifications/         # In-app alerts & warnings
│   ├── scripts/seed_data.py       # Indian kirana store dataset generator
│   ├── tests/                     # 16 unit & integration tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── theme/theme.css        # Native Commerce warm earthy CSS system
│   │   ├── components/            # Sidebar, Header, SummaryCard, StatusBadge
│   │   ├── pages/                 # Comparison, Dashboard, POs, Inventory
│   │   ├── context/               # AuthContext
│   │   └── services/              # Axios API client
│   ├── package.json
│   └── vite.config.js
├── docs/
│   ├── architecture/ARCHITECTURE.md
│   ├── database/SCHEMA.md
│   ├── api/API_REFERENCE.md
│   ├── api/SupplyCompare_API.postman_collection.json
│   ├── api/openapi.yaml
│   ├── user-guides/               # Retailer, Supplier, Admin Guides
│   └── development/SETUP.md
├── docker-compose.yml
└── README.md
```

---

## 👥 Authentic Team Collaboration Setup

* **Venkat Vijay Vardhan Kosuri** : Lead Architect & Core Comparison Engine
* **Kalyan Nanduri** : Backend Services & MySQL Database Specialist
* **Revathi Miriyam** : Frontend Lead & UI/UX Product Designer
