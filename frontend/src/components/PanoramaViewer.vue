<template>
  <div class="panorama-wrapper">
    <div ref="viewerEl" class="panorama-viewer"></div>

    <!-- Loading -->
    <div v-if="loading" class="loading-overlay">
      <div class="spinner"></div>
      <p>Đang tải không gian tham quan...</p>
    </div>

    <!-- Error -->
    <div v-if="error" class="error-overlay">
      <p>⚠ {{ error }}</p>
    </div>

    <!-- Scene title -->
    <div v-if="scene" class="controls-overlay">
      <div class="scene-title">{{ scene.title }}</div>
    </div>

    <!-- Hotspot panel -->
    <transition name="slide-up">
      <div v-if="activeHotspot" class="hotspot-panel">
        <button class="close-btn" @click="activeHotspot = null">✕</button>
        <h3>{{ activeHotspot.title }}</h3>
        <div class="content" v-html="sanitize(activeHotspot.content)"></div>

        <div v-if="activeHotspot.artifact" class="artifact-card">
          <img v-if="activeHotspot.artifact.image_url"
               :src="activeHotspot.artifact.image_url"
               :alt="activeHotspot.artifact.name"
               @error="$event.target.style.display='none'" />
          <div class="artifact-info">
            <h4>{{ activeHotspot.artifact.name }}</h4>
            <p v-if="activeHotspot.artifact.era">Thời kỳ: {{ activeHotspot.artifact.era }}</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import 'pannellum/build/pannellum.js'
import { sceneApi, logApi } from '@/lib/api'
import { useSession } from '@/composables/useSession'

const props = defineProps({
  sceneSlug: { type: String, required: true },
})

const emit = defineEmits(['scene-change', 'hotspot-click'])

const { sessionId } = useSession()

const viewerEl = ref(null)
const viewer = ref(null)
const scene = ref(null)
const loading = ref(true)
const error = ref(null)
const activeHotspot = ref(null)

let enterTime = Date.now()

async function loadScene(slug) {
  if (!slug) return
  loading.value = true
  error.value = null

  // Log thời gian dừng ở scene cũ
  if (scene.value) {
    const duration = Math.round((Date.now() - enterTime) / 1000)
    logAction('view', null, duration)
  }

  try {
    const { data } = await sceneApi.get(slug)
    scene.value = data.data

    if (viewer.value) {
      try { viewer.value.destroy() } catch (e) {}
    }

    await nextTick()

    const config = buildConfig(data.data)

    // Pannellum là UMD module, phải dùng window.pannellum
    if (!window.pannellum) {
      throw new Error('Pannellum chưa được load')
    }

    viewer.value = window.pannellum.viewer(viewerEl.value, config)

    enterTime = Date.now()
    logAction('view', null, 0)
  } catch (err) {
    console.error('Lỗi tải scene:', err)
    error.value = 'Không tải được không gian tham quan: ' + err.message
  } finally {
    loading.value = false
  }
}

function buildConfig(sceneData) {
  const pano = sceneData.panorama

  const sceneConfig = {
    title: sceneData.title,
    type: pano.type,
    hfov: pano.initialHfov || 100,
    pitch: pano.initialPitch || 0,
    yaw: pano.initialYaw || 0,
    hotSpots: (sceneData.hotspots || []).map(h => ({
      id: `hs-${h.id}`,
      pitch: h.pitch,
      yaw: h.yaw,
      type: h.type === 'scene' ? 'scene' : 'info',
      text: h.title,
      sceneId: h.target_scene?.slug || undefined,
      CSSclass: `hotspot hotspot-${h.type}`,
      clickHandlerFunc: () => handleHotspotClick(h),
    })),
    autoLoad: true,
  }

  if (pano.type === 'multires') {
    sceneConfig.multiRes = {
      path: pano.path,
      fallbackPath: pano.fallbackPath,
      extension: pano.extension || 'jpg',
      tileResolution: pano.tileResolution || 512,
      maxLevel: pano.maxLevel || 3,
      cubeResolution: pano.cubeResolution || 4096,
    }
  } else {
    sceneConfig.panorama = pano.panorama
  }

  return {
    default: {
      firstScene: sceneData.slug,
      sceneFadeDuration: 800,
      autoLoad: true,
      showControls: true,
      compass: true,
    },
    scenes: {
      [sceneData.slug]: sceneConfig,
    },
  }
}

