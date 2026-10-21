import React from 'react';
import { AlertTriangle, X } from 'lucide-react';

const ConfirmationDialog = ({ isOpen, title, message, confirmText = 'Confirm', onConfirm, onCancel, isDanger = false }) => {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content" style={{ maxWidth: '440px' }}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              backgroundColor: isDanger ? 'var(--status-error-bg)' : 'var(--primary-light)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: isDanger ? 'var(--status-error)' : 'var(--primary)'
            }}>
              <AlertTriangle size={18} />
            </div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: '700' }}>{title}</h3>
          </div>
          <button onClick={onCancel} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-muted)' }}>
            <X size={18} />
          </button>
        </div>
        <div className="modal-body">
          <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
            {message}
          </p>
        </div>
        <div className="modal-footer">
          <button onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className={`btn ${isDanger ? 'btn-highlight' : 'btn-primary'}`}
          >
            {confirmText}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmationDialog;
