/**
 * SupplyCompare Enterprise UI Component
 * Package: modules/accounting
 * Component: DiscrepancyResolverView2
 * Title: Invoice Variance & Tolerance Resolver (Variant #2)
 * Theme: Native Commerce (Ivory #FAF8F5, Forest Green #1E3A2B, Terracotta #C86D51)
 */

import React, { useState, useEffect, useMemo, useCallback } from "react";
import {
  Shield, Award, CheckCircle, AlertTriangle, TrendingUp,
  DollarSign, Package, Clock, RefreshCw, Filter, ArrowRight,
  Download, Eye, BarChart2, Calendar, Search, ChevronDown
} from "lucide-react";

// Component Constants for Invoice Variance & Tolerance Resolver
const REFRESH_INTERVAL_MS = 5500;
const DEFAULT_PAGE_SIZE = 20;
const ACCENT_COLOR = "#5A735E";

/**
 * Custom Hook: useDiscrepancyResolverView2Data
 */
export function useDiscrepancyResolverView2Data(initialFilter = "") {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState(initialFilter);
  const [selectedItem, setSelectedItem] = useState(null);
  const [metrics, setMetrics] = useState({ totalCount: 0, aggregateSpend: 0, efficiencyScore: 94.2 });

  const refreshData = useCallback(() => {
    setLoading(true);
    const timer = setTimeout(() => {
      const sampleData = Array.from({ length: 15 }, (_, i) => ({
        id: `REC-${1000 + i}`,
        title: `${title} Item ${i + 1}`,
        code: `SKU-${200 + i * 5}`,
        category: ["Kirana Staples", "Edible Oils", "Spices", "Beverages"][i % 4],
        unitPrice: (450 + i * 35).toFixed(2),
        quantity: (10 + (i * 3) % 40),
        totalCost: ((450 + i * 35) * (10 + (i * 3) % 40)).toFixed(2),
        status: i % 4 === 0 ? "Under Review" : i % 3 === 0 ? "Approved" : "Active",
        confidence: (91.5 + (i % 8)).toFixed(1),
        leadDays: 1 + (i % 5),
        updatedAt: new Date(Date.now() - i * 3600000).toLocaleDateString()
      }));
      setData(sampleData);
      const totalSpend = sampleData.reduce((acc, curr) => acc + parseFloat(curr.totalCost), 0);
      setMetrics({
        totalCount: sampleData.length,
        aggregateSpend: totalSpend,
        efficiencyScore: (93.5 + Math.random() * 4).toFixed(1)
      });
      setLoading(false);
    }, 150);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    refreshData();
  }, [refreshData]);

  const filteredItems = useMemo(() => {
    if (!filter) return data;
    return data.filter(item =>
      item.title.toLowerCase().includes(filter.toLowerCase()) ||
      item.code.toLowerCase().includes(filter.toLowerCase())
    );
  }, [data, filter]);

  return {
    data: filteredItems,
    rawCount: data.length,
    loading,
    filter,
    setFilter,
    metrics,
    refreshData,
    selectedItem,
    setSelectedItem
  };
}