function handleHotspotClick(hotspot) {
  emit('hotspot-click', hotspot)
  logAction('hotspot_click', hotspot.id, 0)

  if (hotspot.type === 'scene' && hotspot.target_scene) {
    logAction('scene_change', null, 0)
    emit('scene-change', hotspot.target_scene.slug)
  } else {
    activeHotspot.value = hotspot
  }
}

async function logAction(action, hotspotId = null, duration = 0) {
  if (!scene.value) return
  try {
    await logApi.send({
      scene_id: scene.value.id,
      action,
      hotspot_id: hotspotId,
      duration_seconds: duration,
      session_id: sessionId.value,
    })
  } catch (e) {
    console.warn('Log failed:', e.message)
  }
}

function sanitize(html) {
  if (!html) return ''
  return html
    .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
    .replace(/on\w+="[^"]*"/gi, '')
    .replace(/on\w+='[^']*'/gi, '')
}

watch(() => props.sceneSlug, (newSlug) => {
  if (newSlug) loadScene(newSlug)
})

onMounted(() => {
  loadScene(props.sceneSlug)
})

onUnmounted(() => {
  if (viewer.value) {
    try { viewer.value.destroy() } catch (e) {}
  }
})
</script>

<style scoped>
.panorama-wrapper {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  background: #000;
}
.panorama-viewer {
  width: 100%;
  height: 100%;
}
.loading-overlay, .error-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  z-index: 100;
  gap: 20px;
}
.error-overlay { background: rgba(139, 0, 0, 0.9); }
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.controls-overlay {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 50;
}
.scene-title {
  background: rgba(0, 0, 0, 0.65);
  color: white;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.hotspot-panel {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  max-height: 45%;
  overflow-y: auto;
  background: rgba(20, 20, 25, 0.96);
  color: white;
  padding: 24px;
  z-index: 60;
  backdrop-filter: blur(20px);
  border-top: 3px solid #1C7293;
}
.hotspot-panel h3 {
  margin: 0 0 12px 0;
  color: #4FB3D9;
  font-size: 22px;
}
.hotspot-panel .content {
  line-height: 1.6;
  color: #d0d0d0;
  font-size: 15px;
}
.close-btn {
  position: absolute;
  top: 12px;
  right: 16px;
  background: transparent;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  opacity: 0.7;
}
.close-btn:hover { opacity: 1; }
.artifact-card {
  display: flex;
  gap: 16px;
  margin-top: 20px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.12);
}
.artifact-card img {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 8px;
}
.artifact-info h4 { margin: 0 0 8px 0; color: #fff; }
.artifact-info p { margin: 0; color: #a0a0a0; font-size: 14px; }

.slide-up-enter-active, .slide-up-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}
.slide-up-enter-from, .slide-up-leave-to {
  transform: translateY(100%);
  opacity: 0;
}
</style>

<style>
.hotspot { cursor: pointer; transition: transform 0.2s; }
.hotspot:hover { transform: scale(1.15); }
.hotspot-info {
  width: 42px; height: 42px;
  background: rgba(28, 114, 147, 0.95);
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
}
.hotspot-scene {
  width: 52px; height: 52px;
  background: rgba(255, 193, 7, 0.95);
  border: 3px solid white;
  border-radius: 50%;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
  animation: pulse 2s infinite;
}
.hotspot-artifact {
  width: 46px; height: 46px;
  background: rgba(184, 80, 66, 0.95);
  border: 3px solid white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
}
@keyframes pulse {
  0%, 100% { box-shadow: 0 2px 12px rgba(0,0,0,0.5), 0 0 0 0 rgba(255,193,7,0.7); }
  50% { box-shadow: 0 2px 12px rgba(0,0,0,0.5), 0 0 0 15px rgba(255,193,7,0); }
}
</style>
