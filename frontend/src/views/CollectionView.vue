<template>
  <div class="collection-page">
    <header class="page-header">
      <div class="container">
        <router-link to="/" class="back-link">← Về trang chủ</router-link>
        <h1>📚 Bộ sưu tập của tôi</h1>
        <p>Lưu lại những hiện vật và không gian bạn yêu thích</p>
      </div>
    </header>

    <main class="container">
      <!-- Loading -->
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
      </div>

      <!-- Empty state -->
      <div v-else-if="!items.length" class="empty-state">
        <div class="empty-icon">📭</div>
        <h2>Bộ sưu tập trống</h2>
        <p>Hãy khám phá bảo tàng và lưu lại những gì bạn thích!</p>
        <router-link to="/tour/sanh-chinh" class="btn-primary">
          Bắt đầu tham quan →
        </router-link>
      </div>

      <!-- Grid of items -->
      <div v-else class="collection-grid">
        <div v-for="item in items" :key="item.id" class="collection-card">
          <!-- Artifact card -->
          <template v-if="item.artifact">
            <img
              v-if="item.artifact.image_url"
              :src="item.artifact.image_url"
              :alt="item.artifact.name"
              class="card-image"
            />
            <div class="card-body">
              <span class="card-type">🏺 Hiện vật</span>
              <h3>{{ item.artifact.name }}</h3>
              <p v-if="item.artifact.era" class="card-meta">
                {{ item.artifact.era }}
              </p>
              <p v-if="item.note" class="card-note">📝 {{ item.note }}</p>
              <button @click="removeItem(item.id)" class="btn-remove">
                🗑 Xóa khỏi bộ sưu tập
              </button>
            </div>
          </template>

          <!-- Scene card -->
          <template v-else-if="item.scene">
            <img
              :src="item.scene.original_image_url"
              :alt="item.scene.title"
              class="card-image"
            />
            <div class="card-body">
              <span class="card-type">🏛️ Không gian</span>
              <h3>{{ item.scene.title }}</h3>
              <p v-if="item.note" class="card-note">📝 {{ item.note }}</p>
              <div class="card-actions">
                <router-link
                  :to="`/tour/${item.scene.slug}`"
                  class="btn-view"
                >
                  Xem ngay
                </router-link>
                <button @click="removeItem(item.id)" class="btn-remove-small">
                  🗑
                </button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { collectionApi } from '@/lib/api'

const router = useRouter()
const items = ref([])
const loading = ref(true)

onMounted(async () => {
  await loadCollection()
})

async function loadCollection() {
  loading.value = true
  try {
    const { data } = await collectionApi.list()
    items.value = data.data
  } catch (e) {
    console.error('Không tải được bộ sưu tập:', e)
    if (e.response?.status === 401) {
      router.push({ name: 'login', query: { redirect: '/collection' } })
    }
  } finally {
    loading.value = false
  }
}

async function removeItem(id) {
  if (!confirm('Xóa mục này khỏi bộ sưu tập?')) return
  try {
    await collectionApi.remove(id)
    items.value = items.value.filter((i) => i.id !== id)
  } catch (e) {
    alert('Không xóa được: ' + (e.response?.data?.message || e.message))
  }
}
</script>

<style scoped>
.collection-page {
  min-height: 100vh;
  background: #0a0e14;
  color: white;
}

.page-header {
  background: linear-gradient(135deg, #1c7293, #14556e);
  padding: 60px 20px 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.back-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  color: white;
}

.page-header h1 {
  margin: 12px 0 8px;
  font-size: 36px;
}

.page-header p {
  opacity: 0.9;
  margin: 0;
}

main.container {
  padding: 40px 20px;
}

.loading {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top-color: #4fb3d9;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.empty-state h2 {
  color: #4fb3d9;
  margin-bottom: 12px;
}

.empty-state p {
  color: #888;
  margin-bottom: 32px;
}

.btn-primary {
  display: inline-block;
  background: #1c7293;
  color: white;
  padding: 14px 32px;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

.collection-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.collection-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.2s;
}

.collection-card:hover {
  transform: translateY(-4px);
}

.card-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.card-body {
  padding: 20px;
}

.card-type {
  font-size: 12px;
  color: #4fb3d9;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
}

.card-body h3 {
  margin: 8px 0;
  font-size: 18px;
}

.card-meta {
  color: #888;
  font-size: 14px;
  margin: 4px 0;
}

.card-note {
  color: #b0b0b0;
  font-size: 14px;
  margin: 12px 0;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 6px;
  border-left: 3px solid #4fb3d9;
}

.btn-remove {
  width: 100%;
  padding: 10px;
  background: rgba(220, 53, 69, 0.15);
  color: #ff6b6b;
  border: 1px solid rgba(220, 53, 69, 0.3);
  border-radius: 8px;
  cursor: pointer;
  margin-top: 12px;
  font-size: 14px;
}

.btn-remove:hover {
  background: rgba(220, 53, 69, 0.3);
}

.card-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.btn-view {
  flex: 1;
  text-align: center;
  padding: 10px;
  background: #1c7293;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.btn-remove-small {
  width: 40px;
  padding: 10px;
  background: rgba(220, 53, 69, 0.15);
  color: #ff6b6b;
  border: 1px solid rgba(220, 53, 69, 0.3);
  border-radius: 8px;
  cursor: pointer;
}
</style>
