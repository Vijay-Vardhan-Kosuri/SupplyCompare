import React from 'react';
import { CheckCircle, AlertTriangle, Clock, XCircle, Truck, PackageCheck, Sparkles } from 'lucide-react';

const StatusBadge = ({ status }) => {
  if (!status) return null;
  const s = status.toLowerCase();

  const configs = {
    // PO States
    draft: { label: 'Draft', bg: 'var(--bg-card-subtle)', color: 'var(--text-muted)', icon: Clock },
    submitted: { label: 'Submitted', bg: 'var(--status-info-bg)', color: 'var(--status-info)', icon: Clock },
    confirmed: { label: 'Confirmed', bg: 'var(--primary-light)', color: 'var(--primary)', icon: CheckCircle },
    shipped: { label: 'In Transit', bg: 'var(--status-warning-bg)', color: 'var(--status-warning)', icon: Truck },
    received: { label: 'Received & Stocked', bg: 'var(--status-success-bg)', color: 'var(--status-success)', icon: PackageCheck },
    cancelled: { label: 'Cancelled', bg: 'var(--status-error-bg)', color: 'var(--status-error)', icon: XCircle },

    // Supplier / Quote States
    active: { label: 'Active', bg: 'var(--status-success-bg)', color: 'var(--status-success)', icon: CheckCircle },
    expired: { label: 'Expired', bg: 'var(--status-error-bg)', color: 'var(--status-error)', icon: AlertTriangle },
    inactive: { label: 'Inactive', bg: 'var(--bg-card-subtle)', color: 'var(--text-muted)', icon: XCircle },
    archived: { label: 'Archived', bg: 'var(--bg-card-subtle)', color: 'var(--text-light)', icon: XCircle },

    // Comparison Eligibility
    eligible: { label: 'Eligible', bg: 'var(--status-success-bg)', color: 'var(--status-success)', icon: CheckCircle },
    ineligible: { label: 'Ineligible', bg: 'var(--status-error-bg)', color: 'var(--status-error)', icon: XCircle },
    best_deal: { label: 'Best Total Cost', bg: 'var(--highlight-light)', color: 'var(--highlight)', icon: Sparkles },
  };

  const config = configs[s] || { label: status, bg: 'var(--bg-card-subtle)', color: 'var(--text-main)', icon: null };
  const Icon = config.icon;

  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: '5px',
      padding: '4px 10px',
      borderRadius: 'var(--radius-full)',
      fontSize: '0.75rem',
      fontWeight: '600',
      backgroundColor: config.bg,
      color: config.color,
      letterSpacing: '0.01em',
    }}>
      {Icon && <Icon size={12} strokeWidth={2.2} />}
      {config.label}
    </span>
  );
};

export default StatusBadge;
