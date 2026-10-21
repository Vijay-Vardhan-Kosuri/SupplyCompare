# SupplyCompare — Retailer & Shopkeeper User Guide

Welcome to **SupplyCompare**, your central procurement cockpit for comparing multi-supplier quotes, cutting wholesale purchase costs, and tracking inventory replenishments.

---

## 1. Navigating Your Dashboard
Upon logging in as a Retailer, your dashboard provides real-time visibility into:
1. **Total Purchasing Spend**: Total expenditure across completed and in-transit orders.
2. **Calculated Potential Savings**: Financial savings identified across competitive product categories when selecting optimal eligible quotes over highest rates.
3. **Low Stock Warnings**: Instant alerts for inventory items falling below safety reorder levels.
4. **Instant Comparison Launcher**: Jump straight into quotation analysis with a single click.

---

## 2. Using the Signature Quotation Comparison Engine
The Comparison Engine is located at `/compare`.

### Step 1: Select SKU & Enter Quantity
* Select your target product (e.g. *Parle-G Gold Biscuits (Carton of 24 Packs)*).
* Enter the quantity you wish to order (e.g. `10` or `15`).
* Specify your desired unit (or accept standard unit).

### Step 2: Review Side-by-Side Supplier Cards
The engine deterministically calculates all supplier offers and presents them side-by-side:
* **Best Total Deal**: The lowest total cost supplier among all **eligible** quotes is marked with the **Best Total Deal** badge.
* **Eligible Suppliers**: Displays the complete cost breakdown:
  $$\text{Total Order Cost} = \text{Base Goods} - \text{Discount} + \text{Logistics Fee} + \text{Taxes}$$
* **Ineligible Suppliers**: Clearly displays why a supplier cannot fulfill the request (e.g., *"Minimum order is 15 cartons (your order requires 10 cartons)"* or *"Quotation expired"*).

### Step 3: Issue a Purchase Order
Click **Create Purchase Order** on the winning supplier's card. Confirm your delivery dock address and instructions. The purchase order is automatically created in `draft` status.

---

## 3. Managing Purchase Orders & Receiving Goods
1. Navigate to **Purchase Orders** (`/purchase-orders`).
2. Track orders through their lifecycle: `Draft` $\rightarrow$ `Submitted` $\rightarrow$ `Confirmed` $\rightarrow$ `In-Transit`.
3. Download or print official Purchase Order PDFs via **Export PDF**.
4. When delivery arrives at your store dock, click **Receive Goods & Stock Inventory**:
   - Verify physical counts.
   - Record good units vs damaged units.
   - Click confirm to atomically restock your inventory!
