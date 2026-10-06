import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom/client';
import { gsap } from 'gsap';
import Navbar from './components/Navbar';
import FilterBar from './components/FilterBar';
import TeamCard from './components/TeamCard';
import CreateTeamModal from './components/CreateTeamModal';
import ApplyModal from './components/ApplyModal';
import { api, auth } from './api';
import './style.css';

function TeamListingApp() {
  const [teams, setTeams] = useState([]);
  const [sentRequestsMap, setSentRequestsMap] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [notification, setNotification] = useState('');

  const [filters, setFilters] = useState({
    skill: '',
    hackathon: '',
    status: '',
    search: ''
  });

  const [selectedTeamForApply, setSelectedTeamForApply] = useState(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const toastRef = useRef(null);

  const fetchTeamsAndRequests = async () => {
    setLoading(true);
    setError('');
    try {
      const teamsData = await api.getTeams(filters);
      setTeams(teamsData);

      if (auth.isLoggedIn()) {
        try {
          const sent = await api.getSentRequests();
          const reqMap = {};
          for (const req of sent) {
            reqMap[req.teamId] = req.status;
          }
          setSentRequestsMap(reqMap);
        } catch {
          // non-blocking
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch squads');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTeamsAndRequests();
  }, [filters]);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get('create') === '1' && auth.isLoggedIn()) {
      setShowCreateModal(true);
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  // GSAP animation when teams render
  useEffect(() => {
    if (!loading && teams.length > 0) {
      gsap.fromTo(
        '.team-card',
        { opacity: 0, y: 20 },
        { opacity: 1, y: 0, stagger: 0.05, duration: 0.4, ease: 'power2.out' }
      );
    }
  }, [loading, teams]);

  const showToast = (msg) => {
    setNotification(msg);
    if (toastRef.current) {
      gsap.fromTo(toastRef.current, { opacity: 0, y: -15 }, { opacity: 1, y: 0, duration: 0.3 });
    }
    setTimeout(() => setNotification(''), 4500);
  };

  const handleApplySuccess = (msg) => {
    showToast(msg);
    fetchTeamsAndRequests();
  };

  const handleCreateSuccess = (newTeam) => {
    showToast(`Squad "${newTeam.title}" created successfully!`);
    fetchTeamsAndRequests();
  };

  const resetFilters = () => {
    setFilters({ skill: '', hackathon: '', status: '', search: '' });
  };

  return (
    <div className="min-h-screen flex flex-col bg-canvas text-ink">
      <Navbar onOpenCreateModal={() => setShowCreateModal(true)} />

      {notification && (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 w-full pt-4">
          <div ref={toastRef} className="p-3.5 bg-sage-light border border-sage-border text-sage rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-between shadow-xs">
            <span>✓ {notification}</span>
            <button onClick={() => setNotification('')} className="text-sage text-base font-bold cursor-pointer">×</button>
          </div>
        </div>
      )}

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-10 w-full">
        
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-8 pb-6 border-b border-canvas-border">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="w-2 h-2 rounded-full bg-terracotta"></span>
              <span className="text-[11px] uppercase font-bold tracking-widest text-terracotta font-mono">
                Active Campus Squads
              </span>
            </div>
            <h1 className="font-heading font-black text-ink text-3xl sm:text-4xl tracking-tight">
              Explore Hackathon Squads
            </h1>
            <p className="text-xs sm:text-sm text-ink-secondary mt-1">
              Find squads looking for your technical stack or start your own.
            </p>
          </div>

          <div className="flex items-center gap-3 shrink-0">
            <button
              onClick={() => {
                if (!auth.isLoggedIn()) {
                  window.location.href = '/login.html';
                } else {
                  setShowCreateModal(true);
                }
              }}
              className="interactive-btn px-4 py-2.5 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-xs cursor-pointer"
            >
              + Post Squad Requirement
            </button>
          </div>
        </div>

        {/* Filter Controls */}
        <FilterBar
          filters={filters}
          onFilterChange={setFilters}
          onReset={resetFilters}
        />

        {/* Squads List */}
        {loading ? (
          <div className="py-20 text-center text-xs sm:text-sm font-mono text-ink-muted">
            <div className="inline-block w-6 h-6 border-2 border-terracotta border-t-transparent rounded-full animate-spin mb-3"></div>
            <div>Loading squads...</div>
          </div>
        ) : error ? (
          <div className="p-4 bg-terracotta-light border border-terracotta-border text-terracotta text-xs sm:text-sm rounded-xl text-center my-6 font-semibold">
            {error}
          </div>
        ) : teams.length === 0 ? (
          <div className="paper-card rounded-2xl p-12 text-center my-6 border border-canvas-border">
            <h3 className="font-heading font-bold text-ink text-xl mb-1">
              No matching squads found
            </h3>
            <p className="text-xs sm:text-sm text-ink-muted mb-5">
              Try resetting your filters or post a new squad requirement.
            </p>
            <button
              onClick={() => {
                if (!auth.isLoggedIn()) {
                  window.location.href = '/login.html';
                } else {
                  setShowCreateModal(true);
                }
              }}
              className="interactive-btn px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover"
            >
              + Post Squad
            </button>
          </div>
        ) : (
          <div>
            <div className="flex items-center justify-between text-xs text-ink-muted mb-4 font-mono">
              <span className="font-semibold">{teams.length} Squad{teams.length !== 1 ? 's' : ''} Available</span>
              {filters.skill && <span>Filter: <strong className="text-terracotta">{filters.skill}</strong></span>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
              {teams.map((team) => (
                <TeamCard
                  key={team.id}
                  team={team}
                  onApply={setSelectedTeamForApply}
                  userRequestStatus={sentRequestsMap[team.id] || null}
                />
              ))}
            </div>
          </div>
        )}

      </main>

      {/* Modals */}
      {selectedTeamForApply && (
        <ApplyModal
          team={selectedTeamForApply}
          onClose={() => setSelectedTeamForApply(null)}
          onSuccess={handleApplySuccess}
        />
      )}

      {showCreateModal && (
        <CreateTeamModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={handleCreateSuccess}
        />
      )}

      <footer className="border-t border-canvas-border py-6 mt-12 bg-canvas-alt text-center text-xs text-ink-muted">
        HackMate • Connect, Pitch & Compete
      </footer>
    </div>
  );
}

const rootEl = document.getElementById('root');
if (rootEl) {
  ReactDOM.createRoot(rootEl).render(
    <React.StrictMode>
      <TeamListingApp />
    </React.StrictMode>
  );
}
