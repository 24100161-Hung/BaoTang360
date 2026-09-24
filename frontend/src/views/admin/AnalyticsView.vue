<template>
  <div class="analytics">
    <h1>Phân tích hành vi</h1>
    <p class="subtitle">Dữ liệu từ mô-đun Python</p>

    <div class="stats-grid">
      <div class="stat-card">
        <h3>{{ stats.total_sessions || 0 }}</h3>
        <p>Phiên tham quan</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.total_actions || 0 }}</h3>
        <p>Tổng hành động</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.total_hotspot_clicks || 0 }}</h3>
        <p>Click điểm nóng</p>
      </div>
      <div class="stat-card">
        <h3>{{ stats.total_audio_plays || 0 }}</h3>
        <p>Lượt nghe audio</p>
      </div>
    </div>

    <div v-if="dropOff.length" class="section">
      <h2>Cảnh báo điểm bỏ dở</h2>
      <table>
        <thead>
          <tr>
            <th>Scene</th>
            <th>Phiên</th>
            <th>Tỷ lệ thoát</th>
            <th>Engagement</th>
            <th>Trạng thái</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in dropOff" :key="s.scene_id">
            <td>{{ s.scene_title }}</td>
            <td>{{ s.unique_sessions }}</td>
            <td>{{ (s.exit_rate * 100).toFixed(1) }}%</td>
            <td>{{ (s.engagement_score * 100).toFixed(1) }}%</td>
            <td>
              <span v-if="s.is_drop_off" class="badge danger">⚠ Cần cải thiện</span>
              <span v-else class="badge ok">✓ Tốt</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/lib/api'

const stats = ref({})
const dropOff = ref([])

onMounted(async () => {
  try {
    const [statsRes, dropRes] = await Promise.all([
      api.get('/v1/admin/analytics/visitor-stats'),
      api.get('/v1/admin/analytics/drop-off'),
    ])
    stats.value = statsRes.data.data
    dropOff.value = dropRes.data.data
  } catch (e) {
    console.error(e)
  }
})
</script>

<style scoped>
.analytics h1 { margin: 0 0 8px; }
.subtitle { color: #888; margin: 0 0 32px; }
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}
.stat-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
}
.stat-card h3 {
  font-size: 32px;
  color: #4FB3D9;
  margin: 0 0 8px;
}
.stat-card p { color: #888; margin: 0; }
.section {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 24px;
}
.section h2 { margin: 0 0 20px; color: #4FB3D9; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
th { color: #888; font-size: 13px; text-transform: uppercase; }
.badge { padding: 4px 10px; border-radius: 12px; font-size: 12px; }
.badge.danger { background: #dc3545; }
.badge.ok { background: #28a745; }
</style>
