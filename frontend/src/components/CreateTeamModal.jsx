import React, { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { api } from '../api';

export default function CreateTeamModal({ onClose, onSuccess }) {
  const [formData, setFormData] = useState({
    hackathonName: '',
    title: '',
    description: '',
    skillsNeeded: '',
    teamSize: 4
  });
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

    const skillsArray = formData.skillsNeeded
      .split(',')
      .map(s => s.trim())
      .filter(s => s.length > 0);

    try {
      const payload = {
        hackathonName: formData.hackathonName.trim(),
        title: formData.title.trim(),
        description: formData.description.trim(),
        skillsNeeded: skillsArray,
        teamSize: parseInt(formData.teamSize, 10) || 4
      };

      const newTeam = await api.createTeam(payload);
      onSuccess(newTeam);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to create squad');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/40 backdrop-blur-xs">
      <div ref={modalRef} className="paper-card rounded-2xl max-w-lg w-full p-6 sm:p-7 shadow-2xl relative border border-canvas-border">
        
        <div className="flex items-center justify-between mb-4 pb-3 border-b border-canvas-border">
          <div>
            <h2 className="font-heading font-black text-ink text-xl">
              Post Squad Requirement
            </h2>
            <p className="text-xs text-ink-muted mt-0.5">
              Specify your hackathon, tech stack, and squad capacity.
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
            <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
              Hackathon Event *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Smart India Hackathon 2026, ETHIndia..."
              value={formData.hackathonName}
              onChange={(e) => setFormData({ ...formData, hackathonName: e.target.value })}
              className="w-full text-sm px-3.5 py-2 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta text-ink"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
              Project Title / Idea Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Campus Food Rescue, Decentralized Identity"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full text-sm px-3.5 py-2 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta text-ink"
            />
          </div>

          <div>
            <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
              Project Summary
            </label>
            <textarea
              rows={3}
              placeholder="Briefly describe what you're building and the problem it solves..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full text-sm p-3 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta text-ink leading-relaxed"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
                Needed Skills (comma-separated)
              </label>
              <input
                type="text"
                placeholder="React, Python, OpenCV"
                value={formData.skillsNeeded}
                onChange={(e) => setFormData({ ...formData, skillsNeeded: e.target.value })}
                className="w-full text-sm px-3.5 py-2 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta text-ink"
              />
            </div>

            <div>
              <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
                Squad Capacity
              </label>
              <select
                value={formData.teamSize}
                onChange={(e) => setFormData({ ...formData, teamSize: e.target.value })}
                className="w-full text-sm px-3 py-2 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta text-ink"
              >
                <option value="2">2 Members</option>
                <option value="3">3 Members</option>
                <option value="4">4 Members (Standard)</option>
                <option value="5">5 Members</option>
                <option value="6">6 Members (SIH)</option>
              </select>
            </div>
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
              {loading ? 'Posting...' : 'Publish Squad'}
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}
