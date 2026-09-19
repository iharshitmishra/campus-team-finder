import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
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

  const fetchTeamsAndRequests = async () => {
    setLoading(true);
    setError('');
    try {
      const teamsData = await api.getTeams(filters);
      setTeams(teamsData);

      // If logged in, fetch sent requests to know which teams have pending applications
      if (auth.isLoggedIn()) {
        try {
          const sent = await api.getSentRequests();
          const reqMap = {};
          for (const req of sent) {
            reqMap[req.teamId] = req.status; // 'PENDING', 'ACCEPTED', 'REJECTED'
          }
          setSentRequestsMap(reqMap);
        } catch {
          // non-blocking
        }
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch teams');
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

  const showToast = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(''), 5000);
  };

  const handleApplySuccess = (msg) => {
    showToast(msg);
    fetchTeamsAndRequests();
  };

  const handleCreateSuccess = (newTeam) => {
    showToast(`Team "${newTeam.title}" created successfully!`);
    fetchTeamsAndRequests();
  };

  const resetFilters = () => {
    setFilters({ skill: '', hackathon: '', status: '', search: '' });
  };

  return (
    <div className="min-h-screen flex flex-col bg-canvas text-ink">
      <Navbar onOpenCreateModal={() => setShowCreateModal(true)} />

      {notification && (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 w-full pt-5">
          <div className="p-4 bg-sage-light border border-sage-border text-sage rounded-xl text-sm font-semibold flex items-center justify-between shadow-xs">
            <span>✓ {notification}</span>
            <button onClick={() => setNotification('')} className="text-sage text-lg font-bold">×</button>
          </div>
        </div>
      )}

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-10 w-full">
        
        {/* Page Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10 pb-8 border-b border-canvas-border">
          <div>
            <span className="text-xs uppercase font-bold tracking-widest text-terracotta font-mono">
              Live Student Roster Directory
            </span>
            <h1 className="font-heading font-extrabold text-ink text-3xl sm:text-5xl mt-2 tracking-tight">
              Browse Hackathon Teams
            </h1>
            <p className="text-sm sm:text-base text-ink-secondary mt-2 max-w-2xl leading-relaxed font-normal">
              Find squads needing your technical competencies, send your collaboration pitch, and lock in your roster for upcoming hackathons.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => {
                if (!auth.isLoggedIn()) {
                  window.location.href = '/login.html';
                } else {
                  setShowCreateModal(true);
                }
              }}
              className="px-5 py-3 rounded-lg text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-sm"
            >
              + Post a Team Requirement
            </button>
          </div>
        </div>

        {/* Filter Controls */}
        <FilterBar
          filters={filters}
          onFilterChange={setFilters}
          onReset={resetFilters}
        />

        {/* Teams List */}
        {loading ? (
          <div className="py-20 text-center text-sm font-mono text-ink-muted">
            Loading campus hackathon teams...
          </div>
        ) : error ? (
          <div className="p-5 bg-terracotta-light border border-terracotta-border text-terracotta text-sm rounded-xl text-center my-8 font-semibold">
            {error}
          </div>
        ) : teams.length === 0 ? (
          <div className="paper-card rounded-xl p-14 text-center my-8">
            <h3 className="font-heading font-bold text-ink text-2xl mb-2">
              No matching teams found
            </h3>
            <p className="text-sm text-ink-muted mb-6">
              Try resetting your search filters or be the first to post a team for this hackathon!
            </p>
            <button
              onClick={() => {
                if (!auth.isLoggedIn()) {
                  window.location.href = '/login.html';
                } else {
                  setShowCreateModal(true);
                }
              }}
              className="px-5 py-2.5 rounded-lg text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover"
            >
              Create Team Requirement
            </button>
          </div>
        ) : (
          <div>
            <div className="flex items-center justify-between text-xs sm:text-sm text-ink-muted mb-5 font-mono">
              <span className="font-semibold">Showing {teams.length} active team{teams.length !== 1 ? 's' : ''}</span>
              {filters.skill && <span>Filtered by skill: <strong className="text-terracotta">{filters.skill}</strong></span>}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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

      {/* Campus Footer */}
      <footer className="border-t border-canvas-border py-8 mt-16 bg-canvas-alt text-center text-xs sm:text-sm text-ink-muted">
        Campus Hackathon Team Finder • Built by students, for students • Connect, Collaborate, Compete
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
