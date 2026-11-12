import apiClient from './client';

export const ticketService = {
  getTickets: async (params = {}) => {
    const response = await apiClient.get('/api/tickets', { params });
    return response.data;
  },

  getTicket: async (id) => {
    const response = await apiClient.get(`/api/tickets/${id}`);
    return response.data;
  },

  updateTicket: async (id, data) => {
    const response = await apiClient.patch(`/api/tickets/${id}`, data);
    return response.data;
  },

  assignTicket: async (id, team) => {
    const response = await apiClient.post(`/api/tickets/${id}/assign?team=${encodeURIComponent(team)}`);
    return response.data;
  },

  resolveTicket: async (id, resolutionNotes) => {
    const response = await apiClient.post(`/api/tickets/${id}/resolve?resolution_notes=${encodeURIComponent(resolutionNotes)}`);
    return response.data;
  },

  closeTicket: async (id) => {
    const response = await apiClient.post(`/api/tickets/${id}/close`);
    return response.data;
  },

  deleteTicket: async (id) => {
    const response = await apiClient.delete(`/api/tickets/${id}`);
    return response.data;
  }
};