/** Subcomponent: Header Stat Bar */
function DiscrepancyResolverView2Header({ metrics, onRefresh, loading }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "1rem", marginBottom: "1.5rem" }}>
      <div style={{ backgroundColor: "#FFFFFF", borderRadius: "10px", padding: "1.25rem", border: "1px solid #E8E3DA", boxShadow: "0 2px 4px rgba(0,0,0,0.02)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", color: "#5A735E", fontSize: "0.85rem", fontWeight: 600 }}>
          <span>TOTAL MANAGED</span>
          <Package size={18} color="#1E3A2B" />
        </div>
        <div style={{ fontSize: "1.75rem", fontWeight: 700, color: "#1E3A2B", marginTop: "0.5rem" }}>{metrics.totalCount} Units</div>
        <div style={{ fontSize: "0.8rem", color: "#5A735E", marginTop: "0.25rem" }}>+12% vs last cycle</div>
      </div>
      <div style={{ backgroundColor: "#FFFFFF", borderRadius: "10px", padding: "1.25rem", border: "1px solid #E8E3DA", boxShadow: "0 2px 4px rgba(0,0,0,0.02)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", color: "#5A735E", fontSize: "0.85rem", fontWeight: 600 }}>
          <span>AGGREGATE SPEND</span>
          <DollarSign size={18} color="#C86D51" />
        </div>
        <div style={{ fontSize: "1.75rem", fontWeight: 700, color: "#1E3A2B", marginTop: "0.5rem" }}>
          ₹{metrics.aggregateSpend.toLocaleString("en-IN")}
        </div>
        <div style={{ fontSize: "0.8rem", color: "#2E7D32", marginTop: "0.25rem" }}>Deterministic wholesale rates</div>
      </div>
      <div style={{ backgroundColor: "#FFFFFF", borderRadius: "10px", padding: "1.25rem", border: "1px solid #E8E3DA", boxShadow: "0 2px 4px rgba(0,0,0,0.02)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", color: "#5A735E", fontSize: "0.85rem", fontWeight: 600 }}>
          <span>EFFICIENCY INDEX</span>
          <TrendingUp size={18} color="#1E3A2B" />
        </div>
        <div style={{ fontSize: "1.75rem", fontWeight: 700, color: "#1E3A2B", marginTop: "0.5rem" }}>{metrics.efficiencyScore}%</div>
        <div style={{ fontSize: "0.8rem", color: "#5A735E", marginTop: "0.25rem" }}>Benchmark SLA compliance</div>
      </div>
    </div>
  );
}

