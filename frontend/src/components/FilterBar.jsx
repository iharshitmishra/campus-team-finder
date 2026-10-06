import React from 'react';
import { gsap } from 'gsap';

const POPULAR_SKILLS = [
  'React', 'Python', 'Solidity', 'Java', 'FastAPI', 'Node.js', 
  'TensorFlow', 'UI/UX', 'PostgreSQL', 'Docker'
];

export default function FilterBar({ filters, onFilterChange, onReset }) {
  const handleSkillToggle = (e, skill) => {
    if (typeof gsap !== 'undefined') {
      gsap.fromTo(e.currentTarget, { scale: 0.92 }, { scale: 1, duration: 0.25, ease: 'back.out(2)' });
    }
    onFilterChange({
      ...filters,
      skill: filters.skill === skill ? '' : skill
    });
  };

  const hasActiveFilters = !!(filters.skill || filters.hackathon || filters.status || filters.search);

  return (
    <div className="paper-card rounded-2xl p-5 sm:p-6 mb-8 border border-canvas-border">
      
      {/* Search and Filters grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5 mb-4">
        <div>
          <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
            Search Keyword
          </label>
          <div className="relative">
            <input
              type="text"
              placeholder="e.g. AI, web3, healthcare..."
              value={filters.search || ''}
              onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
              className="w-full text-sm pl-9 pr-3.5 py-2.5 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta transition-colors text-ink placeholder:text-ink-subtle"
            />
            <svg className="w-4 h-4 text-ink-muted absolute left-3 top-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>
        </div>

        <div>
          <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
            Hackathon Event
          </label>
          <input
            type="text"
            placeholder="e.g. SIH, ETHIndia..."
            value={filters.hackathon || ''}
            onChange={(e) => onFilterChange({ ...filters, hackathon: e.target.value })}
            className="w-full text-sm px-3.5 py-2.5 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta transition-colors text-ink placeholder:text-ink-subtle"
          />
        </div>

        <div>
          <label className="block text-[11px] font-bold text-ink-muted uppercase tracking-wider mb-1 font-mono">
            Squad Status
          </label>
          <select
            value={filters.status || ''}
            onChange={(e) => onFilterChange({ ...filters, status: e.target.value })}
            className="w-full text-sm px-3.5 py-2.5 border border-canvas-border rounded-lg bg-white focus:outline-none focus:border-terracotta transition-colors text-ink"
          >
            <option value="">All Squads</option>
            <option value="OPEN">Open (Recruiting)</option>
            <option value="FULL">Full Squads</option>
          </select>
        </div>
      </div>

      {/* Quick Skill Buttons */}
      <div className="flex flex-wrap items-center gap-1.5 pt-3.5 border-t border-canvas-border">
        <span className="text-[11px] font-bold font-mono text-ink-muted uppercase tracking-wider mr-1">
          Stack:
        </span>
        {POPULAR_SKILLS.map((skill) => {
          const isSelected = filters.skill === skill;
          return (
            <button
              key={skill}
              type="button"
              onClick={(e) => handleSkillToggle(e, skill)}
              className={`text-xs font-semibold px-2.5 py-1 rounded-md transition-all cursor-pointer ${
                isSelected
                  ? 'bg-terracotta text-white shadow-xs'
                  : 'bg-canvas-alt text-ink-secondary hover:bg-canvas-border/70 border border-canvas-border/80'
              }`}
            >
              {skill}
            </button>
          );
        })}

        {hasActiveFilters && (
          <button
            type="button"
            onClick={onReset}
            className="ml-auto text-xs font-bold text-terracotta hover:underline cursor-pointer py-1"
          >
            Reset Filters ×
          </button>
        )}
      </div>

    </div>
  );
}
