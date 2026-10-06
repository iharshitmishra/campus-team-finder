import React from 'react';
import { auth } from '../api';

export default function TeamCard({ team, onApply, userRequestStatus }) {
  const user = auth.getUser();
  const currentMemberCount = team.currentMembers ? team.currentMembers.length : 0;
  const isOwner = user && user.id === team.createdBy;
  const isMember = team.currentMembers?.some(m => m.userId === user?.id);
  const isOpen = team.status === 'OPEN';
  const spotsLeft = Math.max(0, team.teamSize - currentMemberCount);

  // Calculate percentage of roster filled
  const fillPercentage = Math.min(100, Math.round((currentMemberCount / (team.teamSize || 4)) * 100));

  return (
    <div className="team-card paper-card rounded-2xl p-5 sm:p-6 flex flex-col justify-between h-full border border-canvas-border">
      <div>
        {/* Top meta row */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className="badge-tag uppercase px-2.5 py-0.5 rounded-md bg-ochre-light text-ochre border border-ochre-border font-bold text-xs truncate max-w-[180px]">
            {team.hackathonName}
          </span>

          <span
            className={`badge-tag uppercase px-2 py-0.5 rounded-md font-bold text-xs shrink-0 ${
              isOpen && spotsLeft > 0
                ? 'bg-sage-light text-sage border border-sage-border'
                : 'bg-canvas-alt text-ink-muted border border-canvas-border'
            }`}
          >
            {spotsLeft === 0 ? 'FULL' : team.status}
          </span>
        </div>

        {/* Team Title */}
        <h3 className="font-heading font-extrabold text-ink text-lg sm:text-xl leading-snug mb-1">
          {team.title}
        </h3>
        
        {/* Creator byline */}
        <p className="text-xs text-ink-muted mb-3.5 font-medium">
          Lead: <span className="font-semibold text-ink">{team.creatorName || 'Student'}</span> • {new Date(team.createdAt).toLocaleDateString()}
        </p>

        {/* Description */}
        <p className="text-xs sm:text-sm text-ink-secondary leading-relaxed mb-4 line-clamp-3">
          {team.description || 'No description provided.'}
        </p>

        {/* Skills Needed */}
        <div className="mb-4">
          <div className="text-[11px] uppercase tracking-wider text-ink-muted mb-1.5 font-bold font-mono">
            Needed Skills
          </div>
          <div className="flex flex-wrap gap-1.5">
            {team.skillsNeeded && team.skillsNeeded.length > 0 ? (
              team.skillsNeeded.map((skill, idx) => (
                <span
                  key={idx}
                  className="text-xs font-semibold px-2.5 py-0.5 rounded-md bg-terracotta-light text-terracotta border border-terracotta-border"
                >
                  {skill}
                </span>
              ))
            ) : (
              <span className="text-xs text-ink-muted italic">Any technical skills</span>
            )}
          </div>
        </div>

        {/* Current Roster & Visual Progress Bar */}
        <div className="mb-4 pt-3.5 border-t border-canvas-border">
          <div className="flex items-center justify-between text-xs mb-1.5 font-mono">
            <span className="text-ink-muted font-bold uppercase tracking-wider">
              Squad Roster
            </span>
            <span className="font-bold text-ink">
              {currentMemberCount}/{team.teamSize} Filled
            </span>
          </div>

          {/* Mini progress bar */}
          <div className="w-full bg-canvas-alt h-1.5 rounded-full overflow-hidden mb-2.5 border border-canvas-border/50">
            <div
              className={`h-full transition-all duration-500 rounded-full ${
                spotsLeft === 0 ? 'bg-sage' : 'bg-terracotta'
              }`}
              style={{ width: `${fillPercentage}%` }}
            ></div>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {team.currentMembers?.map((m, idx) => (
              <span
                key={idx}
                className="text-xs px-2 py-0.5 rounded bg-canvas-alt text-ink border border-canvas-border font-medium flex items-center gap-1.5"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-terracotta"></span>
                <span className="truncate max-w-[120px]">{m.name}</span>
                <span className="text-ink-muted text-[10px]">({m.role || 'Member'})</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Card Action Area */}
      <div className="pt-3.5 border-t border-canvas-border flex items-center justify-between gap-2">
        <span className="text-xs font-semibold text-ink-muted">
          {spotsLeft > 0 ? `${spotsLeft} spot${spotsLeft !== 1 ? 's' : ''} left` : 'Squad full'}
        </span>

        {/* Dynamic Action */}
        <div>
          {!user ? (
            <a
              href="/login.html"
              className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-canvas-border text-ink bg-white hover:border-terracotta hover:text-terracotta transition-colors inline-block shadow-xs"
            >
              Sign In to Apply
            </a>
          ) : isOwner ? (
            <a
              href="/dashboard.html"
              className="text-xs font-bold px-3 py-1.5 rounded-lg bg-canvas-alt text-ink-secondary hover:text-ink hover:bg-canvas-border/70 transition-colors inline-block border border-canvas-border"
            >
              Manage Squad →
            </a>
          ) : isMember ? (
            <span className="text-xs font-bold px-2.5 py-1 rounded bg-sage-light text-sage border border-sage-border inline-block">
              ✓ In Squad
            </span>
          ) : userRequestStatus === 'PENDING' ? (
            <span className="text-xs font-bold px-2.5 py-1 rounded bg-ochre-light text-ochre border border-ochre-border inline-flex items-center gap-1">
              ⏳ Under Review
            </span>
          ) : userRequestStatus === 'REJECTED' ? (
            <span className="text-xs font-semibold px-2.5 py-1 rounded bg-canvas-alt text-ink-muted border border-canvas-border inline-block">
              Declined
            </span>
          ) : spotsLeft === 0 || !isOpen ? (
            <span className="text-xs font-semibold px-2.5 py-1 rounded bg-canvas-alt text-ink-muted border border-canvas-border inline-block">
              Squad Full
            </span>
          ) : (
            <button
              onClick={() => onApply(team)}
              className="interactive-btn text-xs font-bold px-3.5 py-1.5 rounded-lg bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-xs cursor-pointer"
            >
              Apply to Squad
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
