<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    <p class="subtitle">Tổng quan hệ thống Bảo tàng ảo 360°</p>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">🖼</div>
        <div class="stat-info">
          <h3>{{ stats.total_scenes }}</h3>
          <p>Tổng số scenes</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <h3>{{ stats.done_tiles }}</h3>
          <p>Tiles đã xử lý</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <h3>{{ stats.pending_tiles }}</h3>
          <p>Chờ xử lý</p>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon">📍</div>
        <div class="stat-info">
          <h3>{{ stats.total_hotspots }}</h3>
          <p>Điểm nóng</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { adminApi } from '@/lib/api'

const stats = ref({
  total_scenes: 0,
  done_tiles: 0,
  pending_tiles: 0,
  total_hotspots: 0,
})

onMounted(async () => {
  try {
    const { data } = await adminApi.scenes.list({ per_page: 100 })
    const scenes = data.data
    stats.value.total_scenes = data.total || scenes.length
    stats.value.done_tiles = scenes.filter(s => s.tiles_status === 'done').length
    stats.value.pending_tiles = scenes.filter(s => s.tiles_status !== 'done').length
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.dashboard h1 {
  margin: 0 0 8px;
  font-size: 28px;
}
.subtitle {
  color: #888;
  margin: 0 0 32px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}
.stat-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat-icon {
  font-size: 32px;
  width: 60px;
  height: 60px;
  background: rgba(28, 114, 147, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.stat-info h3 {
  margin: 0 0 4px;
  font-size: 28px;
  color: #4FB3D9;
}
.stat-info p {
  margin: 0;
  color: #888;
  font-size: 14px;
}
</style>
