<template>
  <div class="tour-page">
    <PanoramaViewer
      v-if="currentSlug"
      :scene-slug="currentSlug"
      @scene-change="onSceneChange"
    />

    <aside class="scene-sidebar" :class="{ collapsed: sidebarCollapsed }">
      <button class="toggle-btn" @click="sidebarCollapsed = !sidebarCollapsed">
        {{ sidebarCollapsed ? '☰' : '✕' }}
      </button>

      <div v-if="!sidebarCollapsed" class="sidebar-content">
        <h2>Không gian</h2>
        <ul class="scene-list">
          <li v-for="s in scenes" :key="s.id"
              :class="{ active: s.slug === currentSlug }"
              @click="currentSlug = s.slug">
            <img :src="s.thumb" :alt="s.title" class="thumb"
                 @error="$event.target.style.display='none'" />
            <span>{{ s.title }}</span>
          </li>
        </ul>
        <router-link to="/" class="back-link">← Về trang chủ</router-link>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PanoramaViewer from '@/components/PanoramaViewer.vue'
import { sceneApi } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const currentSlug = ref(route.params.slug || '')
const scenes = ref([])
const sidebarCollapsed = ref(false)

onMounted(async () => {
  try {
    const { data } = await sceneApi.list()
    scenes.value = data.data
  } catch (e) {
    console.error('Lỗi tải scenes:', e)
  }
})

watch(currentSlug, (v) => {
  if (v && v !== route.params.slug) {
    router.replace({ name: 'tour-view', params: { slug: v } })
  }
})

function onSceneChange(slug) {
  currentSlug.value = slug
}
</script>

<style scoped>
.tour-page { position: relative; height: 100vh; width: 100%; }
.scene-sidebar {
  position: absolute;
  top: 0; left: 0;
  width: 320px;
  height: 100%;
  background: rgba(20, 20, 25, 0.95);
  backdrop-filter: blur(20px);
  color: white;
  z-index: 40;
  transition: width 0.3s ease;
  overflow-y: auto;
}
.scene-sidebar.collapsed { width: 60px; }
.toggle-btn {
  width: 100%;
  background: transparent;
  border: none;
  color: white;
  font-size: 20px;
  padding: 16px;
  cursor: pointer;
}
.sidebar-content { padding: 16px; }
.sidebar-content h2 {
  font-size: 13px;
  text-transform: uppercase;
  color: #4FB3D9;
  margin: 0 0 12px 0;
  letter-spacing: 1px;
}
.scene-list { list-style: none; padding: 0; margin: 0; }
.scene-list li {
  display: flex;
  gap: 12px;
  padding: 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 4px;
  align-items: center;
}
.scene-list li:hover { background: rgba(255, 255, 255, 0.1); }
.scene-list li.active {
  background: rgba(28, 114, 147, 0.4);
  border-left: 3px solid #4FB3D9;
}
.thumb {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
  background: #333;
}
.back-link {
  display: block;
  margin-top: 24px;
  color: #999;
  text-decoration: none;
  font-size: 14px;
  padding: 8px;
}
.back-link:hover { color: #4FB3D9; }
</style>
