import React from 'react';

const SummaryCard = ({ label, value, explanation, icon: Icon, badge, highlight }) => {
  return (
    <div style={{
      ...styles.card,
      ...(highlight ? styles.cardHighlight : {})
    }}>
      <div style={styles.topRow}>
        <span style={styles.label}>{label}</span>
        {Icon && (
          <div style={{
            ...styles.iconContainer,
            backgroundColor: highlight ? 'var(--highlight-light)' : 'var(--primary-light)',
            color: highlight ? 'var(--highlight)' : 'var(--primary)'
          }}>
            <Icon size={18} strokeWidth={2} />
          </div>
        )}
      </div>

      <div style={styles.valueRow}>
        <span style={styles.value}>{value}</span>
        {badge && <span style={styles.badge}>{badge}</span>}
      </div>

      {explanation && <p style={styles.explanation}>{explanation}</p>}
    </div>
  );
};

const styles = {
  card: {
    backgroundColor: 'var(--bg-card)',
    border: '1px solid var(--border-subtle)',
    borderRadius: 'var(--radius-md)',
    padding: 'var(--space-lg)',
    boxShadow: 'var(--shadow-subtle)',
    display: 'flex',
    flexDirection: 'column',
    transition: 'all 0.15s ease',
  },
  cardHighlight: {
    borderLeft: '4px solid var(--highlight)',
  },
  topRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 'var(--space-sm)',
  },
  label: {
    fontSize: '0.8125rem',
    fontWeight: '600',
    color: 'var(--text-muted)',
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
  },
  iconContainer: {
    width: '32px',
    height: '32px',
    borderRadius: 'var(--radius-sm)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  valueRow: {
    display: 'flex',
    alignItems: 'baseline',
    gap: '8px',
    marginBottom: '6px',
  },
  value: {
    fontSize: '1.75rem',
    fontWeight: '800',
    color: 'var(--text-main)',
    letterSpacing: '-0.03em',
  },
  badge: {
    fontSize: '0.75rem',
    fontWeight: '600',
    padding: '2px 8px',
    borderRadius: 'var(--radius-full)',
    backgroundColor: 'var(--primary-light)',
    color: 'var(--primary)',
  },
  explanation: {
    fontSize: '0.8125rem',
    color: 'var(--text-muted)',
    lineHeight: 1.4,
  },
};

export default SummaryCard;
