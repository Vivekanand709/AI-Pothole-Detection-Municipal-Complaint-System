import apiClient from './client';

export const inspectionService = {
  uploadInspection: async (videoFile, metadata) => {
    const formData = new FormData();
    formData.append('video', videoFile);
    if (metadata.road_name) formData.append('road_name', metadata.road_name);
    if (metadata.area) formData.append('area', metadata.area);
    if (metadata.notes) formData.append('notes', metadata.notes);

    const response = await apiClient.post('/api/inspections/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  getInspections: async (params = {}) => {
    const response = await apiClient.get('/api/inspections', { params });
    return response.data;
  },

  getInspection: async (id) => {
    const response = await apiClient.get(`/api/inspections/${id}`);
    return response.data;
  },

  processInspection: async (id) => {
    const response = await apiClient.post(`/api/inspections/${id}/process`);
    return response.data;
  },

  updateInspection: async (id, data) => {
    const response = await apiClient.patch(`/api/inspections/${id}`, data);
    return response.data;
  },

  deleteInspection: async (id) => {
    const response = await apiClient.delete(`/api/inspections/${id}`);
    return response.data;
  }
};
