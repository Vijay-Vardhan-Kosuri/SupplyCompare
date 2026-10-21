import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import {
  LayoutDashboard,
  Users,
  Package,
  FileSpreadsheet,
  ArrowRightLeft,
  ShoppingCart,
  Boxes,
  BarChart3,
  ShieldCheck,
  Truck,
  LogOut,
  Store,
  Sparkles
} from 'lucide-react';

const Sidebar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const shopName = user?.retailer_profile?.shop_name ||
                   user?.supplier_profile?.business_name ||
                   'Retail Enterprise';

  const navItems = [
    { label: 'Overview', to: '/', icon: LayoutDashboard },
    { label: 'Suppliers', to: '/suppliers', icon: Users },
    { label: 'Product Catalog', to: '/catalog', icon: Package },
    { label: 'Quotations', to: '/quotations', icon: FileSpreadsheet },
    {
      label: 'Compare Suppliers',
      to: '/compare',
      icon: ArrowRightLeft,
      highlight: true,
      badge: 'Signature'
    },
    { label: 'Purchase Orders', to: '/purchase-orders', icon: ShoppingCart },
    { label: 'Inventory', to: '/inventory', icon: Boxes },
    { label: 'Analytics', to: '/analytics', icon: BarChart3 },
  ];

  if (user?.role === 'admin' || user?.is_staff) {
    navItems.push({ label: 'Platform Admin', to: '/admin', icon: ShieldCheck });
  }

  if (user?.role === 'supplier') {
    navItems.push({ label: 'Supplier Portal', to: '/supplier-portal', icon: Truck });
  }

  return (
    <aside style={styles.sidebar}>
      {/* Brand & Wordmark */}
      <div style={styles.brandContainer}>
        <div style={styles.logoMark}>
          <svg width="22" height="22" viewBox="0 0 32 32" fill="none">
            <rect width="32" height="32" rx="8" fill="#1E3A2B" />
            <path d="M8 12L16 7L24 12V21L16 26L8 21V12Z" stroke="#FAF8F5" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" />
            <circle cx="16" cy="16" r="3" fill="#C86D51" />
          </svg>
        </div>
        <div>
          <div style={styles.brandName}>SupplyCompare</div>
          <div style={styles.brandSub}>Retail Procurement</div>
        </div>
      </div>

      {/* Shop / Workspace Badge */}
      <div style={styles.workspaceCard}>
        <div style={styles.workspaceIcon}>
          <Store size={15} color="#5A735E" />
        </div>
        <div style={styles.workspaceText}>
          <div style={styles.workspaceLabel}>Active Shop</div>
          <div style={styles.workspaceName} title={shopName}>{shopName}</div>
        </div>
      </div>

      {/* Navigation */}
      <nav style={styles.nav}>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              style={({ isActive }) => ({
                ...styles.navLink,
                ...(isActive ? styles.navLinkActive : {}),
                ...(item.highlight ? styles.navLinkHighlight : {}),
              })}
            >
              <Icon size={18} strokeWidth={1.9} />
              <span style={{ flex: 1 }}>{item.label}</span>
              {item.badge && (
                <span style={styles.highlightBadge}>
                  <Sparkles size={11} style={{ marginRight: 3 }} />
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* User Profile Footer */}
      <div style={styles.footer}>
        <div style={styles.userInfo}>
          <div style={styles.avatar}>
            {user?.first_name ? user.first_name[0].toUpperCase() : 'U'}
          </div>
          <div style={styles.userMeta}>
            <div style={styles.userName}>{user?.full_name || 'Store Owner'}</div>
            <div style={styles.userRole}>
              {user?.role ? user.role.toUpperCase() : 'RETAILER'}
            </div>
          </div>
        </div>
        <button
          onClick={handleLogout}
          style={styles.logoutBtn}
          title="Sign Out"
        >
          <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
};

const styles = {
  sidebar: {
    position: 'fixed',
    top: 0,
    left: 0,
    bottom: 0,
    width: 'var(--sidebar-width)',
    backgroundColor: 'var(--bg-sidebar)',
    borderRight: '1px solid var(--border-subtle)',
    display: 'flex',
    flexDirection: 'column',
    padding: 'var(--space-lg) var(--space-md)',
    zIndex: 100,
  },
  brandContainer: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: 'var(--space-lg)',
    paddingLeft: 'var(--space-xs)',
  },
  logoMark: {
    width: '32px',
    height: '32px',
    borderRadius: '8px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  brandName: {
    fontSize: '1.05rem',
    fontWeight: '800',
    color: 'var(--primary)',
    letterSpacing: '-0.02em',
    lineHeight: 1.1,
  },
  brandSub: {
    fontSize: '0.72rem',
    color: 'var(--text-muted)',
    fontWeight: '500',
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
  },
  workspaceCard: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    padding: '10px 12px',
    backgroundColor: 'var(--bg-card)',
    border: '1px solid var(--border-subtle)',
    borderRadius: 'var(--radius-sm)',
    marginBottom: 'var(--space-lg)',
  },
  workspaceIcon: {
    width: '28px',
    height: '28px',
    borderRadius: '6px',
    backgroundColor: 'var(--primary-light)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  workspaceText: {
    overflow: 'hidden',
  },
  workspaceLabel: {
    fontSize: '0.6875rem',
    color: 'var(--text-muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
  },
  workspaceName: {
    fontSize: '0.8125rem',
    fontWeight: '600',
    color: 'var(--text-main)',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  nav: {
    display: 'flex',
    flexDirection: 'column',
    gap: '4px',
    flex: 1,
    overflowY: 'auto',
  },
  navLink: {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    padding: '10px 14px',
    borderRadius: 'var(--radius-sm)',
    fontSize: '0.875rem',
    fontWeight: '500',
    color: 'var(--text-muted)',
    transition: 'all 0.15s ease',
  },
  navLinkActive: {
    backgroundColor: 'var(--bg-card)',
    color: 'var(--primary)',
    fontWeight: '700',
    border: '1px solid var(--border-strong)',
    boxShadow: 'var(--shadow-subtle)',
  },
  navLinkHighlight: {
    color: 'var(--primary)',
    fontWeight: '600',
  },
  highlightBadge: {
    display: 'inline-flex',
    alignItems: 'center',
    padding: '2px 8px',
    backgroundColor: 'var(--highlight-light)',
    color: 'var(--highlight)',
    fontSize: '0.6875rem',
    fontWeight: '700',
    borderRadius: 'var(--radius-full)',
  },
  footer: {
    paddingTop: 'var(--space-md)',
    borderTop: '1px solid var(--border-subtle)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  userInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    overflow: 'hidden',
  },
  avatar: {
    width: '34px',
    height: '34px',
    borderRadius: 'var(--radius-full)',
    backgroundColor: 'var(--primary)',
    color: 'var(--text-inverse)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: '0.875rem',
    fontWeight: '700',
    flexShrink: 0,
  },
  userMeta: {
    overflow: 'hidden',
  },
  userName: {
    fontSize: '0.8125rem',
    fontWeight: '600',
    color: 'var(--text-main)',
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  userRole: {
    fontSize: '0.6875rem',
    color: 'var(--text-muted)',
    fontWeight: '600',
  },
  logoutBtn: {
    background: 'none',
    border: 'none',
    padding: '8px',
    color: 'var(--text-muted)',
    borderRadius: 'var(--radius-sm)',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'color 0.15s ease, background 0.15s ease',
  },
};

export default Sidebar;
