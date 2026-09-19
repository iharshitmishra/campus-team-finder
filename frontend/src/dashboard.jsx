import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
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

      // Fetch all teams and filter for owned teams
      const allTeams = await api.getTeams();
      const myTeams = allTeams.filter(t => t.createdBy === user.id);
      setOwnedTeams(myTeams);

      // Fetch received & sent requests
      const [received, sent] = await Promise.all([
        api.getReceivedRequests(),
        api.getSentRequests()
      ]);
      setReceivedRequests(received);
      setSentRequests(sent);
    } catch (err) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(''), 4500);
  };

  const handleRequestDecision = async (requestId, status) => {
    try {
      await api.updateRequestStatus(requestId, status);
      showToast(status === 'ACCEPTED' ? 'Applicant accepted! Added to your team roster.' : 'Application declined.');
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  const handleDeleteTeam = async (teamId) => {
    if (!confirm('Are you sure you want to delete this team post? All join applications for this team will also be deleted.')) {
      return;
    }
    try {
      await api.deleteTeam(teamId);
      showToast('Team post deleted successfully.');
      loadData();
    } catch (err) {
      showToast(`Error deleting team: ${err.message}`);
    }
  };

  const handleToggleStatus = async (team) => {
    const nextStatus = team.status === 'OPEN' ? 'CLOSED' : 'OPEN';
    try {
      await api.updateTeam(team.id, { status: nextStatus });
      showToast(`Team status changed to ${nextStatus}.`);
      loadData();
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-canvas text-ink">
      <Navbar onOpenCreateModal={() => setShowCreateModal(true)} />

      {toast && (
        <div className="max-w-6xl mx-auto px-4 sm:px-6 w-full pt-5">
          <div className="p-4 bg-sage-light border border-sage-border text-sage rounded-xl text-sm font-semibold flex items-center justify-between shadow-xs">
            <span>✓ {toast}</span>
            <button onClick={() => setToast('')} className="text-sage text-lg font-bold">×</button>
          </div>
        </div>
      )}

      <main className="flex-1 max-w-6xl mx-auto px-4 sm:px-6 py-10 w-full">
        
        {/* Profile Banner */}
        {currentUser && (
          <div className="paper-card rounded-2xl p-6 sm:p-8 mb-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div>
              <div className="flex items-center gap-4 mb-2">
                <div className="w-14 h-14 rounded-2xl bg-ochre-light border border-ochre-border text-ochre font-heading font-extrabold text-2xl flex items-center justify-center shadow-xs">
                  {currentUser.name ? currentUser.name[0].toUpperCase() : 'S'}
                </div>
                <div>
                  <h1 className="font-heading font-extrabold text-ink text-2xl sm:text-3xl">
                    {currentUser.name}
                  </h1>
                  <p className="text-sm text-ink-secondary mt-0.5">
                    {currentUser.email} • {currentUser.branch || 'Campus Student'} {currentUser.year ? `(${currentUser.year})` : ''}
                  </p>
                </div>
              </div>

              {/* Skills */}
              <div className="flex flex-wrap items-center gap-2 mt-4">
                <span className="text-xs font-bold font-mono text-ink-muted uppercase tracking-wider mr-1">My Skills:</span>
                {currentUser.skills && currentUser.skills.length > 0 ? (
                  currentUser.skills.map((s, idx) => (
                    <span key={idx} className="text-xs font-semibold px-3 py-1 rounded-md bg-canvas-alt text-ink border border-canvas-border">
                      {s}
                    </span>
                  ))
                ) : (
                  <span className="text-xs text-ink-muted italic">No skills listed</span>
                )}
              </div>
            </div>

            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowCreateModal(true)}
                className="px-5 py-3 rounded-lg text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover transition-colors shadow-sm"
              >
                + Post a Team Requirement
              </button>
            </div>
          </div>
        )}

        {/* Dashboard Navigation Tabs */}
        <div className="flex items-center gap-6 border-b border-canvas-border mb-8">
          <button
            onClick={() => setActiveTab('owned')}
            className={`pb-3 text-sm sm:text-base font-bold tracking-tight transition-colors border-b-2 ${
              activeTab === 'owned'
                ? 'border-terracotta text-terracotta'
                : 'border-transparent text-ink-muted hover:text-ink'
            }`}
          >
            Teams You Lead & Review Applicants ({ownedTeams.length})
          </button>

          <button
            onClick={() => setActiveTab('sent')}
            className={`pb-3 text-sm sm:text-base font-bold tracking-tight transition-colors border-b-2 ${
              activeTab === 'sent'
                ? 'border-terracotta text-terracotta'
                : 'border-transparent text-ink-muted hover:text-ink'
            }`}
          >
            My Sent Applications ({sentRequests.length})
          </button>
        </div>

        {/* Tab 1: Teams You Lead & Review Applicants */}
        {activeTab === 'owned' && (
          <div className="space-y-8">
            {loading ? (
              <div className="py-16 text-center text-sm font-mono text-ink-muted">Loading your teams...</div>
            ) : ownedTeams.length === 0 ? (
              <div className="paper-card rounded-xl p-12 text-center">
                <h3 className="font-heading font-bold text-ink text-2xl mb-2">
                  You haven't posted any hackathon teams yet
                </h3>
                <p className="text-sm text-ink-muted mb-6 max-w-md mx-auto">
                  Planning to compete in SIH, ETHIndia, or an upcoming campus codefest? Post your team requirement and invite teammates.
                </p>
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="px-5 py-2.5 rounded-lg text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover"
                >
                  Create Team Requirement
                </button>
              </div>
            ) : (
              ownedTeams.map((team) => {
                const teamRequests = receivedRequests.filter(r => r.teamId === team.id);
                const pendingRequests = teamRequests.filter(r => r.status === 'PENDING');

                return (
                  <div key={team.id} className="paper-card rounded-xl p-6 sm:p-8">
                    {/* Team Header */}
                    <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4 pb-5 border-b border-canvas-border">
                      <div>
                        <div className="flex items-center gap-2 mb-2">
                          <span className="badge-tag uppercase font-bold px-2.5 py-0.5 rounded bg-ochre-light text-ochre border border-ochre-border text-xs">
                            {team.hackathonName}
                          </span>
                          <span className={`badge-tag uppercase font-bold px-2.5 py-0.5 rounded text-xs ${
                            team.status === 'OPEN'
                              ? 'bg-sage-light text-sage border border-sage-border'
                              : 'bg-canvas-alt text-ink-muted border border-canvas-border'
                          }`}>
                            {team.status}
                          </span>
                        </div>
                        <h2 className="font-heading font-extrabold text-ink text-2xl">
                          {team.title}
                        </h2>
                        <p className="text-sm text-ink-muted mt-1 font-medium">
                          {team.currentMembers?.length || 1} of {team.teamSize} spots filled
                        </p>
                      </div>

                      <div className="flex items-center gap-2.5">
                        <button
                          onClick={() => handleToggleStatus(team)}
                          className="px-3.5 py-2 text-xs sm:text-sm border border-canvas-border rounded-lg text-ink font-semibold hover:bg-canvas-alt"
                        >
                          {team.status === 'OPEN' ? 'Close Recruitment' : 'Re-open Team'}
                        </button>
                        <button
                          onClick={() => handleDeleteTeam(team.id)}
                          className="px-3.5 py-2 text-xs sm:text-sm border border-terracotta-border text-terracotta hover:bg-terracotta-light rounded-lg font-semibold"
                        >
                          Delete Team
                        </button>
                      </div>
                    </div>

                    {/* Team Roster */}
                    <div className="py-5 border-b border-canvas-border">
                      <h4 className="text-xs font-mono uppercase text-ink-muted mb-3 font-bold tracking-wider">
                        Current Team Roster ({team.currentMembers?.length || 1} of {team.teamSize})
                      </h4>
                      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
                        {team.currentMembers?.map((m, idx) => (
                          <div key={idx} className="p-3.5 rounded-lg bg-canvas-alt border border-canvas-border text-sm flex items-center justify-between">
                            <span className="font-bold text-ink">{m.name}</span>
                            <span className="text-xs font-mono text-ink-muted bg-canvas-card px-2 py-0.5 rounded border border-canvas-border">{m.role || 'Member'}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Incoming Join Requests */}
                    <div className="pt-5">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <h4 className="text-xs font-mono uppercase text-ink-muted font-bold tracking-wider">
                            Incoming Student Applications ({teamRequests.length})
                          </h4>
                          <p className="text-xs text-ink-muted mt-0.5">
                            Applicants are only added to your roster when you click <strong>Accept Member</strong>.
                          </p>
                        </div>
                        {pendingRequests.length > 0 && (
                          <span className="badge-tag px-3 py-1 rounded-full bg-ochre-light text-ochre font-bold text-xs">
                            {pendingRequests.length} pending your review
                          </span>
                        )}
                      </div>

                      {teamRequests.length === 0 ? (
                        <p className="text-sm text-ink-muted italic py-2">
                          No student applications received yet for this team.
                        </p>
                      ) : (
                        <div className="space-y-3.5">
                          {teamRequests.map((req) => (
                            <div key={req.id} className="p-5 rounded-xl border border-canvas-border bg-canvas text-sm flex flex-col sm:flex-row sm:items-center justify-between gap-5">
                              <div className="max-w-xl">
                                <div className="flex items-center gap-2.5 mb-1.5">
                                  <span className="font-extrabold text-ink text-base">{req.userName}</span>
                                  <span className="text-ink-muted text-xs">({req.userBranch}, {req.userYear})</span>
                                  <span className={`badge-tag uppercase px-2 py-0.5 rounded font-mono text-[11px] font-bold ${
                                    req.status === 'ACCEPTED' ? 'bg-sage-light text-sage border border-sage-border' :
                                    req.status === 'REJECTED' ? 'bg-terracotta-light text-terracotta border border-terracotta-border' :
                                    'bg-ochre-light text-ochre border border-ochre-border'
                                  }`}>
                                    {req.status}
                                  </span>
                                </div>
                                <p className="text-ink-secondary leading-relaxed mb-3 italic">
                                  "{req.message || 'No message provided.'}"
                                </p>
                                {req.userSkills && req.userSkills.length > 0 && (
                                  <div className="flex flex-wrap gap-1.5">
                                    {req.userSkills.map((s, idx) => (
                                      <span key={idx} className="badge-tag px-2 py-0.5 rounded bg-canvas-card border border-canvas-border text-xs text-ink-secondary font-medium">
                                        {s}
                                      </span>
                                    ))}
                                  </div>
                                )}
                              </div>

                              {/* Decision buttons */}
                              {req.status === 'PENDING' ? (
                                <div className="flex items-center gap-2.5 shrink-0">
                                  <button
                                    onClick={() => handleRequestDecision(req.id, 'ACCEPTED')}
                                    className="px-4 py-2 rounded-lg bg-sage text-white text-xs sm:text-sm font-bold hover:bg-sage/90 shadow-xs"
                                  >
                                    Accept Member
                                  </button>
                                  <button
                                    onClick={() => handleRequestDecision(req.id, 'REJECTED')}
                                    className="px-4 py-2 rounded-lg border border-canvas-border text-ink-secondary text-xs sm:text-sm font-bold hover:text-terracotta hover:border-terracotta"
                                  >
                                    Decline
                                  </button>
                                </div>
                              ) : (
                                <div className="text-xs font-mono font-bold text-ink-muted shrink-0">
                                  {req.status === 'ACCEPTED' ? '✓ Added to Roster' : '✗ Declined'}
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

        {/* Tab 2: My Sent Applications */}
        {activeTab === 'sent' && (
          <div>
            {loading ? (
              <div className="py-16 text-center text-sm font-mono text-ink-muted">Loading your applications...</div>
            ) : sentRequests.length === 0 ? (
              <div className="paper-card rounded-xl p-12 text-center">
                <h3 className="font-heading font-bold text-ink text-2xl mb-2">
                  You haven't applied to any teams yet
                </h3>
                <p className="text-sm text-ink-muted mb-6">
                  Browse open teams on the campus directory and pitch your skills to team leaders.
                </p>
                <a
                  href="/browse-teams.html"
                  className="px-5 py-2.5 rounded-lg text-sm font-bold bg-terracotta text-white hover:bg-terracotta-hover inline-block"
                >
                  Browse Open Teams
                </a>
              </div>
            ) : (
              <div className="space-y-4">
                {sentRequests.map((req) => (
                  <div key={req.id} className="paper-card rounded-xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-5">
                    <div>
                      <div className="flex items-center gap-2 mb-1.5">
                        <span className="badge-tag uppercase px-2.5 py-0.5 rounded bg-ochre-light text-ochre border border-ochre-border text-xs font-bold">
                          {req.hackathonName}
                        </span>
                        <span className={`badge-tag uppercase px-2.5 py-0.5 rounded text-xs font-bold ${
                          req.status === 'ACCEPTED' ? 'bg-sage-light text-sage border border-sage-border' :
                          req.status === 'REJECTED' ? 'bg-terracotta-light text-terracotta border border-terracotta-border' :
                          'bg-ochre-light text-ochre border border-ochre-border'
                        }`}>
                          {req.status === 'PENDING' ? '⏳ PENDING REVIEW' : req.status}
                        </span>
                      </div>
                      <h3 className="font-heading font-bold text-ink text-xl">
                        {req.teamTitle}
                      </h3>
                      <p className="text-xs text-ink-muted mt-1">
                        Applied on {new Date(req.createdAt).toLocaleDateString()}
                      </p>
                      <p className="text-sm text-ink-secondary mt-2.5 max-w-xl italic leading-relaxed">
                        "{req.message}"
                      </p>
                    </div>

                    <div className="shrink-0 text-left sm:text-right">
                      {req.status === 'ACCEPTED' && (
                        <div className="p-3 rounded-lg bg-sage-light border border-sage-border text-sage font-bold text-sm">
                          ✓ Accepted by Team Leader! You are on the roster.
                        </div>
                      )}
                      {req.status === 'PENDING' && (
                        <div className="text-xs font-mono font-bold text-ochre bg-ochre-light px-3 py-1.5 rounded-md border border-ochre-border">
                          Awaiting Team Leader Decision
                        </div>
                      )}
                      {req.status === 'REJECTED' && (
                        <div className="text-xs font-mono font-semibold text-ink-muted">
                          Application declined by leader
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
            showToast('Team posted successfully!');
            loadData();
          }}
        />
      )}

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
      <DashboardApp />
    </React.StrictMode>
  );
}
