import apiClient from './client';

export const authService = {
  login: async (email, password) => {
    // Demo mode - simulate login
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          access_token: "demo-token-" + Date.now(),
          token_type: "bearer",
          user: {
            id: 1,
            name: "Demo User",
            email: email,
            role: "Municipal Officer"
          }
        });
      }, 500);
    });
  },

  register: async (userData) => {
    const response = await apiClient.post('/api/auth/register', userData);
    return response.data;
  },

  getCurrentUser: async () => {
    // Return demo user
    return {
      id: 1,
      name: "Demo User",
      email: "demo@municipal.gov",
      role: "Municipal Officer"
    };
  },

  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },

  getUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }
};
