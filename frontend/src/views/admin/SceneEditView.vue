<template>
  <div class="scene-edit">
    <div v-if="loading">Đang tải...</div>

    <div v-else-if="scene">
      <header>
        <div>
          <h1>{{ scene.title }}</h1>
          <p class="subtitle">Chỉnh sửa thông tin và quản lý điểm nóng</p>
        </div>
        <router-link to="/admin/scenes" class="btn-back">← Quay lại</router-link>
      </header>

      <!-- Form thông tin -->
      <section class="section">
        <h2>Thông tin cơ bản</h2>
        <div class="form-grid">
          <div class="field">
            <label>Tiêu đề</label>
            <input v-model="form.title" type="text" />
          </div>
          <div class="field">
            <label>Slug</label>
            <input v-model="form.slug" type="text" disabled />
          </div>
          <div class="field full">
            <label>Mô tả</label>
            <textarea v-model="form.description" rows="3"></textarea>
          </div>
          <div class="field">
            <label>Pitch ban đầu</label>
            <input v-model.number="form.initial_pitch" type="number" step="0.1" />
          </div>
          <div class="field">
            <label>Yaw ban đầu</label>
            <input v-model.number="form.initial_yaw" type="number" step="0.1" />
          </div>
          <div class="field">
            <label>HFOV ban đầu</label>
            <input v-model.number="form.initial_hfov" type="number" step="1" />
          </div>
          <div class="field">
            <label>Thứ tự hiển thị</label>
            <input v-model.number="form.default_order" type="number" />
          </div>
        </div>
        <button class="btn-primary" @click="saveScene">Lưu thay đổi</button>
      </section>

      <!-- Hotspots -->
      <section class="section">
        <div class="section-header">
          <h2>Điểm nóng ({{ hotspots.length }})</h2>
          <button class="btn-primary" @click="showHotspotModal = true">+ Thêm điểm nóng</button>
        </div>

        <div v-if="hotspots.length === 0" class="empty">
          Chưa có điểm nóng nào.
        </div>

        <table v-else class="hotspot-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Loại</th>
              <th>Tiêu đề</th>
              <th>Pitch/Yaw</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="h in hotspots" :key="h.id">
              <td>{{ h.id }}</td>
              <td><span :class="`badge badge-${h.type}`">{{ h.type }}</span></td>
              <td>{{ h.title }}</td>
              <td>{{ h.pitch.toFixed(1) }} / {{ h.yaw.toFixed(1) }}</td>
              <td>
                <button @click="deleteHotspot(h)" class="danger">🗑</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>

    <!-- Modal thêm hotspot -->
    <div v-if="showHotspotModal" class="modal-overlay" @click.self="showHotspotModal = false">
      <div class="modal">
        <h2>Thêm điểm nóng</h2>
        <form @submit.prevent="createHotspot">
          <div class="field">
            <label>Loại</label>
            <select v-model="newHotspot.type">
              <option value="info">Thông tin (info)</option>
              <option value="scene">Chuyển cảnh (scene)</option>
              <option value="artifact">Hiện vật (artifact)</option>
            </select>
          </div>
          <div class="form-grid">
            <div class="field">
              <label>Pitch (-90 đến 90)</label>
              <input v-model.number="newHotspot.pitch" type="number" step="0.1" required />
            </div>
            <div class="field">
              <label>Yaw (-180 đến 180)</label>
              <input v-model.number="newHotspot.yaw" type="number" step="0.1" required />
            </div>
          </div>
          <div class="field">
            <label>Tiêu đề</label>
            <input v-model="newHotspot.title" type="text" required />
          </div>
          <div class="field">
            <label>Nội dung</label>
            <textarea v-model="newHotspot.content" rows="3"></textarea>
          </div>
          <div v-if="newHotspot.type === 'scene'" class="field">
            <label>Scene đích</label>
            <select v-model.number="newHotspot.target_scene_id" required>
              <option :value="null">-- Chọn scene --</option>
              <option v-for="s in allScenes" :key="s.id" :value="s.id">
                {{ s.title }}
              </option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" @click="showHotspotModal = false">Hủy</button>
            <button type="submit" class="btn-primary">Tạo</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { adminApi } from '@/lib/api'

const route = useRoute()
const sceneId = route.params.id

const scene = ref(null)
const hotspots = ref([])
const allScenes = ref([])
const loading = ref(true)
const showHotspotModal = ref(false)

const form = ref({})
const newHotspot = ref({
  type: 'info', pitch: 0, yaw: 0, title: '', content: '', target_scene_id: null,
})

onMounted(async () => {
  try {
    const [sceneRes, hotspotsRes, scenesRes] = await Promise.all([
      adminApi.scenes.get(sceneId),
      adminApi.hotspots.list(sceneId),
      adminApi.scenes.list({ per_page: 100 }),
    ])
    scene.value = sceneRes.data.data
    form.value = { ...scene.value }
    hotspots.value = hotspotsRes.data.data
    allScenes.value = scenesRes.data.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
})

async function saveScene() {
  try {
    await adminApi.scenes.update(sceneId, form.value)
    alert('Đã lưu!')
  } catch (e) {
    alert('Lỗi: ' + (e.response?.data?.message || e.message))
  }
}

async function createHotspot() {
  try {
    await adminApi.hotspots.create(sceneId, newHotspot.value)
    showHotspotModal.value = false
    newHotspot.value = { type: 'info', pitch: 0, yaw: 0, title: '', content: '', target_scene_id: null }
    const { data } = await adminApi.hotspots.list(sceneId)
    hotspots.value = data.data
  } catch (e) {
    alert('Lỗi: ' + (e.response?.data?.message || e.message))
  }
}

async function deleteHotspot(h) {
  if (!confirm(`Xóa điểm nóng "${h.title}"?`)) return
  await adminApi.hotspots.delete(h.id)
  const { data } = await adminApi.hotspots.list(sceneId)
  hotspots.value = data.data
}
</script>

<style scoped>
.scene-edit h1 { margin: 0 0 8px; font-size: 28px; }
header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}
.subtitle { color: #888; margin: 0; }
.btn-back {
  color: #4FB3D9;
  text-decoration: none;
  padding: 10px 16px;
  border-radius: 6px;
  border: 1px solid #4FB3D9;
}
.section {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.section h2 { margin: 0 0 20px; font-size: 20px; color: #4FB3D9; }
.section-header h2 { margin: 0; }
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}
.field.full { grid-column: 1 / -1; }
.field label {
  display: block;
  margin-bottom: 6px;
  color: #aaa;
  font-size: 13px;
}
.field input, .field textarea, .field select {
  width: 100%;
  padding: 10px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  color: white;
  font-size: 14px;
  font-family: inherit;
}
.btn-primary {
  background: #1C7293;
  color: white;
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}
.empty { padding: 20px; text-align: center; color: #666; }
.hotspot-table {
  width: 100%;
  border-collapse: collapse;
}
.hotspot-table th, .hotspot-table td {
  padding: 10px 12px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}
.badge {
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 11px;
  text-transform: uppercase;
}
.badge-info { background: #1C7293; }
.badge-scene { background: #ffc107; color: black; }
.badge-artifact { background: #B85042; }
.danger { background: #dc3545; color: white; border: none; padding: 6px 10px; border-radius: 4px; cursor: pointer; }
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
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}
.modal h2 { margin: 0 0 24px; }
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
