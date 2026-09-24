<template>
  <div class="login-page">
    <div class="login-box">
      <h1>Đăng nhập Admin</h1>
      <p class="subtitle">Bảo tàng ảo 360°</p>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>Email</label>
          <input v-model="form.email" type="email" required placeholder="admin@baotang.test" />
        </div>

        <div class="field">
          <label>Mật khẩu</label>
          <input v-model="form.password" type="password" required placeholder="••••••••" />
        </div>

        <div v-if="error" class="error">{{ error }}</div>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
        </button>
      </form>

      <router-link to="/" class="back-link">← Về trang chủ</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '@/lib/api'
import { authStore } from '@/lib/auth'

const router = useRouter()
const route = useRoute()

const form = ref({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    const { data } = await authApi.login(form.value)
    authStore.setAuth(data.token, data.user)
    router.push(route.query.redirect || '/admin')
  } catch (e) {
    error.value = e.response?.data?.message || 'Đăng nhập thất bại'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0e14, #1C7293);
}
.login-box {
  background: rgba(20, 20, 30, 0.95);
  padding: 40px;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
h1 {
  margin: 0 0 8px;
  color: white;
  font-size: 24px;
}
.subtitle {
  color: #4FB3D9;
  margin: 0 0 32px;
  font-size: 14px;
}
.field {
  margin-bottom: 20px;
}
.field label {
  display: block;
  color: #ccc;
  margin-bottom: 8px;
  font-size: 14px;
}
.field input {
  width: 100%;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: white;
  font-size: 15px;
}
.field input:focus {
  outline: none;
  border-color: #4FB3D9;
  background: rgba(255, 255, 255, 0.08);
}
.error {
  color: #ff6b6b;
  margin-bottom: 16px;
  padding: 10px;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 6px;
  font-size: 14px;
}
button {
  width: 100%;
  padding: 14px;
  background: #1C7293;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
button:hover:not(:disabled) { background: #14556E; }
button:disabled { opacity: 0.6; cursor: not-allowed; }
.back-link {
  display: block;
  text-align: center;
  margin-top: 24px;
  color: #888;
  font-size: 14px;
  text-decoration: none;
}
.back-link:hover { color: #4FB3D9; }
</style>
