# SupplyCompare — Relational Database Schema & Architecture

## Database Engine & Charset
* **Engine**: MySQL 8.0 `InnoDB` (ACID Compliant Transactions)
* **Default Charset**: `utf8mb4`
* **Collation**: `utf8mb4_unicode_ci`
* **SQL Mode**: `STRICT_TRANS_TABLES`

---

## Entity Relationship Overview

```
 [auth_users] 1 ----- 1 [retailer_profiles]
      |       1 ----- 1 [supplier_profiles]
      |
      +------- 1:N ---- [purchasing_orders] 1:N ---- [purchasing_order_items]
      |                         |                             |
      |                         +--- 1:N -- [purchasing_order_history]
      |                         |
      +------- 1:N ---- [inventory_stock_items]
      |                         |
      +------- 1:N ---- [inventory_stock_movements]
      |
 [catalog_categories] 1:N ---- [catalog_products] 1:N ---- [catalog_unit_conversions]
                                      |
                                      +--- 1:N --- [quotations]
                                                        |
 [suppliers] 1:N ---------------------------------------+
```

---

## Detailed Table Specifications

### 1. `auth_users`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Unique User Identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Login Username & Communication |
| `password` | VARCHAR(128) | NOT NULL | PBKDF2/Argon2 Cryptographic Hash |
| `first_name` | VARCHAR(150) | NULLABLE | Given Name |
| `last_name` | VARCHAR(150) | NULLABLE | Family Name |
| `phone` | VARCHAR(20) | NULLABLE | Mobile Phone Number |
| `role` | VARCHAR(20) | NOT NULL, INDEX, DEFAULT 'retailer' | Enum: `retailer`, `supplier`, `admin` |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Account Access Status |
| `is_staff` | BOOLEAN | NOT NULL, DEFAULT FALSE | Administrative Privilege |
| `date_joined`| DATETIME | NOT NULL | Timestamp of registration |

### 2. `retailer_profiles`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Profile Identifier |
| `user_id` | BIGINT | UNIQUE, FK -> `auth_users.id` ON DELETE CASCADE | Associated Retailer User |
| `shop_name` | VARCHAR(200) | NOT NULL | Registered Store Name |
| `gstin` | VARCHAR(30) | NULLABLE | Goods & Services Tax ID |
| `shop_type` | VARCHAR(30) | NOT NULL, DEFAULT 'kirana' | Enum: `kirana`, `supermarket`, `convenience`, etc. |
| `address_line` | VARCHAR(255)| NULLABLE | Physical Street Address |
| `city` | VARCHAR(100) | NOT NULL, DEFAULT 'Hyderabad' | Municipal Jurisdiction |
| `state` | VARCHAR(100) | NOT NULL, DEFAULT 'Telangana' | State / Province |
| `pincode` | VARCHAR(20) | NULLABLE | Postal Code |
| `currency` | VARCHAR(10) | NOT NULL, DEFAULT 'INR' | Operating Currency |

### 3. `catalog_categories`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Category ID |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Display Category Name |
| `slug` | VARCHAR(120) | UNIQUE, NOT NULL | URL-Safe Slug |
| `description`| TEXT | NULLABLE | Category Scope |
| `icon_name` | VARCHAR(50) | DEFAULT 'Package' | Lucide UI Icon Identifier |
| `is_active` | BOOLEAN | DEFAULT TRUE | Active in Catalog |

### 4. `catalog_products`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Product ID |
| `name` | VARCHAR(200) | NOT NULL, INDEX | Commercial Product Title |
| `sku` | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Stock Keeping Unit Barcode/Code |
| `category_id`| BIGINT | FK -> `catalog_categories.id` ON DELETE SET NULL | Product Classification |
| `brand` | VARCHAR(100) | NULLABLE, INDEX | Brand / Manufacturer |
| `standard_unit`| VARCHAR(30)| NOT NULL, DEFAULT 'piece' | Standard Inventory Measurement Unit |
| `min_stock_alert`| DECIMAL(10,2)| DEFAULT 10.00 | Safety Reorder Threshold |
| `target_purchase_price`| DECIMAL(12,2)| NULLABLE | Target Benchmark Price in INR |
| `is_active` | BOOLEAN | DEFAULT TRUE | Active in Ordering |

### 5. `catalog_unit_conversions`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Conversion Rule ID |
| `product_id`| BIGINT | FK -> `catalog_products.id` ON DELETE CASCADE (NULL = global) | Product Context |
| `from_unit` | VARCHAR(30) | NOT NULL | Source Unit (e.g. carton) |
| `to_unit` | VARCHAR(30) | NOT NULL | Destination Unit (e.g. packet) |
| `conversion_factor`| DECIMAL(12,4)| NOT NULL | $1 \text{ from\_unit} = \text{factor} \times \text{to\_unit}$ |

### 6. `suppliers`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Supplier Identifier |
| `name` | VARCHAR(200) | NOT NULL, INDEX | Distributor Business Name |
| `gstin` | VARCHAR(30) | NULLABLE | Tax Identifier |
| `contact_person`| VARCHAR(150)| NOT NULL | Primary Sales Representative |
| `phone` | VARCHAR(30) | NOT NULL, INDEX | Phone Contact |
| `email` | VARCHAR(254) | NULLABLE | Dispatch Email |
| `payment_terms`| VARCHAR(30) | NOT NULL, DEFAULT 'net_15' | Terms: `cod`, `advance`, `net_7`, `net_15`, `net_30` |
| `delivery_lead_days`| INT UNSIGNED | DEFAULT 2 | Average Promised Lead Time in Days |
| `rating` | DECIMAL(3,2) | DEFAULT 4.50 | Performance Rating (out of 5.0) |
| `status` | VARCHAR(20) | DEFAULT 'active', INDEX | Status: `active`, `inactive`, `archived` |

