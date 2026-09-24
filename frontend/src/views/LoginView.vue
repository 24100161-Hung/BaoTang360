<template>
  <div class="login-page">
    <div class="login-box">
      <div class="logo">🏛️</div>
      <h2>Đăng nhập Quản trị</h2>
      <p class="subtitle">Bảo tàng ảo 360° - CSE703073</p>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="admin@baotang.test"
            autocomplete="email"
          />
        </div>

        <div class="form-group">
          <label for="password">Mật khẩu</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="Password123!"
            autocomplete="current-password"
          />
        </div>

        <button type="submit" :disabled="loading" class="btn-login">
          {{ loading ? 'Đang đăng nhập...' : 'Đăng nhập' }}
        </button>

        <p v-if="error" class="error">{{ error }}</p>
      </form>

      <router-link to="/" class="back-link">← Về trang chủ</router-link>

      <div class="test-accounts">
        <p><strong>Tài khoản mẫu:</strong></p>
        <p>📧 admin@baotang.test</p>
        <p>🔑 Password123!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '@/lib/api'

const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    const { data } = await api.post('/login', {
      email: email.value,
      password: password.value,
    })

    // Lưu token và thông tin user
    localStorage.setItem('admin_token', data.token)
    localStorage.setItem('admin_user', JSON.stringify(data.user))

    // Chuyển hướng
    const redirect = route.query.redirect || '/admin/scenes'
    router.push(redirect)
  } catch (e) {
    console.error('Login error:', e)
    if (e.response?.status === 401) {
      error.value = 'Email hoặc mật khẩu không đúng.'
    } else if (e.response?.status === 403) {
      error.value = 'Tài khoản đã bị khóa.'
    } else if (e.response?.status === 429) {
      error.value = 'Quá nhiều lần thử. Vui lòng đợi 1 phút.'
    } else {
      error.value = e.response?.data?.message || 'Đăng nhập thất bại. Vui lòng thử lại.'
    }
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
  background: linear-gradient(135deg, #0a0e14 0%, #1C7293 100%);
  padding: 20px;
}

.login-box {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  padding: 48px 40px;
  border-radius: 20px;
  width: 100%;
  max-width: 440px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  color: white;
}

.logo {
  font-size: 48px;
  text-align: center;
  margin-bottom: 16px;
}

h2 {
  text-align: center;
  margin: 0 0 8px 0;
  color: #4FB3D9;
  font-size: 28px;
}

.subtitle {
  text-align: center;
  color: #888;
  font-size: 14px;
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #b0b0b0;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(0, 0, 0, 0.3);
  color: white;
  font-size: 15px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #4FB3D9;
  background: rgba(0, 0, 0, 0.5);
}

input::placeholder {
  color: #666;
}

.btn-login {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #1C7293, #14556E);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  margin-top: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(28, 114, 147, 0.4);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #ff6b6b;
  text-align: center;
  margin-top: 16px;
  padding: 10px;
  background: rgba(220, 53, 69, 0.15);
  border-radius: 8px;
  font-size: 14px;
}

.back-link {
  display: block;
  text-align: center;
  margin-top: 20px;
  color: #888;
  text-decoration: none;
  font-size: 14px;
}

.back-link:hover {
  color: #4FB3D9;
}

.test-accounts {
  margin-top: 24px;
  padding: 16px;
  background: rgba(28, 114, 147, 0.15);
  border-radius: 10px;
  font-size: 13px;
  color: #b0b0b0;
  border-left: 3px solid #4FB3D9;
}

.test-accounts p {
  margin: 4px 0;
}
</style>
