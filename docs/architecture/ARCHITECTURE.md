# SupplyCompare — Technical Architecture Document

## 1. System Overview

**SupplyCompare** is an enterprise-grade supplier quotation comparison and procurement management system architected specifically for small and medium retail merchants. It solves the fragmentation and opacity of informal supplier price quotes that differ across minimum order quantities (MOQ), delivery logistics surcharges, payment terms, delivery lead times, and units of measurement.

```
+-------------------------------------------------------------------------+
|                              REACT FRONTEND                             |
|          Vite + React 18 + Lucide Icons + Recharts + CSS Modules        |
|    - Retailer Dashboard     - Supplier Directory     - Product Catalog   |
|    - Signature Comparison   - Purchase Order System  - Inventory Ledger  |
|    - Analytics Engine       - Supplier Portal        - Admin Governance  |
+-------------------------------------------------------------------------+
                                     |  HTTP REST (JWT Bearer)
                                     v
+-------------------------------------------------------------------------+
|                          DJANGO REST FRAMEWORK                          |
|             Versioned API Endpoints (/api/v1/) + Token Auth             |
|     /auth/        /catalog/       /suppliers/       /quotations/        |
|     /comparison/  /purchasing/    /inventory/       /analytics/         |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
|                          CORE DOMAIN SERVICES                           |
|  - ComparisonService (Pure business logic, unit conversions, MOQ filter)|
|  - InventoryService (Atomic transaction ledger, receipt idempotency)    |
|  - AnalyticsService (Real-time financial metrics, supplier scorecards)  |
|  - ReportLab PDF Engine (Purchase order document compilation)           |
+-------------------------------------------------------------------------+
                                     |  Django ORM (InnoDB Engine)
                                     v
+-------------------------------------------------------------------------+
|                            MYSQL 8.0 DATABASE                           |
|  - utf8mb4_unicode_ci charset                                           |
|  - Strict Foreign Keys, Indexes on SKUs, POs, and Timestamps            |
|  - Transactional Isolation (STRICT_TRANS_TABLES)                        |
+-------------------------------------------------------------------------+
```

---

## 2. Key Architecture Pillars

### 2.1 Pure Python Quotation Comparison Engine
The comparison engine is strictly separated from HTTP controllers and frontend components. It evaluates:
1. **Unit Normalization**: Translates requested units to quoted units using an extensible conversion factor graph (`1 carton = 24 packets`, `1 quintal = 100 kg`).
2. **Deterministic Eligibility Filtering**:
   - Rejects expired quotations (`valid_until < today`).
   - Rejects inactive or suspended supplier accounts.
   - Enforces Minimum Order Quantity: `quoted_qty_needed >= quotation.moq`.
   - Enforces Supplier Stock Availability: `quoted_qty_needed <= quotation.available_stock`.
   - Enforces Minimum Order Value thresholds.
3. **Multi-Component Cost Breakdown**:
   $$\text{Total Cost} = (\text{Base Merchandise} - \text{Discount}) + \text{Delivery Charge} + \text{Taxes}$$
4. **Ranking & Best Deal Recommendation**:
   Sorts eligible suppliers strictly by `total_cost ASC`, `expected_delivery_days ASC`, and `supplier_rating DESC`. Never recommends a supplier based on unit price alone.

### 2.2 Finite State Machine for Purchase Orders
Purchase orders adhere to strict validated state transitions:
$$\text{draft} \longrightarrow \text{submitted} \longrightarrow \text{confirmed} \longrightarrow \text{shipped} \longrightarrow \text{received}$$
Any order in `draft`, `submitted`, `confirmed`, or `shipped` may transition to `cancelled`. Terminal states `received` and `cancelled` cannot transition further.

### 2.3 Idempotent Transactional Inventory Restocking
The transition to `received` executes within `django.db.transaction.atomic()`. A dedicated boolean guard `is_inventory_stocked` prevents double-counting upon repeated API calls or network retries. Every stock modification is permanently recorded in `StockMovement` with previous stock, delta, resulting stock, and PO reference number.

---

## 3. Security and RBAC Matrix

| Role | Catalog & Quotes | Comparison Engine | Purchase Orders | Inventory Adjust | User Governance |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Retailer** | Full CRUD | Full Access | Create & Receive | Full Access | Profile only |
| **Supplier** | Maintain own quotes | Prohibited | View & Dispatch | Prohibited | Profile only |
| **Admin** | Oversight & Audit | Full Access | Full Access | Audit view | Full User CRUD |

Backend permission classes (`IsRetailer`, `IsSupplier`, `IsPlatformAdmin`) strictly enforce role verification on every API request.
