import React, { useState, useEffect, useRef } from 'react';
import ReactDOM from 'react-dom/client';
import { gsap } from 'gsap';
import Navbar from './components/Navbar';
import CreateTeamModal from './components/CreateTeamModal';
import { api, auth } from './api';
import './style.css';

function DashboardApp() {
  const [currentUser, setCurrentUser] = useState(null);
  const [activeTab, setActiveTab] = useState('owned'); // 'owned' | 'sent'
  const [ownedTeams, setOwnedTeams] = useState([]);
  const [receivedRequests, setReceivedRequests] = useState([]);
  const [sentRequests, setSentRequests] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [toast, setToast] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const toastRef = useRef(null);

  useEffect(() => {
    if (!auth.isLoggedIn()) {
      window.location.href = '/login.html';
      return;
    }
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    setError('');
    try {
      const user = await api.getMe();
      setCurrentUser(user);

      const allTeams = await api.getTeams();
      const myTeams = allTeams.filter(t => t.createdBy === user.id);
      setOwnedTeams(myTeams);

      const [received, sent] = await Promise.all([
        api.getReceivedRequests(),
        api.getSentRequests()
      ]);
      setReceivedRequests(received);
      setSentRequests(sent);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  // GSAP animation on tab content load
  useEffect(() => {
    if (!loading) {
      gsap.fromTo(
        '.dash-card',
        { opacity: 0, y: 15 },
        { opacity: 1, y: 0, stagger: 0.05, duration: 0.35, ease: 'power2.out' }
      );
    }
  }, [loading, activeTab]);

  const showToast = (msg) => {
    setToast(msg);
    if (toastRef.current) {
      gsap.fromTo(toastRef.current, { opacity: 0, y: -15 }, { opacity: 1, y: 0, duration: 0.3 });
    }
    setTimeout(() => setToast(''), 4000);
  };

  const handleRequestDecision = async (requestId, status) => {
    try {
      await api.updateRequestStatus(requestId, status);
      showToast(status === 'ACCEPTED' ? 'Applicant accepted to squad!' : 'Application declined.');
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  const handleDeleteTeam = async (teamId) => {
    if (!confirm('Are you sure you want to delete this squad?')) {
      return;
    }
    try {
      await api.deleteTeam(teamId);
      showToast('Squad deleted.');
      loadData();
    } catch (err) {
      showToast(`Error deleting squad: ${err.message}`);
    }
  };

  const handleToggleStatus = async (team) => {
    const nextStatus = team.status === 'OPEN' ? 'CLOSED' : 'OPEN';
    try {
      await api.updateTeam(team.id, { status: nextStatus });
      showToast(`Squad status updated to ${nextStatus}.`);
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-canvas text-ink">
      <Navbar onOpenCreateModal={() => setShowCreateModal(true)} />

      {toast && (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 w-full pt-4">
          <div ref={toastRef} className="p-3.5 bg-sage-light border border-sage-border text-sage rounded-xl text-xs sm:text-sm font-semibold flex items-center justify-between shadow-xs">
            <span>✓ {toast}</span>
            <button onClick={() => setToast('')} className="text-sage text-base font-bold cursor-pointer">×</button>
          </div>
        </div>
      )}

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-8 sm:py-10 w-full">
        
        {/* Profile Card */}
        {currentUser && (
          <div className="dash-card paper-card rounded-2xl p-6 sm:p-7 mb-8 flex flex-col md:flex-row md:items-center justify-between gap-6 border border-canvas-border">
            <div>
              <div className="flex items-center gap-3.5 mb-2">
                <div className="w-12 h-12 rounded-xl bg-ochre-light border border-ochre-border text-ochre font-heading font-black text-xl flex items-center justify-center shadow-xs">
                  {currentUser.name ? currentUser.name[0].toUpperCase() : 'S'}
                </div>
                <div>
                  <h1 className="font-heading font-black text-ink text-2xl">
                    {currentUser.name}
                  </h1>
                  <p className="text-xs text-ink-secondary mt-0.5">
                    {currentUser.email} • {currentUser.branch || 'Student'} {currentUser.year ? `(${currentUser.year})` : ''}
                  </p>
                </div>
              </div>

              {/* Skills */}
              <div className="flex flex-wrap items-center gap-1.5 mt-3">
                <span className="text-[11px] font-bold font-mono text-ink-muted uppercase tracking-wider mr-1">Skills:</span>
                {currentUser.skills && currentUser.skills.length > 0 ? (
                  currentUser.skills.map((s, idx) => (
                    <span key={idx} className="text-xs font-semibold px-2.5 py-0.5 rounded-md bg-canvas-alt text-ink border border-canvas-border">
                      {s}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-ink-muted italic">No skills added</span>
                )}
              </div>
            </div>

            <div className="flex items-center gap-2.5">
              <button
                onClick={() => setShowCreateModal(true)}
                className="interactive-btn px-4 py-2.5 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-xs cursor-pointer whitespace-nowrap"
              >
                + Post Squad Requirement
              </button>
            </div>
          </div>
        )}

        {/* Navigation Tabs */}
        <div className="flex items-center gap-4 border-b border-canvas-border mb-6">
          <button
            onClick={() => setActiveTab('owned')}
            className={`pb-2.5 text-xs sm:text-sm font-bold transition-all border-b-2 cursor-pointer ${
              activeTab === 'owned'
                ? 'border-terracotta text-terracotta'
                : 'border-transparent text-ink-muted hover:text-ink'
            }`}
          >
            Squads You Lead ({ownedTeams.length})
          </button>

          <button
            onClick={() => setActiveTab('sent')}
            className={`pb-2.5 text-xs sm:text-sm font-bold transition-all border-b-2 cursor-pointer ${
              activeTab === 'sent'
                ? 'border-terracotta text-terracotta'
                : 'border-transparent text-ink-muted hover:text-ink'
            }`}
          >
            Sent Applications ({sentRequests.length})
          </button>
        </div>

        {/* Tab 1: Squads You Lead */}
        {activeTab === 'owned' && (
          <div className="space-y-6">
            {loading ? (
              <div className="py-16 text-center text-xs font-mono text-ink-muted">Loading squads...</div>
            ) : ownedTeams.length === 0 ? (
              <div className="dash-card paper-card rounded-2xl p-10 text-center border border-canvas-border">
                <h3 className="font-heading font-bold text-ink text-xl mb-1">
                  You haven't posted any squads yet
                </h3>
                <p className="text-xs sm:text-sm text-ink-muted mb-5">
                  Post a squad requirement to recruit teammates for upcoming hackathons.
                </p>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="interactive-btn px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover cursor-pointer"
                >
                  + Post Squad
                </button>
              </div>
            ) : (
              ownedTeams.map((team) => {
                const teamRequests = receivedRequests.filter(r => r.teamId === team.id);
                const pendingRequests = teamRequests.filter(r => r.status === 'PENDING');

                return (
                  <div key={team.id} className="dash-card paper-card rounded-2xl p-5 sm:p-6 border border-canvas-border">
                    {/* Header */}
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 pb-4 border-b border-canvas-border">
                      <div>
                        <div className="flex items-center gap-2 mb-1.5">
                          <span className="badge-tag uppercase font-bold px-2 py-0.5 rounded bg-ochre-light text-ochre border border-ochre-border text-xs">
                            {team.hackathonName}
                          </span>
                          <span className={`badge-tag uppercase font-bold px-2 py-0.5 rounded text-xs ${
                            team.status === 'OPEN'
                              ? 'bg-sage-light text-sage border border-sage-border'
                              : 'bg-canvas-alt text-ink-muted border border-canvas-border'
                          }`}>
                            {team.status}
                          </span>
                        </div>
                        <h2 className="font-heading font-black text-ink text-xl">
                          {team.title}
                        </h2>
                        <p className="text-xs text-ink-muted mt-0.5 font-medium">
                          {team.currentMembers?.length || 1} of {team.teamSize} spots filled
                        </p>
                      </div>

                      <div className="flex items-center gap-2">
                        <button
                          onClick={() => handleToggleStatus(team)}
                          className="px-3 py-1.5 text-xs border border-canvas-border rounded-lg text-ink font-semibold hover:bg-canvas-alt cursor-pointer transition-colors"
                        >
                          {team.status === 'OPEN' ? 'Close Squad' : 'Reopen Squad'}
                        </button>
                        <button
                          onClick={() => handleDeleteTeam(team.id)}
                          className="px-3 py-1.5 text-xs border border-terracotta-border text-terracotta hover:bg-terracotta-light rounded-lg font-semibold cursor-pointer transition-colors"
                        >
                          Delete
                        </button>
                      </div>
                    </div>

                    {/* Roster */}
                    <div className="py-4 border-b border-canvas-border">
                      <h4 className="text-[11px] font-mono uppercase text-ink-muted mb-2.5 font-bold tracking-wider">
                        Squad Roster ({team.currentMembers?.length || 1}/{team.teamSize})
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
                        {team.currentMembers?.map((m, idx) => (
                          <div key={idx} className="p-2.5 rounded-lg bg-canvas-alt border border-canvas-border text-xs flex items-center justify-between">
                            <span className="font-bold text-ink truncate">{m.name}</span>
                            <span className="text-[10px] font-mono text-ink-muted bg-white px-1.5 py-0.5 rounded border border-canvas-border">{m.role || 'Member'}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Applications */}
                    <div className="pt-4">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="text-[11px] font-mono uppercase text-ink-muted font-bold tracking-wider">
                          Incoming Pitches ({teamRequests.length})
                        </h4>
                        {pendingRequests.length > 0 && (
                          <span className="badge-tag px-2.5 py-0.5 rounded-full bg-ochre-light text-ochre font-bold text-xs">
                            {pendingRequests.length} pending
                          </span>
                        )}
                      </div>

                      {teamRequests.length === 0 ? (
                        <p className="text-xs text-ink-muted italic py-1">
                          No applications received yet.
                        </p>
                      ) : (
                        <div className="space-y-2.5">
                          {teamRequests.map((req) => (
                            <div key={req.id} className="p-4 rounded-xl border border-canvas-border bg-white text-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                              <div className="max-w-xl">
                                <div className="flex items-center gap-2 mb-1">
                                  <span className="font-bold text-ink text-sm">{req.userName}</span>
                                  <span className="text-ink-muted text-[11px]">({req.userBranch}, {req.userYear})</span>
                                  <span className={`badge-tag uppercase px-1.5 py-0.5 rounded font-mono text-[10px] font-bold ${
                                    req.status === 'ACCEPTED' ? 'bg-sage-light text-sage border border-sage-border' :
                                    req.status === 'REJECTED' ? 'bg-terracotta-light text-terracotta border border-terracotta-border' :
                                    'bg-ochre-light text-ochre border border-ochre-border'
                                  }`}>
                                    {req.status}
                                  </span>
                                </div>
                                <p className="text-ink-secondary leading-relaxed mb-2 italic">
                                  "{req.message || 'No pitch note provided.'}"
                                </p>
                                {req.userSkills && req.userSkills.length > 0 && (
                                  <div className="flex flex-wrap gap-1">
                                    {req.userSkills.map((s, idx) => (
                                      <span key={idx} className="badge-tag px-1.5 py-0.5 rounded bg-canvas-alt border border-canvas-border text-[10px] text-ink-secondary">
                                        {s}
                                      </span>
                                    ))}
                                  </div>
                                )}
                              </div>

                              {/* Decision buttons */}
                              {req.status === 'PENDING' ? (
                                <div className="flex items-center gap-2 shrink-0">
                                  <button
                                    onClick={() => handleRequestDecision(req.id, 'ACCEPTED')}
                                    className="interactive-btn px-3 py-1.5 rounded-lg bg-sage text-white text-xs font-bold hover:bg-sage/90 shadow-xs cursor-pointer"
                                  >
                                    Accept
                                  </button>
                                  <button
                                    onClick={() => handleRequestDecision(req.id, 'REJECTED')}
                                    className="px-3 py-1.5 rounded-lg border border-canvas-border text-ink-secondary text-xs font-bold hover:text-terracotta hover:border-terracotta cursor-pointer transition-colors"
                                  >
                                    Decline
                                  </button>
                                </div>
                              ) : (
                                <div className="text-xs font-mono font-bold text-ink-muted shrink-0">
                                  {req.status === 'ACCEPTED' ? '✓ On Roster' : '✗ Declined'}
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                  </div>
                );
              })
            )}
          </div>
        )}

        {/* Tab 2: Sent Applications */}
        {activeTab === 'sent' && (
          <div>
            {loading ? (
              <div className="py-16 text-center text-xs font-mono text-ink-muted">Loading applications...</div>
            ) : sentRequests.length === 0 ? (
              <div className="dash-card paper-card rounded-2xl p-10 text-center border border-canvas-border">
                <h3 className="font-heading font-bold text-ink text-xl mb-1">
                  You haven't applied to any squads yet
                </h3>
                <p className="text-xs sm:text-sm text-ink-muted mb-5">
                  Explore active squads on the campus hub and pitch your skills to team leads.
                </p>
                <a
                  href="/browse-teams.html"
                  className="interactive-btn px-4 py-2 rounded-lg text-xs sm:text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover inline-block"
                >
                  Explore Squads
                </a>
              </div>
            ) : (
              <div className="space-y-3.5">
                {sentRequests.map((req) => (
                  <div key={req.id} className="dash-card paper-card rounded-2xl p-5 sm:p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 border border-canvas-border">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="badge-tag uppercase px-2 py-0.5 rounded bg-ochre-light text-ochre border border-ochre-border text-xs font-bold">
                          {req.hackathonName}
                        </span>
                        <span className={`badge-tag uppercase px-2 py-0.5 rounded text-xs font-bold ${
                          req.status === 'ACCEPTED' ? 'bg-sage-light text-sage border border-sage-border' :
                          req.status === 'REJECTED' ? 'bg-terracotta-light text-terracotta border border-terracotta-border' :
                          'bg-ochre-light text-ochre border border-ochre-border'
                        }`}>
                          {req.status === 'PENDING' ? '⏳ Under Review' : req.status}
                        </span>
                      </div>
                      <h3 className="font-heading font-bold text-ink text-lg">
                        {req.teamTitle}
                      </h3>
                      <p className="text-[11px] text-ink-muted mt-0.5">
                        Applied on {new Date(req.createdAt).toLocaleDateString()}
                      </p>
                      <p className="text-xs sm:text-sm text-ink-secondary mt-2 max-w-xl italic leading-relaxed">
                        "{req.message}"
                      </p>
                    </div>

                    <div className="shrink-0 text-left sm:text-right">
                      {req.status === 'ACCEPTED' && (
                        <div className="p-2.5 rounded-lg bg-sage-light border border-sage-border text-sage font-bold text-xs">
                          ✓ Accepted! You are on the squad roster.
                        </div>
                      )}
                      {req.status === 'PENDING' && (
                        <div className="text-xs font-mono font-bold text-ochre bg-ochre-light px-2.5 py-1 rounded-md border border-ochre-border">
                          Awaiting Decision
                        </div>
                      )}
                      {req.status === 'REJECTED' && (
                        <div className="text-xs font-mono font-semibold text-ink-muted">
                          Declined by lead
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

      </main>

      {showCreateModal && (
        <CreateTeamModal
          onClose={() => setShowCreateModal(false)}
          onSuccess={() => {
            showToast('Squad posted successfully!');
            loadData();
          }}
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
      <DashboardApp />
    </React.StrictMode>
  );
}
