import apiClient from './client';

export const citizenReportService = {
  getReports: async (params = {}) => {
    const response = await apiClient.get('/api/citizen-reports', { params });
    return response.data;
  },
  updateStatus: async (id, status) => {
    const response = await apiClient.patch(`/api/citizen-reports/${id}/status`, null, { params: { status } });
    return response.data;
  },
};
