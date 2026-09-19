import React, { useState } from 'react';
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
      setError(err.message || 'Failed to create team post');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/50 backdrop-blur-xs">
      <div className="bg-canvas-card border border-canvas-border rounded-xl max-w-xl w-full p-6 sm:p-8 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150">
        
        <div className="flex items-start justify-between mb-5">
          <div>
            <h2 className="font-heading font-extrabold text-ink text-2xl">
              Post a New Hackathon Team
            </h2>
            <p className="text-sm text-ink-muted mt-1 font-medium">
              Publish your project problem statement, needed technical skills, and target team size.
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
          <div>
            <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
              Hackathon Event Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Smart India Hackathon 2026, ETHIndia..."
              value={formData.hackathonName}
              onChange={(e) => setFormData({ ...formData, hackathonName: e.target.value })}
              className="w-full text-sm px-4 py-2.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta text-ink"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
              Project Title / Idea Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. Campus Food Rescue, Decentralized Research Identity"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full text-sm px-4 py-2.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta text-ink"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
              Project Vision & Problem Statement
            </label>
            <textarea
              rows={3}
              placeholder="Explain the problem you're tackling, what the solution will look like, and the tech stack you want to use..."
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full text-sm p-3.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta text-ink leading-relaxed"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
                Skills Needed (comma-separated)
              </label>
              <input
                type="text"
                placeholder="React, Python, OpenCV, Figma"
                value={formData.skillsNeeded}
                onChange={(e) => setFormData({ ...formData, skillsNeeded: e.target.value })}
                className="w-full text-sm px-4 py-2.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta text-ink"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
                Target Team Capacity
              </label>
              <select
                value={formData.teamSize}
                onChange={(e) => setFormData({ ...formData, teamSize: e.target.value })}
                className="w-full text-sm px-4 py-2.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta text-ink"
              >
                <option value="2">2 Members</option>
                <option value="3">3 Members</option>
                <option value="4">4 Members (Standard)</option>
                <option value="5">5 Members</option>
                <option value="6">6 Members (SIH Standard)</option>
              </select>
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-4 border-t border-canvas-border">
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
              {loading ? 'Publishing...' : 'Publish Team Requirement'}
            </button>
          </div>
        </form>

      </div>
    </div>
  );
}