### 7. `quotations`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Quotation Identifier |
| `supplier_id`| BIGINT | FK -> `suppliers.id` ON DELETE CASCADE | Quoting Distributor |
| `product_id` | BIGINT | FK -> `catalog_products.id` ON DELETE CASCADE | Target SKU |
| `quoted_unit`| VARCHAR(30) | DEFAULT 'piece' | Unit Priced (e.g. carton, bag) |
| `unit_price` | DECIMAL(12,2)| NOT NULL | Base Rate per Quoted Unit (INR) |
| `moq` | DECIMAL(10,2)| NOT NULL, DEFAULT 1.00 | Minimum Order Quantity |
| `available_stock`| DECIMAL(10,2)| DEFAULT 9999.00 | Current Distributor Inventory |
| `delivery_charge`| DECIMAL(10,2)| DEFAULT 0.00 | Logistics Charge in INR |
| `free_delivery_threshold`| DECIMAL(12,2)| DEFAULT 0.00 | Free Shipping Order Value Target |
| `expected_delivery_days`| INT UNSIGNED | DEFAULT 2 | Quoted Transit Days |
| `discount_type`| VARCHAR(20)| DEFAULT 'none' | `none`, `flat`, `percentage` |
| `discount_value`| DECIMAL(10,2)| DEFAULT 0.00 | Numerical Discount |
| `tax_percentage`| DECIMAL(5,2)| DEFAULT 0.00 | GST Tax Rate (0%, 5%, 12%, 18%) |
| `valid_until`| DATE | NOT NULL, INDEX | Expiration Cutoff Date |
| `status` | VARCHAR(20) | DEFAULT 'active', INDEX | `active`, `expired`, `archived` |

### 8. `purchasing_orders`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | PO Identifier |
| `po_number` | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Document Number (e.g. `PO-2026-0001`) |
| `retailer_id`| BIGINT | FK -> `auth_users.id` ON DELETE CASCADE | Purchasing Merchant |
| `supplier_id`| BIGINT | FK -> `suppliers.id` ON DELETE CASCADE | Fulfilling Supplier |
| `source_quotation_id`| BIGINT| FK -> `quotations.id` ON DELETE SET NULL | Originating Quotation Reference |
| `order_date` | DATE | NOT NULL | Booking Date |
| `expected_delivery_date`| DATE | NULLABLE | Scheduled Receiving Date |
| `actual_delivery_date`| DATE | NULLABLE | Physical Delivery Date |
| `status` | VARCHAR(20) | DEFAULT 'draft', INDEX | `draft`, `submitted`, `confirmed`, `shipped`, `received`, `cancelled` |
| `subtotal` | DECIMAL(12,2)| DEFAULT 0.00 | Merchandise Subtotal |
| `discount_amount`| DECIMAL(12,2)| DEFAULT 0.00 | Total Discount |
| `delivery_charge`| DECIMAL(10,2)| DEFAULT 0.00 | Logistics Fee |
| `tax_amount` | DECIMAL(10,2)| DEFAULT 0.00 | Calculated GST |
| `total_amount`| DECIMAL(12,2)| DEFAULT 0.00 | Final Invoice Payable Amount |
| `is_inventory_stocked`| BOOLEAN| DEFAULT FALSE | Idempotency guard against double-receipt |

### 9. `inventory_stock_items`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Stock ID |
| `user_id` | BIGINT | FK -> `auth_users.id` ON DELETE CASCADE | Shopkeeper Identity |
| `product_id` | BIGINT | FK -> `catalog_products.id` ON DELETE CASCADE | SKU Item |
| `current_stock`| DECIMAL(12,2)| DEFAULT 0.00 | Physical On-Hand Balance |
| `low_stock_threshold`| DECIMAL(10,2)| DEFAULT 10.00 | Warning Trigger Level |
| `last_restocked_at`| DATETIME| NULLABLE | Last Inward PO Date |

### 10. `inventory_stock_movements`
| Column | Type | Constraints / Attributes | Description |
| :--- | :--- | :--- | :--- |
| `id` | BIGINT | PRIMARY KEY, AUTO_INCREMENT | Movement ID |
| `user_id` | BIGINT | FK -> `auth_users.id` ON DELETE CASCADE | Shopkeeper |
| `product_id` | BIGINT | FK -> `catalog_products.id` ON DELETE CASCADE | SKU Item |
| `movement_type`| VARCHAR(30)| NOT NULL, INDEX | `purchase_receipt`, `adjustment_add`, `adjustment_subtract`, `damaged`, `sale`, `supplier_return` |
| `quantity_delta`| DECIMAL(10,2)| NOT NULL | Net Change (+/-) |
| `previous_stock`| DECIMAL(12,2)| NOT NULL | Pre-transaction Stock |
| `resulting_stock`| DECIMAL(12,2)| NOT NULL | Post-transaction Stock |
| `reference_id`| VARCHAR(100)| NULLABLE | PO Number or Reference Code |
| `timestamp` | DATETIME | NOT NULL, INDEX | Immutable Audit Time |
