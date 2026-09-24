<template>
  <div class="scene-list">
    <header>
      <div>
        <h1>Quản lý Scenes</h1>
        <p class="subtitle">Tổng {{ total }} không gian tham quan</p>
      </div>
      <button class="btn-primary" @click="showCreateModal = true">+ Thêm Scene mới</button>
    </header>

    <table class="scene-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Ảnh</th>
          <th>Tiêu đề</th>
          <th>Slug</th>
          <th>Tiles</th>
          <th>Thao tác</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in scenes" :key="s.id">
          <td>{{ s.id }}</td>
          <td>
            <img :src="s.original_image_url" class="thumb"
                 @error="$event.target.style.background='#333'" />
          </td>
          <td>{{ s.title }}</td>
          <td><code>{{ s.slug }}</code></td>
          <td>
            <span :class="`status status-${s.tiles_status}`">
              {{ s.tiles_status }}
            </span>
          </td>
          <td class="actions">
            <label class="upload-btn" title="Upload ảnh">
              📤 Upload
              <input type="file" accept="image/*" @change="uploadImage(s, $event)" hidden />
            </label>
            <button @click="generateTiles(s)" :disabled="s.tiles_status === 'processing'">
              🔄 {{ s.tiles_status === 'processing' ? 'Đang xử lý...' : 'Tiles' }}
            </button>
            <router-link :to="`/admin/scenes/${s.id}/edit`" class="edit-btn">
              ✏️ Sửa
            </router-link>
            <button @click="deleteScene(s)" class="danger">🗑</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal">
        <h2>Thêm Scene mới</h2>
        <form @submit.prevent="createScene">
          <div class="field">
            <label>Tiêu đề *</label>
            <input v-model="newScene.title" type="text" required />
          </div>
          <div class="field">
            <label>Mô tả</label>
            <textarea v-model="newScene.description" rows="3"></textarea>
          </div>
          <div class="field">
            <label>Slug (để trống sẽ tự sinh)</label>
            <input v-model="newScene.slug" type="text" placeholder="sanh-chinh" />
          </div>
          <div class="modal-actions">
            <button type="button" @click="showCreateModal = false">Hủy</button>
            <button type="submit" class="btn-primary">Tạo</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/lib/api'

const scenes = ref([])
const total = ref(0)
const showCreateModal = ref(false)
const newScene = ref({ title: '', description: '', slug: '' })

onMounted(loadScenes)

async function loadScenes() {
  const { data } = await adminApi.scenes.list({ per_page: 100 })
  scenes.value = data.data
  total.value = data.total
}

async function createScene() {
  await adminApi.scenes.create(newScene.value)
  showCreateModal.value = false
  newScene.value = { title: '', description: '', slug: '' }
  loadScenes()
}

async function uploadImage(scene, event) {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('image', file)

  try {
    await adminApi.scenes.uploadImage(scene.id, formData)
    alert('Upload thành công! Nhấn "Tiles" để xử lý.')
    loadScenes()
  } catch (e) {
    alert('Lỗi upload: ' + (e.response?.data?.message || e.message))
  }
}

async function generateTiles(scene) {
  if (!confirm(`Xử lý tiles cho "${scene.title}"? Có thể mất 1-2 phút.`)) return

  try {
    const { data } = await adminApi.scenes.generateTiles(scene.id)
    alert('Tiles đã tạo thành công!')
    loadScenes()
  } catch (e) {
    alert('Lỗi: ' + (e.response?.data?.message || e.message))
  }
}

async function deleteScene(scene) {
  if (!confirm(`Xóa "${scene.title}"?`)) return
  await adminApi.scenes.delete(scene.id)
  loadScenes()
}
</script>

<style scoped>
.scene-list h1 { margin: 0 0 8px; font-size: 28px; }
header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}
.subtitle { color: #888; margin: 0; }
.btn-primary {
  background: #1C7293;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}
.btn-primary:hover { background: #14556E; }
.scene-table {
  width: 100%;
  border-collapse: collapse;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  overflow: hidden;
}
.scene-table th, .scene-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.scene-table th {
  background: rgba(28, 114, 147, 0.2);
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
}
.thumb {
  width: 80px;
  height: 50px;
  object-fit: cover;
  border-radius: 4px;
  background: #333;
}
.status {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}
.status-pending { background: #6c757d; }
.status-processing { background: #ffc107; color: black; }
.status-done { background: #28a745; }
.status-failed { background: #dc3545; }
.actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.actions button, .upload-btn, .edit-btn {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.05);
  color: white;
  cursor: pointer;
  font-size: 13px;
  text-decoration: none;
}
.actions .danger { background: #dc3545; border-color: #dc3545; }
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.modal {
  background: #1a1e28;
  padding: 32px;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
}
.modal h2 { margin: 0 0 24px; }
.field { margin-bottom: 16px; }
.field label {
  display: block;
  margin-bottom: 6px;
  color: #aaa;
  font-size: 13px;
}
.field input, .field textarea {
  width: 100%;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  color: white;
  font-size: 14px;
  font-family: inherit;
}
.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}
.modal-actions button {
  padding: 10px 20px;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  background: transparent;
  color: white;
  cursor: pointer;
}
</style>