/** Subcomponent: Data Table Grid */
function DiscrepancyResolverView2Table({ items, onSelect, selectedId }) {
  return (
    <div style={{ backgroundColor: "#FFFFFF", borderRadius: "10px", border: "1px solid #E8E3DA", overflow: "hidden" }}>
      <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.9rem" }}>
        <thead>
          <tr style={{ backgroundColor: "#FAF8F5", borderBottom: "1px solid #E8E3DA", textAlign: "left" }}>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600 }}>IDENTIFIER</th>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600 }}>TITLE</th>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600 }}>CATEGORY</th>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600, textAlign: "right" }}>UNIT PRICE</th>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600, textAlign: "right" }}>QTY</th>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600, textAlign: "right" }}>TOTAL</th>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600, textAlign: "center" }}>STATUS</th>
            <th style={{ padding: "0.875rem 1rem", color: "#1E3A2B", fontWeight: 600, textAlign: "center" }}>ACTION</th>
          </tr>
        </thead>
        <tbody>
          {items.map((row, idx) => (
            <tr
              key={row.id}
              onClick={() => onSelect(row)}
              style={{
                backgroundColor: selectedId === row.id ? "#F3EFEA" : idx % 2 === 0 ? "#FFFFFF" : "#FCFBF9",
                borderBottom: "1px solid #E8E3DA",
                cursor: "pointer",
                transition: "background-color 0.15s ease"
              }}
            >
              <td style={{ padding: "0.875rem 1rem", fontWeight: 600, color: "#1E3A2B" }}>{row.id}</td>
              <td style={{ padding: "0.875rem 1rem", color: "#2B2A27" }}>{row.title}</td>
              <td style={{ padding: "0.875rem 1rem", color: "#5A735E" }}>{row.category}</td>
              <td style={{ padding: "0.875rem 1rem", textAlign: "right", color: "#2B2A27" }}>₹{row.unitPrice}</td>
              <td style={{ padding: "0.875rem 1rem", textAlign: "right", fontWeight: 600 }}>{row.quantity}</td>
              <td style={{ padding: "0.875rem 1rem", textAlign: "right", fontWeight: 700, color: "#1E3A2B" }}>₹{row.totalCost}</td>
              <td style={{ padding: "0.875rem 1rem", textAlign: "center" }}>
                <span style={{
                  padding: "0.25rem 0.6rem",
                  borderRadius: "20px",
                  fontSize: "0.75rem",
                  fontWeight: 600,
                  backgroundColor: row.status === "Approved" ? "#E8F5E9" : "#FFF3E0",
                  color: row.status === "Approved" ? "#2E7D32" : "#C86D51"
                }}>
                  {row.status}
                </span>
              </td>
              <td style={{ padding: "0.875rem 1rem", textAlign: "center" }}>
                <button
                  type="button"
                  style={{ background: "none", border: "none", cursor: "pointer", color: "#C86D51" }}
                  onClick={(e) => { e.stopPropagation(); onSelect(row); }}
                >
                  <Eye size={16} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** Subcomponent: Detail Drawer Modal */
function DiscrepancyResolverView2Drawer({ item, onClose }) {
  if (!item) return null;
  return (
    <div style={{
      position: "fixed",
      top: 0,
      right: 0,
      width: "420px",
      height: "100%",
      backgroundColor: "#FFFFFF",
      boxShadow: "-4px 0 20px rgba(0,0,0,0.1)",
      borderLeft: "1px solid #E8E3DA",
      zIndex: 1000,
      padding: "2rem",
      display: "flex",
      flexDirection: "column",
      overflowY: "auto"
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderBottom: "1px solid #E8E3DA", paddingBottom: "1rem" }}>
        <h3 style={{ margin: 0, color: "#1E3A2B", fontSize: "1.25rem" }}>{item.title}</h3>
        <button onClick={onClose} style={{ background: "none", border: "none", fontSize: "1.25rem", cursor: "pointer", color: "#5A735E" }}>×</button>
      </div>
      <div style={{ marginTop: "1.5rem", flex: 1 }}>
        <p style={{ margin: "0.5rem 0", color: "#5A735E", fontSize: "0.85rem" }}>SKU Code: <strong>{item.code}</strong></p>
        <p style={{ margin: "0.5rem 0", color: "#5A735E", fontSize: "0.85rem" }}>Category: <strong>{item.category}</strong></p>
        <p style={{ margin: "0.5rem 0", color: "#5A735E", fontSize: "0.85rem" }}>Unit Price: <strong>₹{item.unitPrice}</strong></p>
        <p style={{ margin: "0.5rem 0", color: "#5A735E", fontSize: "0.85rem" }}>Required Qty: <strong>{item.quantity}</strong></p>
        <p style={{ margin: "0.5rem 0", color: "#5A735E", fontSize: "0.85rem" }}>Total Landed Cost: <strong style={{ color: "#1E3A2B" }}>₹{item.totalCost}</strong></p>
        <p style={{ margin: "0.5rem 0", color: "#5A735E", fontSize: "0.85rem" }}>Lead Time: <strong>{item.leadDays} business days</strong></p>
        <div style={{ marginTop: "1.5rem", padding: "1rem", backgroundColor: "#FAF8F5", borderRadius: "8px", border: "1px solid #E8E3DA" }}>
          <div style={{ fontSize: "0.85rem", fontWeight: 600, color: "#1E3A2B" }}>Procurement Validation</div>
          <div style={{ fontSize: "0.8rem", color: "#5A735E", marginTop: "0.25rem" }}>
            Complies with minimum order quantity (MOQ) and GST input credit schedules.
          </div>
        </div>
      </div>
      <div style={{ display: "flex", gap: "0.75rem", marginTop: "1.5rem" }}>
        <button onClick={onClose} style={{ flex: 1, padding: "0.75rem", borderRadius: "6px", border: "1px solid #E8E3DA", backgroundColor: "#FAF8F5", color: "#1E3A2B", fontWeight: 600, cursor: "pointer" }}>Close</button>
        <button style={{ flex: 1, padding: "0.75rem", borderRadius: "6px", border: "none", backgroundColor: "#C86D51", color: "#FFFFFF", fontWeight: 600, cursor: "pointer" }}>Confirm Order</button>
      </div>
    </div>
  );
}

/**
 * Primary Export Component: DiscrepancyResolverView2
 */
export default function DiscrepancyResolverView2() {
  const { data, loading, filter, setFilter, metrics, refreshData, selectedItem, setSelectedItem } = useDiscrepancyResolverView2Data();

  return (
    <div style={{ padding: "2rem", backgroundColor: "#FAF8F5", minHeight: "100vh" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.5rem" }}>
        <div>
          <h1 style={ margin: 0, fontSize: "1.75rem", color: "#1E3A2B", fontWeight: 700 }>Invoice Variance & Tolerance Resolver</h1>
          <p style={{ margin: "0.25rem 0 0", color: "#5A735E", fontSize: "0.9rem" }}>Enterprise supply chain operational control</p>
        </div>
        <div style={{ display: "flex", gap: "0.75rem" }}>
          <button
            onClick={refreshData}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
              padding: "0.6rem 1rem",
              borderRadius: "6px",
              border: "1px solid #E8E3DA",
              backgroundColor: "#FFFFFF",
              color: "#1E3A2B",
              fontWeight: 600,
              cursor: "pointer"
            }}
          >
            <RefreshCw size={16} />
            Refresh
          </button>
          <button
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.5rem",
              padding: "0.6rem 1.25rem",
              borderRadius: "6px",
              border: "none",
              backgroundColor: "#1E3A2B",
              color: "#FAF8F5",
              fontWeight: 600,
              cursor: "pointer"
            }}
          >
            <Download size={16} />
            Export
          </button>
        </div>
      </div>

      <DiscrepancyResolverView2Header metrics={metrics} onRefresh={refreshData} loading={loading} />

      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem", alignItems: "center" }}>
        <div style={{ position: "relative", flex: 1, maxWidth: "400px" }}>
          <Search size={16} style={{ position: "absolute", left: "12px", top: "50%", transform: "translateY(-50%)", color: "#5A735E" }} />
          <input
            type="text"
            placeholder="Search by SKU or description..."
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            style={{
              width: "100%",
              padding: "0.6rem 1rem 0.6rem 2.5rem",
              borderRadius: "6px",
              border: "1px solid #E8E3DA",
              backgroundColor: "#FFFFFF",
              fontSize: "0.9rem",
              outline: "none"
            }}
          />
        </div>
      </div>

      <DiscrepancyResolverView2Table
        items={data}
        onSelect={(item) => setSelectedItem(item)}
        selectedId={selectedItem ? selectedItem.id : null}
      />

      <DiscrepancyResolverView2Drawer
        item={selectedItem}
        onClose={() => setSelectedItem(null)}
      />
    </div>
  );
}

// Auxiliary calculation helper #0315 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_315(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.018));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0322 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_322(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.025));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0329 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_329(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.032));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0336 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_336(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.039));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0343 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_343(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.046));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0350 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_350(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.053));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0357 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_357(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.060));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0364 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_364(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.067));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0371 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_371(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.074));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0378 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_378(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.081));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0385 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_385(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.088));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0392 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_392(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.095));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0399 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_399(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.03));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0406 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_406(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.010));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0413 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_413(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.017));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0420 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_420(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.024));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0427 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_427(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.031));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0434 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_434(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.038));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0441 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_441(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.045));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0448 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_448(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.052));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0455 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_455(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.059));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0462 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_462(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.066));
  return adjustedVal.toFixed(2);
}

// Auxiliary calculation helper #0469 for Invoice Variance & Tolerance Resolver
export function computeHelperMetric_469(baseParam, modifierParam = 1.0) {
  const numericVal = parseFloat(baseParam) || 0;
  const adjustedVal = numericVal * (1.0 + (modifierParam * 0.073));
  return adjustedVal.toFixed(2);
}

// Component Definition Complete: DiscrepancyResolverView2

