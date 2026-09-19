import React from 'react';
import { auth } from '../api';

export default function TeamCard({ team, onApply, userRequestStatus }) {
  const user = auth.getUser();
  const currentMemberCount = team.currentMembers ? team.currentMembers.length : 0;
  const isOwner = user && user.id === team.createdBy;
  const isMember = team.currentMembers?.some(m => m.userId === user?.id);
  const isOpen = team.status === 'OPEN';
  const spotsLeft = Math.max(0, team.teamSize - currentMemberCount);

  return (
    <div className="paper-card rounded-xl p-6 flex flex-col justify-between h-full">
      <div>
        {/* Top meta row */}
        <div className="flex items-start justify-between gap-3 mb-3">
          <span className="badge-tag uppercase px-2.5 py-1 rounded-md bg-ochre-light text-ochre border border-ochre-border font-bold">
            {team.hackathonName}
          </span>

          <span
            className={`badge-tag uppercase px-2.5 py-1 rounded-md font-bold ${
              isOpen && spotsLeft > 0
                ? 'bg-sage-light text-sage border border-sage-border'
                : 'bg-canvas-alt text-ink-muted border border-canvas-border'
            }`}
          >
            {spotsLeft === 0 ? 'TEAM FULL' : team.status}
          </span>
        </div>

        {/* Team Title */}
        <h3 className="font-heading font-bold text-ink text-lg sm:text-xl leading-snug mb-1.5">
          {team.title}
        </h3>
        
        {/* Creator byline */}
        <p className="text-xs text-ink-muted mb-4 font-medium">
          Led by <span className="font-semibold text-ink">{team.creatorName || 'Student'}</span> • Posted {new Date(team.createdAt).toLocaleDateString()}
        </p>

        {/* Description */}
        <p className="text-sm text-ink-secondary leading-relaxed mb-5 line-clamp-3">
          {team.description}
        </p>

        {/* Skills Needed */}
        <div className="mb-5">
          <div className="text-xs uppercase tracking-wider text-ink-muted mb-2 font-bold font-mono">
            Required Skills
          </div>
          <div className="flex flex-wrap gap-2">
            {team.skillsNeeded && team.skillsNeeded.length > 0 ? (
              team.skillsNeeded.map((skill, idx) => (
                <span
                  key={idx}
                  className="text-xs font-semibold px-2.5 py-1 rounded-md bg-terracotta-light text-terracotta border border-terracotta-border"
                >
                  {skill}
                </span>
              ))
            ) : (
              <span className="text-xs text-ink-muted italic">Open to all tech stacks</span>
            )}
          </div>
        </div>

        {/* Current Roster */}
        <div className="mb-5 pt-4 border-t border-canvas-border/80">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="text-ink-muted font-bold uppercase tracking-wider font-mono">
              Team Roster
            </span>
            <span className="font-semibold text-ink">
              {currentMemberCount} of {team.teamSize} spots filled
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            {team.currentMembers?.map((m, idx) => (
              <span
                key={idx}
                className="text-xs px-2.5 py-1 rounded-md bg-canvas-alt text-ink border border-canvas-border font-medium flex items-center gap-1.5"
              >
                <span className="w-1.5 h-1.5 rounded-full bg-terracotta"></span>
                {m.name}
                <span className="text-ink-muted text-[11px]">({m.role || 'Member'})</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Card Action Area */}
      <div className="pt-4 border-t border-canvas-border flex items-center justify-between gap-3">
        <span className="text-xs font-semibold text-ink-muted">
          {spotsLeft > 0 ? `${spotsLeft} spot${spotsLeft !== 1 ? 's' : ''} available` : 'Roster complete'}
        </span>

        {/* Dynamic Contextual Button */}
        <div>
          {!user ? (
            <a
              href="/login.html"
              className="text-xs sm:text-sm font-semibold px-4 py-2 rounded-lg border border-canvas-border text-ink bg-canvas-card hover:border-terracotta hover:text-terracotta transition-colors inline-block"
            >
              Sign In to Apply
            </a>
          ) : isOwner ? (
            <a
              href="/dashboard.html"
              className="text-xs sm:text-sm font-semibold px-4 py-2 rounded-lg bg-canvas-alt text-ink-secondary hover:bg-canvas-border transition-colors inline-block"
            >
              Your Team (Manage) →
            </a>
          ) : isMember ? (
            <span className="text-xs font-bold px-3 py-1.5 rounded-md bg-sage-light text-sage border border-sage-border inline-block">
              ✓ Joined Member
            </span>
          ) : userRequestStatus === 'PENDING' ? (
            <span className="text-xs font-bold px-3 py-1.5 rounded-md bg-ochre-light text-ochre border border-ochre-border inline-flex items-center gap-1.5" title="Request has been sent to team leader for manual review">
              <span>⏳</span> Application Under Review
            </span>
          ) : userRequestStatus === 'REJECTED' ? (
            <span className="text-xs font-semibold px-3 py-1.5 rounded-md bg-canvas-alt text-ink-muted border border-canvas-border inline-block">
              Application Declined
            </span>
          ) : spotsLeft === 0 || !isOpen ? (
            <span className="text-xs font-semibold px-3 py-1.5 rounded-md bg-canvas-alt text-ink-muted border border-canvas-border inline-block">
              Team Full
            </span>
          ) : (
            <button
              onClick={() => onApply(team)}
              className="text-xs sm:text-sm font-semibold px-4 py-2 rounded-lg bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-xs"
            >
              Apply to Join Team
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
