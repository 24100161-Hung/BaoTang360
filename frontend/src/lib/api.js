import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
})

export default api

export const sceneApi = {
  list: (params) => api.get('/v1/scenes', { params }),
  get: (slug) => api.get(`/v1/scenes/${slug}`),
}

export const tourApi = {
  list: () => api.get('/v1/tours'),
  get: (slug) => api.get(`/v1/tours/${slug}`),
}

export const logApi = {
  send: (data) => api.post('/v1/logs', data),
}
