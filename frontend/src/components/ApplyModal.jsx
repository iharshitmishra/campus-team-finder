import React, { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { api } from '../api';

export default function ApplyModal({ team, onClose, onSuccess }) {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const modalRef = useRef(null);

  useEffect(() => {
    if (modalRef.current) {
      gsap.fromTo(
        modalRef.current,
        { opacity: 0, scale: 0.94, y: 15 },
        { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: 'back.out(1.5)' }
      );
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await api.sendRequest(team.id, message);
      onSuccess(`Your application for "${team.title}" was submitted! The team lead will review it.`);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to submit application');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/40 backdrop-blur-xs">
      <div ref={modalRef} className="paper-card rounded-2xl max-w-md w-full p-6 sm:p-7 shadow-2xl relative border border-canvas-border">
        
        <div className="flex items-start justify-between mb-4 pb-3 border-b border-canvas-border">
          <div>
            <span className="badge-tag uppercase font-bold px-2 py-0.5 rounded bg-ochre-light text-ochre border border-ochre-border text-[11px]">
              {team.hackathonName}
            </span>
            <h2 className="font-heading font-black text-ink text-xl mt-1.5 leading-snug">
              Apply to {team.title}
            </h2>
            <p className="text-xs text-ink-muted mt-0.5">
              Lead: <strong className="text-ink">{team.creatorName}</strong>
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-ink-muted hover:text-ink text-xl leading-none p-1 font-bold cursor-pointer"
          >
            ×
          </button>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-terracotta-light border border-terracotta-border text-terracotta text-xs font-semibold">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div>
            <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
              Your Pitch & Background *
            </label>
            <textarea
              required
              rows={4}
              placeholder="Introduce yourself, your primary skills (e.g. React, ML, UI), GitHub link, and what you'd like to contribute..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              className="w-full text-sm p-3 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta transition-colors text-ink leading-relaxed"
            />
          </div>

          <div className="flex items-center justify-end gap-2.5 pt-3 border-t border-canvas-border">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs sm:text-sm font-semibold text-ink-secondary hover:text-ink cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="interactive-btn px-5 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-xs disabled:opacity-50 cursor-pointer"
            >
              {loading ? 'Sending...' : 'Send Pitch'}
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}
