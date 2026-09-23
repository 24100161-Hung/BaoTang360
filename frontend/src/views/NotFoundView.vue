<template>
  <div class="not-found">
    <h1>404</h1>
    <p>Không tìm thấy trang bạn đang tìm kiếm</p>
    <router-link to="/" class="btn">Về trang chủ</router-link>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  background: #0a0e14;
}
h1 { font-size: 120px; margin: 0; color: #4FB3D9; }
p { font-size: 18px; margin-bottom: 32px; color: #999; }
.btn {
  background: #1C7293;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
}
.btn:hover { background: #14556E; }
</style>
