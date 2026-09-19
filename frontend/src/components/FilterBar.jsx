import React from 'react';

const POPULAR_SKILLS = [
  'React', 'Python', 'Solidity', 'Java', 'FastAPI', 'Node.js', 
  'TensorFlow', 'UI/UX Design', 'PostgreSQL', 'Docker'
];

export default function FilterBar({ filters, onFilterChange, onReset }) {
  const handleSkillToggle = (skill) => {
    onFilterChange({
      ...filters,
      skill: filters.skill === skill ? '' : skill
    });
  };

  const hasActiveFilters = !!(filters.skill || filters.hackathon || filters.status || filters.search);

  return (
    <div className="bg-canvas-card border border-canvas-border rounded-xl p-5 sm:p-6 mb-8 shadow-xs">
      
      {/* Search and Filters grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-5">
        <div>
          <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
            Search Project or Problem
          </label>
          <input
            type="text"
            placeholder="Search keywords, e.g. drone, transit, AI..."
            value={filters.search || ''}
            onChange={(e) => onFilterChange({ ...filters, search: e.target.value })}
            className="w-full text-sm px-3.5 py-2.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta transition-colors text-ink placeholder:text-ink-subtle"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
            Hackathon Competition
          </label>
          <input
            type="text"
            placeholder="e.g. Smart India Hackathon, ETHIndia..."
            value={filters.hackathon || ''}
            onChange={(e) => onFilterChange({ ...filters, hackathon: e.target.value })}
            className="w-full text-sm px-3.5 py-2.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta transition-colors text-ink placeholder:text-ink-subtle"
          />
        </div>

        <div>
          <label className="block text-xs font-bold text-ink-muted uppercase tracking-wider mb-1.5 font-mono">
            Recruitment Status
          </label>
          <select
            value={filters.status || ''}
            onChange={(e) => onFilterChange({ ...filters, status: e.target.value })}
            className="w-full text-sm px-3.5 py-2.5 border border-canvas-border rounded-lg bg-canvas focus:outline-none focus:border-terracotta transition-colors text-ink"
          >
            <option value="">All Teams (Open & Full)</option>
            <option value="OPEN">Open (Actively Recruiting)</option>
            <option value="FULL">Full Teams</option>
          </select>
        </div>
      </div>

      {/* Quick Skill Buttons */}
      <div className="flex flex-wrap items-center gap-2 pt-4 border-t border-canvas-border/80">
        <span className="text-xs font-bold font-mono text-ink-muted uppercase tracking-wider mr-1">
          Skill Filter:
        </span>
        {POPULAR_SKILLS.map((skill) => {
          const isSelected = filters.skill === skill;
          return (
            <button
              key={skill}
              type="button"
              onClick={() => handleSkillToggle(skill)}
              className={`text-xs font-semibold px-3 py-1.5 rounded-lg transition-all ${
                isSelected
                  ? 'bg-terracotta text-white shadow-xs'
                  : 'bg-canvas-alt text-ink-secondary hover:bg-canvas-border border border-canvas-border/60'
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
            className="ml-auto text-xs font-bold text-terracotta hover:text-terracotta-hover underline decoration-2 cursor-pointer"
          >
            Clear All Filters
          </button>
        )}
      </div>

    </div>
  );
}
