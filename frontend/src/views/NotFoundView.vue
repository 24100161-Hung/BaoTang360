<template>
  <div class="not-found">
    <div class="content">
      <div class="error-code">404</div>
      <h1>Không tìm thấy trang</h1>
      <p>Trang bạn đang tìm kiếm không tồn tại hoặc đã bị di chuyển.</p>
      <div class="actions">
        <router-link to="/" class="btn-primary">← Về trang chủ</router-link>
        <router-link to="/tour/sanh-chinh" class="btn-secondary">
          Tham quan bảo tàng
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0a0e14 0%, #1c7293 100%);
  color: white;
  padding: 20px;
}

.content {
  text-align: center;
  max-width: 500px;
}

.error-code {
  font-size: 140px;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(135deg, #4fb3d9, #1c7293);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 16px;
}

h1 {
  font-size: 32px;
  margin: 0 0 12px;
}

p {
  color: #b0b0b0;
  margin-bottom: 32px;
  line-height: 1.6;
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  padding: 12px 24px;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  transition: transform 0.2s;
}

.btn-primary {
  background: #1c7293;
  color: white;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-primary:hover,
.btn-secondary:hover {
  transform: translateY(-2px);
}
</style>
