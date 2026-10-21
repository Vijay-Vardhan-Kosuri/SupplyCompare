import React from 'react';

const PageHeader = ({ title, subtitle, breadcrumb, actions }) => {
  return (
    <div style={styles.container}>
      <div style={styles.textBlock}>
        {breadcrumb && <div style={styles.breadcrumb}>{breadcrumb}</div>}
        <h1 style={styles.title}>{title}</h1>
        {subtitle && <p style={styles.subtitle}>{subtitle}</p>}
      </div>
      {actions && <div style={styles.actions}>{actions}</div>}
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 'var(--space-xl)',
    flexWrap: 'wrap',
    gap: 'var(--space-md)',
  },
  textBlock: {
    maxWidth: '700px',
  },
  breadcrumb: {
    fontSize: '0.75rem',
    color: 'var(--text-light)',
    marginBottom: '4px',
    fontWeight: '500',
    textTransform: 'uppercase',
    letterSpacing: '0.04em',
  },
  title: {
    fontSize: '1.75rem',
    fontWeight: '800',
    color: 'var(--text-main)',
    letterSpacing: '-0.025em',
    marginBottom: '4px',
  },
  subtitle: {
    fontSize: '0.9375rem',
    color: 'var(--text-muted)',
    lineHeight: 1.45,
  },
  actions: {
    display: 'flex',
    alignItems: 'center',
    gap: 'var(--space-sm)',
    flexWrap: 'wrap',
  },
};

export default PageHeader;
