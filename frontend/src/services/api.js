import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Agents API
export const agentsAPI = {
  getAll: () => api.get('/agents'),
  getById: (id) => api.get(`/agents/${id}`),
  create: (data) => api.post('/agents', data),
  update: (id, data) => api.put(`/agents/${id}`, data),
  delete: (id) => api.delete(`/agents/${id}`),
};

// Tools API
export const toolsAPI = {
  getAll: () => api.get('/tools'),
  getById: (id) => api.get(`/tools/${id}`),
  create: (data) => api.post('/tools', data),
  update: (id, data) => api.put(`/tools/${id}`, data),
  delete: (id) => api.delete(`/tools/${id}`),
};

// Workflows API
export const workflowsAPI = {
  getAll: () => api.get('/workflows'),
  getById: (id) => api.get(`/workflows/${id}`),
  create: (data) => api.post('/workflows', data),
  update: (id, data) => api.put(`/workflows/${id}`, data),
  delete: (id) => api.delete(`/workflows/${id}`),
  run: (id, input = {}) => api.post(`/workflows/${id}/run`, input),
};

// Solutions API (Runs)
export const solutionsAPI = {
  getAll: () => api.get('/solutions'),
  getById: (id) => api.get(`/solutions/${id}`),
  create: (data) => api.post('/solutions', data),
  update: (id, data) => api.put(`/solutions/${id}`, data),
  delete: (id) => api.delete(`/solutions/${id}`),
  
  // Workflow management
  addWorkflow: (solutionId, workflowId) => api.post(`/solutions/${solutionId}/workflows/${workflowId}`),
  removeWorkflow: (solutionId, workflowId) => api.delete(`/solutions/${solutionId}/workflows/${workflowId}`),
  getWorkflows: (solutionId) => api.get(`/solutions/${solutionId}/workflows`),
  
  // Communication
  sendCommunication: (solutionId, data) => api.post(`/solutions/${solutionId}/communicate`, data),
  getCommunications: (solutionId) => api.get(`/solutions/${solutionId}/communications`),
  
  // New: Workflow communication endpoints
  getSummary: (solutionId) => api.get(`/workflows/solution/${solutionId}/summary`),
  clearMemory: (solutionId) => api.delete(`/workflows/solution/${solutionId}/memory`),
  communicate: (data) => api.post('/workflows/communicate', data),
  
  // Legacy runs endpoint
  getRuns: () => api.get('/workflows/runs'),
  getRunById: (id) => api.get(`/workflows/runs/${id}`),
};

// Chat API
export const chatAPI = {
  getSessions: () => api.get('/chat/sessions'),
  getSession: (sessionId) => api.get(`/chat/sessions/${sessionId}`),
  createSession: (data) => api.post('/chat/sessions', data),
  deleteSession: (sessionId) => api.delete(`/chat/sessions/${sessionId}`),
  sendMessage: (sessionId, message) => api.post(`/chat/sessions/${sessionId}/message`, { message }),
  
  // Solution-aware features
  switchWorkflow: (sessionId, data) => api.post(`/chat/sessions/${sessionId}/switch-workflow`, data),
  getSolutionContext: (sessionId) => api.get(`/chat/sessions/${sessionId}/solution-context`),
  getBlueprint: (sessionId) => api.get(`/chat/sessions/${sessionId}/blueprint`),
};

export default api;
