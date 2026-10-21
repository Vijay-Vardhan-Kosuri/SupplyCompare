import React from 'react';
import { PackageOpen } from 'lucide-react';

const EmptyState = ({ title, message, icon: Icon = PackageOpen, actionText, onAction }) => {
  return (
    <div style={styles.container}>
      <div style={styles.iconBox}>
        <Icon size={28} color="var(--primary)" strokeWidth={1.8} />
      </div>
      <h3 style={styles.title}>{title}</h3>
      <p style={styles.message}>{message}</p>
      {actionText && onAction && (
        <button onClick={onAction} className="btn btn-primary" style={styles.btn}>
          {actionText}
        </button>
      )}
    </div>
  );
};

const styles = {
  container: {
    padding: '48px 24px',
    textAlign: 'center',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'var(--bg-card)',
    borderRadius: 'var(--radius-md)',
    border: '1px dashed var(--border-strong)',
  },
  iconBox: {
    width: '56px',
    height: '56px',
    borderRadius: 'var(--radius-full)',
    backgroundColor: 'var(--primary-light)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: '16px',
  },
  title: {
    fontSize: '1.125rem',
    fontWeight: '700',
    color: 'var(--text-main)',
    marginBottom: '6px',
  },
  message: {
    fontSize: '0.875rem',
    color: 'var(--text-muted)',
    maxWidth: '420px',
    lineHeight: 1.5,
    marginBottom: '18px',
  },
  btn: {
    marginTop: '4px',
  }
};

export default EmptyState;
