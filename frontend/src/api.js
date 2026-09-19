// Lightweight REST Client for Hackathon Team Finder

const API_BASE = (import.meta.env.VITE_API_BASE || '').replace(/\/$/, '') + '/api';

export const auth = {
  getToken: () => localStorage.getItem('htf_token'),
  getUser: () => {
    try {
      const u = localStorage.getItem('htf_user');
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  },
  setAuth: (token, user) => {
    if (token) localStorage.setItem('htf_token', token);
    if (user) localStorage.setItem('htf_user', JSON.stringify(user));
  },
  clearAuth: () => {
    localStorage.removeItem('htf_token');
    localStorage.removeItem('htf_user');
  },
  isLoggedIn: () => {
    return !!(localStorage.getItem('htf_token') && localStorage.getItem('htf_user'));
  }
};

export async function apiCall(endpoint, options = {}) {
  const token = auth.getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });

  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Request failed with status ${res.status}`);
  }
  return data;
}

export const api = {
  // Auth
  login: (email, password) => apiCall('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }),
  register: (payload) => apiCall('/auth/register', { method: 'POST', body: JSON.stringify(payload) }),
  getMe: async () => {
    try {
      return await apiCall('/users/me');
    } catch (err) {
      // If profile verification specifically fails, clear invalid session
      if (err.message && err.message.toLowerCase().includes('unauthorized')) {
        auth.clearAuth();
      }
      throw err;
    }
  },

  // Teams
  getTeams: (params = {}) => {
    const query = new URLSearchParams();
    if (params.skill) query.set('skill', params.skill);
    if (params.hackathon) query.set('hackathon', params.hackathon);
    if (params.status) query.set('status', params.status);
    if (params.search) query.set('search', params.search);
    const qs = query.toString();
    return apiCall(`/teams${qs ? '?' + qs : ''}`);
  },
  getTeam: (id) => apiCall(`/teams/${id}`),
  createTeam: (payload) => apiCall('/teams', { method: 'POST', body: JSON.stringify(payload) }),
  updateTeam: (id, payload) => apiCall(`/teams/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  deleteTeam: (id) => apiCall(`/teams/${id}`, { method: 'DELETE' }),

  // Join Requests
  sendRequest: (teamId, message) => apiCall('/requests', { method: 'POST', body: JSON.stringify({ teamId, message }) }),
  getReceivedRequests: () => apiCall('/requests/received'),
  getSentRequests: () => apiCall('/requests/sent'),
  updateRequestStatus: (id, status) => apiCall(`/requests/${id}`, { method: 'PUT', body: JSON.stringify({ status }) })
};
