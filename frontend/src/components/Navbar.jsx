import React, { useState, useEffect, useRef } from 'react';
import { gsap } from 'gsap';
import { auth } from '../api';

export default function Navbar({ onOpenCreateModal }) {
  const user = auth.getUser();
  const loggedIn = auth.isLoggedIn();
  const [showHowItWorksModal, setShowHowItWorksModal] = useState(false);
  const modalRef = useRef(null);

  useEffect(() => {
    if (showHowItWorksModal && modalRef.current) {
      gsap.fromTo(
        modalRef.current,
        { opacity: 0, scale: 0.95, y: 15 },
        { opacity: 1, scale: 1, y: 0, duration: 0.3, ease: 'back.out(1.5)' }
      );
    }
  }, [showHowItWorksModal]);

  const handleLogout = () => {
    auth.clearAuth();
    window.location.href = '/login.html';
  };

  const displayName = user?.name ? user.name.split(' ')[0] : 'Student';

  return (
    <>
      <header className="border-b border-canvas-border bg-canvas/80 backdrop-blur-md sticky top-0 z-30 transition-all">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-3">
          
          {/* Brand */}
          <a href="/index.html" className="flex items-center shrink-0 group">
            <img src="/logo.png" alt="HackMate" className="h-8 sm:h-9 w-auto object-contain group-hover:scale-105 transition-transform" />
          </a>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-5 text-xs sm:text-sm font-semibold text-ink-secondary">
            <a href="/browse-teams.html" className="hover:text-terracotta transition-colors whitespace-nowrap">
              Browse Teams
            </a>
            {loggedIn && (
              <a href="/dashboard.html" className="hover:text-terracotta transition-colors whitespace-nowrap font-bold text-terracotta">
                Dashboard
              </a>
            )}
            <button
              type="button"
              onClick={() => setShowHowItWorksModal(true)}
              className="hover:text-terracotta transition-colors whitespace-nowrap cursor-pointer text-xs sm:text-sm font-semibold text-ink-secondary"
            >
              How It Works
            </button>
          </nav>

          {/* Actions & User State */}
          <div className="flex items-center gap-2 sm:gap-3 shrink-0">
            {loggedIn ? (
              <>
                {onOpenCreateModal && (
                  <button
                    onClick={onOpenCreateModal}
                    className="interactive-btn px-3 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-all shadow-xs whitespace-nowrap cursor-pointer"
                  >
                    + Post Squad
                  </button>
                )}

                {/* Profile Pill */}
                <a
                  href="/dashboard.html"
                  className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg bg-white border border-canvas-border hover:border-terracotta transition-all shadow-xs"
                  title={`${user?.name} (${user?.email})`}
                >
                  <div className="w-6 h-6 rounded-full bg-ochre-light border border-ochre-border text-ochre font-extrabold text-xs flex items-center justify-center shrink-0">
                    {user?.name ? user.name[0].toUpperCase() : 'S'}
                  </div>
                  <span className="text-xs font-bold text-ink max-w-[80px] sm:max-w-[120px] truncate">
                    {displayName}
                  </span>
                </a>

                <button
                  onClick={handleLogout}
                  className="px-2 py-1.5 text-xs font-semibold text-ink-muted hover:text-ink transition-colors whitespace-nowrap cursor-pointer"
                  title="Sign out"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <a
                  href="/login.html"
                  className="px-3 py-1.5 text-xs sm:text-sm font-semibold text-ink-secondary hover:text-ink whitespace-nowrap transition-colors"
                >
                  Sign In
                </a>
                <a
                  href="/login.html#register"
                  className="interactive-btn px-3.5 sm:px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-all shadow-xs whitespace-nowrap"
                >
                  Join Campus
                </a>
              </>
            )}
          </div>

        </div>
      </header>

      {/* How It Works Modal */}
      {showHowItWorksModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-ink/40 backdrop-blur-xs">
          <div ref={modalRef} className="paper-card rounded-2xl max-w-lg w-full p-6 sm:p-7 shadow-2xl relative border border-canvas-border">
            
            <div className="flex items-center justify-between mb-5 pb-3 border-b border-canvas-border">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-terracotta"></span>
                <h2 className="font-heading font-black text-ink text-xl">
                  How HackMate Works
                </h2>
              </div>
              <button
                onClick={() => setShowHowItWorksModal(false)}
                className="text-ink-muted hover:text-ink text-xl font-bold p-1 leading-none cursor-pointer"
              >
                ×
              </button>
            </div>

            <div className="space-y-3 mb-6">
              <div className="p-3.5 rounded-xl bg-canvas-alt border border-canvas-border flex items-start gap-3">
                <div className="w-6 h-6 rounded-md bg-terracotta text-white font-mono font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                  1
                </div>
                <div>
                  <h3 className="font-heading font-bold text-ink text-sm">Post or Filter Squads</h3>
                  <p className="text-xs text-ink-secondary mt-0.5 leading-relaxed">
                    Filter by skills (React, Python, OpenCV, Solidity) or target hackathons.
                  </p>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-canvas-alt border border-canvas-border flex items-start gap-3">
                <div className="w-6 h-6 rounded-md bg-terracotta text-white font-mono font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                  2
                </div>
                <div>
                  <h3 className="font-heading font-bold text-ink text-sm">Send Collaboration Pitch</h3>
                  <p className="text-xs text-ink-secondary mt-0.5 leading-relaxed">
                    Submit your background, preferred role, and projects to the squad creator.
                  </p>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-canvas-alt border border-canvas-border flex items-start gap-3">
                <div className="w-6 h-6 rounded-md bg-terracotta text-white font-mono font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                  3
                </div>
                <div>
                  <h3 className="font-heading font-bold text-ink text-sm">Review & Lock Squad</h3>
                  <p className="text-xs text-ink-secondary mt-0.5 leading-relaxed">
                    Leaders review pitches in their dashboard and accept teammates to fill spots.
                  </p>
                </div>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => setShowHowItWorksModal(false)}
                className="interactive-btn px-5 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover cursor-pointer"
              >
                Close Guide
              </button>
            </div>

          </div>
        </div>
      )}
    </>
  );
}
