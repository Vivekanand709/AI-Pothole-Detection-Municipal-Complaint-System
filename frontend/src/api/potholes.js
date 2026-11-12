import apiClient from './client';

export const potholeService = {
  getPotholes: async (params = {}) => {
    const response = await apiClient.get('/api/potholes', { params });
    return response.data;
  },

  getPotholesForMap: async (params = {}) => {
    const response = await apiClient.get('/api/potholes/map', { params });
    return response.data;
  },

  getPothole: async (id) => {
    const response = await apiClient.get(`/api/potholes/${id}`);
    return response.data;
  },

  updatePotholeStatus: async (id, status) => {
    const response = await apiClient.patch(`/api/potholes/${id}/status?status=${status}`);
    return response.data;
  },

  deletePothole: async (id) => {
    const response = await apiClient.delete(`/api/potholes/${id}`);
    return response.data;
  }
};
