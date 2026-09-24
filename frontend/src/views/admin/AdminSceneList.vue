<template>
  <div class="admin-page">
    <!-- Header -->
    <header class="admin-header">
      <div class="header-content">
        <div class="header-left">
          <span class="logo">⚙️</span>
          <div>
            <h1>Quản trị không gian tham quan</h1>
            <p class="subtitle">Bảo tàng ảo 360° - CSE703073</p>
          </div>
        </div>
        <div class="header-right">
          <span v-if="user" class="user-info">
            👤 {{ user.full_name || user.email }}
          </span>
          <button @click="logout" class="btn-logout">Đăng xuất</button>
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main class="container">
      <div class="toolbar">
        <h2>Danh sách không gian ({{ scenes.length }})</h2>
        <button class="btn-refresh" @click="loadScenes">🔄 Tải lại</button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>Đang tải dữ liệu...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-box">
        <p>❌ {{ error }}</p>
        <button @click="loadScenes">Thử lại</button>
      </div>

      <!-- Empty -->
      <div v-else-if="!scenes.length" class="empty-box">
        <p>📭 Chưa có không gian tham quan nào.</p>
      </div>

      <!-- Table -->
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Ảnh</th>
            <th>Tiêu đề</th>
            <th>Slug</th>
            <th>Trạng thái tiles</th>
            <th>Thao tác</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in scenes" :key="s.id">
            <td>{{ s.id }}</td>
            <td>
              <img
                v-if="s.original_image_url"
                :src="s.original_image_url"
                class="thumb"
                alt=""
              />
              <span v-else class="no-image">—</span>
            </td>
            <td class="title-cell">{{ s.title }}</td>
            <td><code>{{ s.slug }}</code></td>
            <td>
              <span :class="`status status-${s.tiles_status || 'pending'}`">
                {{ statusLabel(s.tiles_status) }}
              </span>
            </td>
            <td class="actions-cell">
              <label class="upload-btn">
                📤 Upload ảnh
                <input
                  type="file"
                  accept="image/jpeg,image/png,image/jpg"
                  @change="uploadImage(s, $event)"
                  hidden
                />
              </label>
            </td>
          </tr>
        </tbody>
      </table>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/lib/api'

const router = useRouter()

const scenes = ref([])
const loading = ref(true)
const error = ref('')
const user = ref(null)

onMounted(async () => {
  // Lấy thông tin user từ localStorage
  try {
    const u = localStorage.getItem('admin_user')
    if (u) user.value = JSON.parse(u)
  } catch (e) {}

  await loadScenes()
})

async function loadScenes() {
  loading.value = true
  error.value = ''

  try {
    const { data } = await api.get('/admin/scenes')
    // Hỗ trợ cả 2 dạng response: { data: [...] } hoặc { data: { data: [...] } }
    const list = data.data?.data || data.data || []
    scenes.value = list
  } catch (e) {
    console.error('Load scenes error:', e)

    if (e.response?.status === 401) {
      router.push({ name: 'login' })
      return
    }

    if (e.response?.status === 403) {
      error.value = 'Bạn không có quyền truy cập trang này.'
    } else if (e.response?.status === 404) {
      error.value = 'API không tồn tại. Kiểm tra backend đã chạy chưa.'
    } else if (e.code === 'ERR_NETWORK') {
      error.value = 'Không kết nối được Backend. Kiểm tra Docker đã chạy chưa.'
    } else {
      error.value = e.response?.data?.message || 'Lỗi không xác định: ' + e.message
    }
  } finally {
    loading.value = false
  }
}

