<template>
  <div class="theme-tour">
    <!-- Loading state -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Đang tải tour...</p>
    </div>

    <!-- Tour info header -->
    <header v-else-if="tour" class="tour-header">
      <div class="container">
        <router-link to="/" class="back-link">← Về trang chủ</router-link>
        <h1>{{ tour.title }}</h1>
        <p class="description">{{ tour.description }}</p>
        <div class="meta">
          <span>📍 {{ tour.steps.length }} điểm dừng</span>
          <span>⏱ {{ tour.duration }} phút</span>
          <span>🎯 {{ difficultyLabel(tour.difficulty) }}</span>
        </div>
      </div>
    </header>

    <!-- Panorama viewer in tour mode -->
    <div v-if="currentSceneSlug" class="viewer-container">
      <PanoramaViewer
        :scene-slug="currentSceneSlug"
        :tour-mode="true"
        :tour-steps="tourSteps"
        :initial-step="currentStep"
        @scene-change="onSceneChange"
        @exit-tour="exitTour"
      />
    </div>

    <!-- Step list sidebar -->
    <aside v-if="tour" class="steps-panel">
      <h3>Các bước tham quan</h3>
      <ol class="steps-list">
        <li
          v-for="(step, idx) in tour.steps"
          :key="idx"
          :class="{ active: idx === currentStep, done: idx < currentStep }"
          @click="jumpToStep(idx)"
        >
          <span class="step-number">{{ idx + 1 }}</span>
          <div class="step-info">
            <strong>{{ step.scene_title }}</strong>
            <p v-if="step.narration">{{ step.narration }}</p>
          </div>
        </li>
      </ol>

      <div class="legend">
        <p><span class="dot active-dot"></span> Đang xem</p>
        <p><span class="dot done-dot"></span> Đã xem</p>
      </div>
    </aside>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PanoramaViewer from '@/components/PanoramaViewer.vue'
import { tourApi } from '@/lib/api'

const route = useRoute()
const router = useRouter()

const tour = ref(null)
const loading = ref(true)
const currentStep = ref(0)
const currentSceneSlug = ref('')

const tourSteps = ref([])

onMounted(async () => {
  await loadTour()
})

watch(
  () => route.params.slug,
  async () => {
    await loadTour()
  }
)

async function loadTour() {
  loading.value = true
  try {
    const { data } = await tourApi.get(route.params.slug)
    tour.value = data.data
    tourSteps.value = data.data.steps.map((s) => s.scene_slug)
    currentStep.value = 0
    currentSceneSlug.value = tourSteps.value[0]
  } catch (e) {
    console.error('Không tải được tour:', e)
    router.push({ name: 'not-found' })
  } finally {
    loading.value = false
  }
}

function onSceneChange(slug) {
  currentSceneSlug.value = slug
  const idx = tourSteps.value.indexOf(slug)
  if (idx !== -1) {
    currentStep.value = idx
  }
}

function jumpToStep(idx) {
  currentStep.value = idx
  currentSceneSlug.value = tourSteps.value[idx]
}

function exitTour() {
  router.push({ name: 'home' })
}

function difficultyLabel(d) {
  return { easy: 'Dễ', medium: 'Trung bình', hard: 'Khó' }[d] || 'Dễ'
}
</script>

<style scoped>
.theme-tour {
  position: relative;
  min-height: 100vh;
  background: #0a0e14;
  color: white;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.2);
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

.tour-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 30;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.85), transparent);
  padding: 20px;
  pointer-events: none;
}

.tour-header .container {
  max-width: 800px;
  margin: 0 auto;
  pointer-events: auto;
}

.back-link {
  color: #4fb3d9;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  text-decoration: underline;
}

.tour-header h1 {
  margin: 8px 0;
  font-size: 28px;
  color: #4fb3d9;
}

.description {
  color: #b0b0b0;
  margin: 8px 0;
  line-height: 1.5;
}

.meta {
  display: flex;
  gap: 20px;
  font-size: 14px;
  color: #888;
  margin-top: 12px;
}

.viewer-container {
  width: 100%;
  height: 100vh;
}

.steps-panel {
  position: absolute;
  top: 120px;
  right: 20px;
  width: 320px;
  max-height: calc(100vh - 160px);
  overflow-y: auto;
  background: rgba(20, 20, 25, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 12px;
  padding: 20px;
  z-index: 25;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.steps-panel h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #4fb3d9;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.steps-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.steps-list li {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 6px;
}

.steps-list li:hover {
  background: rgba(255, 255, 255, 0.05);
}

.steps-list li.active {
  background: rgba(28, 114, 147, 0.3);
  border-left: 3px solid #4fb3d9;
}

.steps-list li.done {
  opacity: 0.6;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
}

.steps-list li.active .step-number {
  background: #4fb3d9;
  color: #0a0e14;
}

.steps-list li.done .step-number::after {
  content: '✓';
}

.steps-list li.done .step-number {
  color: transparent;
  font-size: 0;
}

.steps-list li.done .step-number::after {
  font-size: 14px;
  color: #4fb3d9;
}

.step-info {
  flex: 1;
}

.step-info strong {
  font-size: 14px;
  display: block;
  margin-bottom: 4px;
}

.step-info p {
  font-size: 12px;
  color: #888;
  margin: 0;
  line-height: 1.4;
}

.legend {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 12px;
  color: #888;
}

.legend p {
  margin: 4px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.active-dot {
  background: #4fb3d9;
}

.done-dot {
  background: rgba(79, 179, 217, 0.4);
}

@media (max-width: 1024px) {
  .steps-panel {
    display: none;
  }
}
</style>
