import React, { useState } from 'react';
import { api } from '../api';

export default function ApplyModal({ team, onClose, onSuccess }) {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await api.sendRequest(team.id, message);
      onSuccess(`Your application for "${team.title}" has been sent! The team leader will review your pitch in their dashboard.`);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to submit application');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/50 backdrop-blur-xs">
      <div className="bg-canvas-card border border-canvas-border rounded-xl max-w-lg w-full p-6 sm:p-8 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150">
        
        <div className="flex items-start justify-between mb-5">
          <div>
            <span className="badge-tag uppercase font-bold px-2.5 py-1 rounded-md bg-ochre-light text-ochre border border-ochre-border text-xs">
              {team.hackathonName}
            </span>
            <h2 className="font-heading font-extrabold text-ink text-xl sm:text-2xl mt-2 leading-snug">
              Apply to join: {team.title}
            </h2>
            <p className="text-xs text-ink-muted mt-1 font-medium">
              Team Leader: <strong className="text-ink">{team.creatorName}</strong>
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-ink-muted hover:text-ink text-2xl leading-none p-1 font-bold"
          >
            ×
          </button>
        </div>

        {error && (
          <div className="mb-5 p-4 rounded-lg bg-terracotta-light border border-terracotta-border text-terracotta text-sm font-semibold">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="p-3.5 rounded-lg bg-canvas-alt border border-canvas-border text-xs text-ink-secondary leading-relaxed">
            💡 <strong>How it works:</strong> Your pitch, department details, and technical skills will be sent to the team leader. They will evaluate your profile and make an accept or decline decision from their dashboard.
          </div>

          <div>
            <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-2 font-mono">
              Your Pitch & Background *
            </label>
            <textarea
              required
              rows={4}
              placeholder="Introduce yourself, what role you'd like to own (frontend, backend, ML, pitch), your relevant project experience, and links to your GitHub or portfolio..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full text-sm p-3.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta transition-colors text-ink leading-relaxed"
            />
          </div>

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-canvas-border">
            <button
              type="button"
              onClick={onClose}
              className="px-5 py-2.5 text-sm font-bold text-ink-secondary hover:text-ink transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2.5 rounded-lg text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-sm disabled:opacity-50"
            >
              {loading ? 'Submitting Application...' : 'Send Join Request'}
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}
