import apiClient from './client';

export const dashboardService = {
  getStats: async () => {
    const response = await apiClient.get('/api/dashboard/stats');
    return response.data;
  },

  getRecentActivity: async (limit = 10) => {
    const response = await apiClient.get('/api/dashboard/recent-activity', {
      params: { limit }
    });
    return response.data;
  }
};
