import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  },
})

// ===== Request Interceptor: Đính kèm CSRF + Bearer Token =====
api.interceptors.request.use(
  (config) => {
    // 1. CSRF token (cho session-based auth)
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content
    if (csrfToken) {
      config.headers['X-CSRF-TOKEN'] = csrfToken
    }

    // 2. Bearer Token (cho Sanctum API auth)
    const adminToken = localStorage.getItem('admin_token')
    if (adminToken) {
      config.headers['Authorization'] = `Bearer ${adminToken}`
    }

    return config
  },
  (error) => Promise.reject(error)
)

// ===== Response Interceptor: Xử lý lỗi chung =====
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status

    if (status === 401) {
      // Token hết hạn hoặc chưa đăng nhập
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_user')

      // Chỉ redirect nếu không phải đang ở trang login
      if (!window.location.pathname.includes('/login')) {
        window.location.href = '/login'
      }
    }

    if (status === 419) {
      return Promise.reject(
        new Error('Phiên làm việc đã hết hạn. Vui lòng tải lại trang.')
      )
    }

    if (status === 403) {
      console.warn('Không đủ quyền truy cập')
    }

    if (status === 429) {
      console.warn('Quá nhiều yêu cầu. Vui lòng chậm lại.')
    }

    return Promise.reject(error)
  }
)

export default api

// ============================================================
// API HELPERS
// ============================================================

// ===== Scenes (Public) =====
export const sceneApi = {
  list: (params) => api.get('/v1/scenes', { params }),
  get: (slug) => api.get(`/v1/scenes/${slug}`),
}

// ===== Tours (Public) =====
export const tourApi = {
  list: () => api.get('/v1/tours'),
  get: (slug) => api.get(`/v1/tours/${slug}`),
}

// ===== Logs =====
export const logApi = {
  send: (data) => api.post('/v1/logs', data),
}

// ===== Collections (Cần đăng nhập) =====
export const collectionApi = {
  list: () => api.get('/v1/me/collections'),
  add: (data) => api.post('/v1/me/collections', data),
  remove: (id) => api.delete(`/v1/me/collections/${id}`),
}

// ===== Auth =====
export const authApi = {
  login: (credentials) => api.post('/login', credentials),
  logout: () => api.post('/logout'),
  me: () => api.get('/me'),
}

// ===== Admin =====
export const adminApi = {
  // Scenes
  listScenes: (params) => api.get('/admin/scenes', { params }),
  createScene: (data) => api.post('/admin/scenes', data),
  updateScene: (id, data) => api.put(`/admin/scenes/${id}`, data),
  deleteScene: (id) => api.delete(`/admin/scenes/${id}`),
  uploadImage: (id, formData) =>
    api.post(`/admin/scenes/${id}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),

  // Analytics
  dropOff: () => api.get('/admin/analytics/drop-off'),
  visitorStats: () => api.get('/admin/analytics/visitor-stats'),
}
