import React, { useState } from 'react';
import { auth } from '../api';

export default function Navbar({ onOpenCreateModal }) {
  const user = auth.getUser();
  const loggedIn = auth.isLoggedIn();
  const [showHowItWorksModal, setShowHowItWorksModal] = useState(false);

  const handleLogout = () => {
    auth.clearAuth();
    window.location.href = '/login.html';
  };

  const displayName = user?.name ? user.name.split(' ')[0] : 'Student';

  return (
    <>
      <header className="border-b border-canvas-border bg-canvas/95 backdrop-blur-md sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-3">
          
          {/* Brand - Left */}
          <a href="/index.html" className="flex items-center gap-2.5 shrink-0 group">
            <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-terracotta text-white flex items-center justify-center font-heading font-black text-lg sm:text-xl shadow-xs">
              H
            </div>
            <div className="flex flex-col">
              <span className="font-heading font-extrabold text-ink text-base sm:text-lg leading-tight tracking-tight group-hover:text-terracotta transition-colors">
                Campus Team Finder
              </span>
              <span className="text-[10px] uppercase tracking-wider text-ink-muted font-semibold">
                Hackathon Squads
              </span>
            </div>
          </a>

          {/* Navigation Links - Center */}
          <nav className="hidden md:flex items-center gap-4 lg:gap-6 text-xs sm:text-sm font-semibold text-ink-secondary">
            <a href="/browse-teams.html" className="hover:text-terracotta transition-colors whitespace-nowrap">
              Browse Teams
            </a>
            {loggedIn && (
              <a href="/dashboard.html" className="hover:text-terracotta transition-colors whitespace-nowrap">
                My Dashboard
              </a>
            )}
            <button
              type="button"
              onClick={() => setShowHowItWorksModal(true)}
              className="hover:text-terracotta transition-colors whitespace-nowrap cursor-pointer text-xs sm:text-sm font-semibold text-ink-secondary"
            >
              How It Works
            </button>
            <a href="/index.html#hackathons" className="hover:text-terracotta transition-colors whitespace-nowrap">
              Hackathons
            </a>
          </nav>

          {/* Actions & User State - Right */}
          <div className="flex items-center gap-2 sm:gap-3 shrink-0">
            {loggedIn ? (
              <>
                {onOpenCreateModal && (
                  <button
                    onClick={onOpenCreateModal}
                    className="px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-xs whitespace-nowrap cursor-pointer"
                  >
                    + Post Team
                  </button>
                )}

                {/* Compact User Profile Pill */}
                <a
                  href="/dashboard.html"
                  className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-canvas-alt border border-canvas-border hover:border-terracotta transition-all"
                  title={`${user?.name} (${user?.email})`}
                >
                  <div className="w-6 h-6 rounded-full bg-ochre-light border border-ochre-border text-ochre font-extrabold text-xs flex items-center justify-center shrink-0">
                    {user?.name ? user.name[0].toUpperCase() : 'S'}
                  </div>
                  <span className="text-xs font-bold text-ink max-w-[90px] sm:max-w-[120px] truncate">
                    {displayName}
                  </span>
                </a>

                <button
                  onClick={handleLogout}
                  className="px-2.5 py-1.5 text-xs font-semibold text-ink-muted hover:text-ink transition-colors whitespace-nowrap cursor-pointer"
                  title="Sign out of student account"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <a
                  href="/login.html"
                  className="px-3 py-1.5 text-xs sm:text-sm font-semibold text-ink-secondary hover:text-ink whitespace-nowrap"
                >
                  Sign In
                </a>
                <a
                  href="/login.html#register"
                  className="px-3.5 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-xs whitespace-nowrap"
                >
                  Join Campus
                </a>
              </>
            )}
          </div>

        </div>
      </header>

      {/* Interactive How It Works Modal (Does not navigate or disrupt session!) */}
      {showHowItWorksModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/50 backdrop-blur-xs">
          <div className="bg-canvas-card border border-canvas-border rounded-2xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl relative animate-in fade-in zoom-in-95 duration-150">
            
            <div className="flex items-start justify-between mb-6 pb-4 border-b border-canvas-border">
              <div>
                <span className="badge-tag uppercase font-bold text-xs text-terracotta bg-terracotta-light px-2.5 py-1 rounded-md border border-terracotta-border">
                  Workflow Guide
                </span>
                <h2 className="font-heading font-extrabold text-ink text-2xl mt-1.5">
                  How Campus Team Finder Works
                </h2>
              </div>
              <button
                onClick={() => setShowHowItWorksModal(false)}
                className="text-ink-muted hover:text-ink text-2xl font-bold p-1 leading-none cursor-pointer"
              >
                ×
              </button>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
              <div className="p-4 rounded-xl bg-canvas-alt border border-canvas-border">
                <div className="w-7 h-7 rounded-lg bg-terracotta text-white font-mono font-bold text-xs flex items-center justify-center mb-3">
                  01
                </div>
                <h3 className="font-heading font-bold text-ink text-sm mb-1">
                  Post or Browse
                </h3>
                <p className="text-xs text-ink-secondary leading-relaxed">
                  Leaders post team requirements with tech stack and capacity. Students filter by skills and competitions.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-canvas-alt border border-canvas-border">
                <div className="w-7 h-7 rounded-lg bg-terracotta text-white font-mono font-bold text-xs flex items-center justify-center mb-3">
                  02
                </div>
                <h3 className="font-heading font-bold text-ink text-sm mb-1">
                  Send Pitch
                </h3>
                <p className="text-xs text-ink-secondary leading-relaxed">
                  Submit a customized application with your GitHub, department background, and role interest.
                </p>
              </div>

              <div className="p-4 rounded-xl bg-canvas-alt border border-canvas-border">
                <div className="w-7 h-7 rounded-lg bg-terracotta text-white font-mono font-bold text-xs flex items-center justify-center mb-3">
                  03
                </div>
                <h3 className="font-heading font-bold text-ink text-sm mb-1">
                  Leader Decision
                </h3>
                <p className="text-xs text-ink-secondary leading-relaxed">
                  The team creator reviews your application in their dashboard and clicks Accept or Decline. No automatic approvals!
                </p>
              </div>
            </div>

            <div className="flex justify-end pt-2 border-t border-canvas-border">
              <button
                onClick={() => setShowHowItWorksModal(false)}
                className="px-5 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover cursor-pointer"
              >
                Got It
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
}
