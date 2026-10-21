# SupplyCompare — Versioned REST API Reference (v1)

Base URL: `http://localhost:8000/api/v1`  
Authentication: HTTP Bearer Token (`Authorization: Bearer <JWT_ACCESS_TOKEN>`)

---

## 1. Authentication Endpoints (`/api/v1/auth/`)

### `POST /auth/register/`
Registers a new retailer or supplier account.
* **Payload**:
```json
{
  "email": "shopkeeper@example.com",
  "password": "SecurePassword123",
  "first_name": "Ramesh",
  "last_name": "Gupta",
  "phone": "+91 98765 43210",
  "role": "retailer",
  "shop_name": "Sri Lakshmi Kirana Stores",
  "shop_type": "kirana",
  "city": "Hyderabad"
}
```
* **Response (201 Created)**:
```json
{
  "message": "Account registered successfully",
  "user": { "id": 1, "email": "shopkeeper@example.com", "role": "retailer" },
  "tokens": { "access": "eyJhbGciOi...", "refresh": "eyJhbGciOi..." }
}
```

### `POST /auth/login/`
Authenticates user and returns JWT token pair.
* **Payload**: `{"email": "retailer@supplycompare.local", "password": "Retailer@123"}`
* **Response (200 OK)**:
```json
{
  "message": "Login successful",
  "user": {
    "id": 2,
    "email": "retailer@supplycompare.local",
    "role": "retailer",
    "full_name": "Ramesh Gupta",
    "retailer_profile": { "shop_name": "Sri Lakshmi Kirana & General Stores", "city": "Hyderabad" }
  },
  "tokens": { "access": "eyJhbGci...", "refresh": "eyJhbGci..." }
}
```

### `GET /auth/me/`
Returns current authenticated user details and profile.

---

## 2. Supplier Quotation Comparison (`/api/v1/comparison/`)

### `GET /comparison/compare/`
The core engine endpoint that executes deterministic multi-supplier evaluation.
* **Query Parameters**:
  - `product_id` (required, int): SKU ID
  - `quantity` (required, float): Desired order quantity
  - `unit` (optional, string): Desired order unit (defaults to standard unit)
* **Response (200 OK)**:
```json
{
  "product": {
    "id": 10,
    "name": "Parle-G Gold Glucose Biscuits (Carton of 24 Packs)",
    "sku": "BSC-PRL-024",
    "standard_unit": "carton"
  },
  "requested_quantity": 10.0,
  "requested_unit": "carton",
  "summary": {
    "total_quotes_evaluated": 3,
    "eligible_count": 1,
    "ineligible_count": 2,
    "potential_savings": 0.0,
    "best_deal_supplier": "Singhania Wholesale Agri Corp",
    "best_deal_total_cost": 9000.0,
    "best_deal_unit_cost": 900.0
  },
  "eligible_suppliers": [
    {
      "quotation_id": 1,
      "supplier_id": 1,
      "supplier_name": "Singhania Wholesale Agri Corp",
      "supplier_rating": 4.8,
      "payment_terms": "Net 15 Days",
      "quoted_unit": "carton",
      "unit_price": 900.0,
      "moq": 5.0,
      "available_stock": 100.0,
      "delivery_charge": 0.0,
      "expected_delivery_days": 2,
      "is_eligible": true,
      "is_best_deal": true,
      "base_cost": 9000.0,
      "discount_amount": 0.0,
      "effective_delivery_charge": 0.0,
      "tax_amount": 0.0,
      "total_cost": 9000.0,
      "effective_unit_cost": 900.0,
      "exclusion_reason": "Eligible for your requested quantity."
    }
  ],
  "ineligible_suppliers": [
    {
      "quotation_id": 2,
      "supplier_id": 3,
      "supplier_name": "Balaji FMCG Distributors",
      "unit_price": 870.0,
      "moq": 15.0,
      "is_eligible": false,
      "is_best_deal": false,
      "exclusion_reason": "Minimum order is 15 carton (your order requires 10 carton)."
    }
  ]
}
```

---

## 3. Purchase Orders (`/api/v1/purchasing/`)

### `GET /purchasing/`
Lists purchase orders for authenticated user with status filtering (`?status=draft,submitted,confirmed,shipped,received,cancelled`).

### `POST /purchasing/`
Creates a new purchase order directly from an evaluated quotation.
* **Payload**:
```json
{
  "quotation_id": 1,
  "quantity": 10.0,
  "delivery_address": "Plot 42, Main Road, KPHB Colony, Hyderabad",
  "notes": "Express delivery requested"
}
```

### `POST /purchasing/{id}/transition/`
Advances purchase order status through the finite state machine.
* **Payload**: `{"status": "shipped", "notes": "Dispatched via vehicle AP-28-V-1234"}`

### `POST /purchasing/{id}/receive/`
Receives delivery dock items, records physical discrepancy, and updates inventory stock atomically.
* **Payload**:
```json
{
  "items": [
    {
      "item_id": 12,
      "quantity_received": 10.0,
      "quantity_damaged": 0.0,
      "discrepancy_notes": "Cartons intact and seals verified"
    }
  ],
  "notes": "Verified by shopkeeper"
}
```

### `GET /purchasing/{id}/pdf/`
Streams official purchase order PDF compiled with ReportLab.

---

## 4. Inventory Control (`/api/v1/inventory/`)

### `GET /inventory/stock/`
Retrieves current stock balance with optional low stock filter (`?low_stock=true`).

### `POST /inventory/adjust/`
Records physical audit count adjustment with reason code and audit ledger trail.
* **Payload**:
```json
{
  "product_id": 10,
  "new_quantity": 25.0,
  "reason": "adjustment_add",
  "notes": "Physical audit recount"
}
```

### `GET /inventory/movements/`
Retrieves chronological audit trail of all inventory increases, deductions, and PO receipts.

---

## 5. Procurement Analytics (`/api/v1/analytics/`)

* `GET /analytics/dashboard/`: Key performance indicators and savings potential.
* `GET /analytics/supplier-spending/`: Total procurement spend grouped by supplier.
* `GET /analytics/top-products/`: Top purchased products by volume and spending.
* `GET /analytics/supplier-performance/`: Supplier on-time delivery rates and promised lead days.
* `GET /analytics/spend-trends/`: Monthly procurement expenditure history.
