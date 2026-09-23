<template>
  <div class="home">
    <header class="hero">
      <h1>Bảo tàng ảo 360°</h1>
      <p>Khám phá di sản văn hóa mọi lúc, mọi nơi</p>
      <router-link v-if="firstScene" :to="`/tour/${firstScene.slug}`" class="btn-primary">
        Bắt đầu tham quan →
      </router-link>
    </header>

    <section class="scenes-section">
      <h2>Không gian tham quan</h2>
      <div v-if="loading" class="loading">Đang tải...</div>
      <div v-else-if="scenes.length === 0" class="loading">
        Chưa có không gian tham quan nào.
      </div>
      <div v-else class="scene-grid">
        <router-link v-for="s in scenes" :key="s.id"
                     :to="`/tour/${s.slug}`"
                     class="scene-card">
          <img :src="s.thumb" :alt="s.title"
               @error="$event.target.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 400 200%22%3E%3Crect fill=%22%23222%22 width=%22400%22 height=%22200%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 text-anchor=%22middle%22 fill=%22%23999%22 dy=%22.3em%22 font-family=%22sans-serif%22 font-size=%2218%22%3EẢnh 360°%3C/text%3E%3C/svg%3E'" />
          <div class="scene-info">
            <h3>{{ s.title }}</h3>
            <p>{{ s.description }}</p>
          </div>
        </router-link>
      </div>
    </section>

    <footer class="site-footer">
      <p>Học phần <strong>CSE703073</strong> - Lập trình ứng dụng web trong du lịch 2</p>
      <p>Nhóm 03 · Trường Công nghệ thông tin, Đại học Phenikaa</p>
      <p class="note">Sản phẩm học thuật - phục vụ mục đích đào tạo</p>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { sceneApi } from '@/lib/api'

const scenes = ref([])
const loading = ref(true)

const firstScene = computed(() => scenes.value[0] || null)

onMounted(async () => {
  try {
    const { data } = await sceneApi.list()
    scenes.value = data.data
  } catch (e) {
    console.error('Lỗi tải scenes:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home { min-height: 100vh; background: #0a0e14; color: white; }
.hero {
  text-align: center;
  padding: 100px 20px 60px;
  background: linear-gradient(135deg, #1C7293, #14556E);
}
.hero h1 { font-size: clamp(32px, 6vw, 64px); margin: 0 0 16px; }
.hero p { font-size: 20px; opacity: 0.9; margin-bottom: 32px; }
.btn-primary {
  display: inline-block;
  background: white;
  color: #14556E;
  padding: 14px 32px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }
.scenes-section { padding: 60px 40px; max-width: 1400px; margin: 0 auto; }
.scenes-section h2 { font-size: 32px; margin-bottom: 32px; }
.loading { text-align: center; padding: 40px; color: #999; }
.scene-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}
.scene-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  overflow: hidden;
  text-decoration: none;
  color: white;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.scene-card:hover { transform: translateY(-4px); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4); }
.scene-card img { width: 100%; height: 200px; object-fit: cover; display: block; }
.scene-info { padding: 20px; }
.scene-info h3 { margin: 0 0 8px; color: #4FB3D9; }
.scene-info p { color: #b0b0b0; margin: 0; line-height: 1.5; font-size: 14px; }
.site-footer {
  text-align: center;
  padding: 40px 20px;
  margin-top: 60px;
  border-top: 1px solid rgba(255,255,255,0.1);
  color: #888;
  font-size: 13px;
}
.site-footer p { margin: 4px 0; }
.site-footer .note { color: #666; font-style: italic; margin-top: 8px; }
</style>
