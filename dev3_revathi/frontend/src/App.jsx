import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import AppLayout from './layouts/AppLayout';

import Login from './pages/auth/Login';
import Register from './pages/auth/Register';
import RetailerDashboard from './pages/dashboard/RetailerDashboard';
import SupplierDirectory from './pages/suppliers/SupplierDirectory';
import ProductCatalog from './pages/catalog/ProductCatalog';
import QuotationWorkspace from './pages/quotations/QuotationWorkspace';
import SupplierComparison from './pages/comparison/SupplierComparison';
import PurchaseOrdersList from './pages/purchasing/PurchaseOrdersList';
import PurchaseOrderDetail from './pages/purchasing/PurchaseOrderDetail';
import InventoryManagement from './pages/inventory/InventoryManagement';
import AnalyticsDashboard from './pages/analytics/AnalyticsDashboard';
import SupplierPortal from './pages/supplier_portal/SupplierPortal';
import AdminDashboard from './pages/admin/AdminDashboard';

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Application Routes */}
          <Route path="/" element={<AppLayout />}>
            <Route index element={<RetailerDashboard />} />
            <Route path="suppliers" element={<SupplierDirectory />} />
            <Route path="catalog" element={<ProductCatalog />} />
            <Route path="quotations" element={<QuotationWorkspace />} />
            <Route path="compare" element={<SupplierComparison />} />
            <Route path="purchase-orders" element={<PurchaseOrdersList />} />
            <Route path="purchase-orders/:id" element={<PurchaseOrderDetail />} />
            <Route path="inventory" element={<InventoryManagement />} />
            <Route path="analytics" element={<AnalyticsDashboard />} />
            <Route path="supplier-portal" element={<SupplierPortal />} />
            <Route path="admin" element={<AdminDashboard />} />
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
