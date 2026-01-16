import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor to inject JWT access token into outgoing request headers
api.interceptors.request.use(
    (config) => {
        // Retrieve token from browser local storage
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Interceptor to handle token expiration
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            // Clear token and redirect to login if unauthorized
            localStorage.removeItem('token');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const authService = {
    login: (credentials) => api.post('/auth/login', credentials),
    register: (userData) => api.post('/auth/register', userData),
    getMe: () => api.get('/auth/me'),
};

export const tradeService = {
    getTrades: (params) => api.get('/trades/', { params }),
    createTrade: (tradeData) => api.post('/trades/', tradeData),
    cancelTrade: (id) => api.post(`/trades/${id}/cancel`),
};

export const portfolioService = {
    getPortfolio: () => api.get('/portfolio/'),
    getPerformance: () => api.get('/portfolio/performance'),
};

export const workflowService = {
    getWorkflows: () => api.get('/workflows/'),
    createWorkflow: (data) => api.post('/workflows/', data),
    executeWorkflow: (id) => api.post(`/workflows/${id}/execute`),
    toggleWorkflow: (id) => api.post(`/workflows/${id}/activate`),
};

export default api;
