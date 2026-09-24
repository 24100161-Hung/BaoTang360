<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="logo">
        <h2>Bảo tàng 360</h2>
        <p>{{ user?.full_name }}</p>
      </div>

      <nav>
            <nav>
        <router-link to="/admin" exact-active-class="active">
          📊 Dashboard
        </router-link>
        <router-link to="/admin/scenes" active-class="active">
          🖼 Quản lý Scenes
        </router-link>
        <router-link to="/admin/analytics" active-class="active">
          📈 Phân tích hành vi
        </router-link>
      </nav>
        <router-link to="/admin" exact-active-class="active">
          📊 Dashboard
        </router-link>
        <router-link to="/admin/scenes" active-class="active">
          🖼 Quản lý Scenes
        </router-link>
      </nav>

      <div class="footer">
        <router-link to="/" target="_blank">🌐 Xem trang chủ</router-link>
        <button @click="logout">🚪 Đăng xuất</button>
      </div>
    </aside>

    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { authStore } from '@/lib/auth'
import { authApi } from '@/lib/api'

const router = useRouter()
const user = computed(() => authStore.user.value)

async function logout() {
  try {
    await authApi.logout()
  } catch (e) {}
  authStore.clear()
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: #0a0e14;
  color: white;
}
.sidebar {
  width: 260px;
  background: rgba(20, 20, 30, 0.95);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 24px 0;
  display: flex;
  flex-direction: column;
}
.logo {
  padding: 0 24px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.logo h2 {
  margin: 0 0 4px;
  color: #4FB3D9;
  font-size: 18px;
}
.logo p {
  margin: 0;
  color: #888;
  font-size: 13px;
}
nav {
  flex: 1;
  padding: 24px 0;
}
nav a {
  display: block;
  padding: 12px 24px;
  color: #ccc;
  text-decoration: none;
  font-size: 15px;
  transition: background 0.2s;
}
nav a:hover { background: rgba(255, 255, 255, 0.05); }
nav a.active {
  background: rgba(28, 114, 147, 0.3);
  border-left: 3px solid #4FB3D9;
  color: #4FB3D9;
}
.footer {
  padding: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.footer a, .footer button {
  color: #ccc;
  text-decoration: none;
  font-size: 14px;
  padding: 8px 0;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
}
.footer a:hover, .footer button:hover { color: #4FB3D9; }
.content {
  flex: 1;
  padding: 32px;
  overflow-y: auto;
}
</style>
