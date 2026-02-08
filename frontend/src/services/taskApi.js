import { api } from './authApi';

const taskApi = {
  // Get all tasks for a user
  async getTasks(userId, params = {}) {
    const queryParams = new URLSearchParams(params);
    const response = await api.get(`/${userId}/tasks?${queryParams}`);
    return response.data;
  },

  // Create a new task for a user
  async createTask(userId, taskData) {
    const response = await api.post(`/${userId}/tasks`, taskData);
    return response.data;
  },

  // Get a specific task
  async getTask(userId, taskId) {
    const response = await api.get(`/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Update a task
  async updateTask(userId, taskId, taskData) {
    const response = await api.put(`/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  },

  // Delete a task
  async deleteTask(userId, taskId) {
    const response = await api.delete(`/${userId}/tasks/${taskId}`);
    return response.data;
  },

  // Toggle task completion status
  async toggleTaskCompletion(userId, taskId, completed) {
    const response = await api.patch(`/${userId}/tasks/${taskId}/complete`, {
      completed
    });
    return response.data;
  }
};

export default taskApi;