async function uploadImage(scene, event) {
  const file = event.target.files[0]
  if (!file) return

  // Kiểm tra dung lượng (tối đa 50MB)
  if (file.size > 50 * 1024 * 1024) {
    alert('File quá lớn. Tối đa 50MB.')
    event.target.value = ''
    return
  }

  const formData = new FormData()
  formData.append('image', file)

  try {
    const { data } = await api.post(`/admin/scenes/${scene.id}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    alert('✅ Upload thành công!\n\n' +
          'Bước tiếp theo: chạy lệnh sau trong Git Bash để xử lý tiles:\n' +
          `docker compose exec app php artisan scene:generate-tiles ${scene.id}`)

    await loadScenes()
  } catch (e) {
    console.error('Upload error:', e)
    alert('❌ Lỗi upload: ' + (e.response?.data?.message || e.message))
  } finally {
    event.target.value = ''
  }
}

async function logout() {
  try {
    await api.post('/logout')
  } catch (e) {
    // Bỏ qua lỗi
  }

  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push({ name: 'login' })
}

function statusLabel(status) {
  return {
    pending: 'Chờ xử lý',
    processing: 'Đang xử lý',
    done: 'Hoàn thành',
    failed: 'Thất bại',
  }[status] || status || 'Chờ xử lý'
}
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  background: #0a0e14;
  color: white;
}

/* ===== Header ===== */
.admin-header {
  background: linear-gradient(135deg, rgba(28, 114, 147, 0.3), rgba(20, 85, 110, 0.3));
  border-bottom: 1px solid rgba(79, 179, 217, 0.2);
  padding: 20px 40px;
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(10px);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo {
  font-size: 36px;
}

.admin-header h1 {
  margin: 0;
  color: #4fb3d9;
  font-size: 22px;
}

.subtitle {
  margin: 4px 0 0;
  color: #888;
  font-size: 13px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  color: #b0b0b0;
  font-size: 14px;
}

.btn-logout {
  background: rgba(220, 53, 69, 0.9);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.btn-logout:hover {
  background: #dc3545;
}

/* ===== Container ===== */
.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 40px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.toolbar h2 {
  margin: 0;
  font-size: 20px;
  color: #e8edf3;
}

.btn-refresh {
  background: rgba(28, 114, 147, 0.3);
  color: #4fb3d9;
  border: 1px solid rgba(79, 179, 217, 0.4);
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.btn-refresh:hover {
  background: rgba(28, 114, 147, 0.5);
}

/* ===== Loading ===== */
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 80px 0;
  color: #888;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.15);
  border-top-color: #4fb3d9;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* ===== Error / Empty ===== */
.error-box,
.empty-box {
  padding: 60px 20px;
  text-align: center;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #b0b0b0;
}

.error-box {
  background: rgba(220, 53, 69, 0.1);
  border-color: rgba(220, 53, 69, 0.3);
  color: #ff6b6b;
}

.error-box button {
  margin-top: 16px;
  background: #dc3545;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
}

/* ===== Table ===== */
.data-table {
  width: 100%;
  border-collapse: collapse;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.data-table th,
.data-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  vertical-align: middle;
}

.data-table th {
  background: rgba(28, 114, 147, 0.25);
  font-weight: 600;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #4fb3d9;
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.03);
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.title-cell {
  font-weight: 500;
}

.data-table code {
  background: rgba(0, 0, 0, 0.4);
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 12px;
  color: #4fb3d9;
  font-family: 'Consolas', 'Monaco', monospace;
}

.thumb {
  width: 80px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.no-image {
  color: #555;
  font-size: 12px;
}

/* ===== Status badge ===== */
.status {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.status-pending {
  background: rgba(108, 117, 125, 0.3);
  color: #adb5bd;
}

.status-processing {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.status-done {
  background: rgba(40, 167, 69, 0.2);
  color: #4ade80;
}

.status-failed {
  background: rgba(220, 53, 69, 0.2);
  color: #ff6b6b;
}

/* ===== Actions ===== */
.actions-cell {
  white-space: nowrap;
}

.upload-btn {
  display: inline-block;
  padding: 8px 16px;
  background: rgba(28, 114, 147, 0.3);
  color: #4fb3d9;
  border: 1px solid rgba(79, 179, 217, 0.4);
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  transition: background 0.2s;
}

.upload-btn:hover {
  background: rgba(28, 114, 147, 0.5);
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .admin-header {
    padding: 16px 20px;
  }

  .container {
    padding: 20px;
  }

  .data-table {
    font-size: 14px;
  }

  .data-table th,
  .data-table td {
    padding: 10px 12px;
  }

  .thumb {
    width: 60px;
    height: 40px;
  }
}
</style>
