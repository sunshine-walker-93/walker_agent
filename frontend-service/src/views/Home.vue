<template>
  <div class="home-bg">
    <div class="home-content right-top">
      <h1 class="title">欢迎使用智能助手</h1>
      <p class="subtitle">登录或注册以开始使用</p>
      <div class="button-group">
        <el-button type="primary" size="large" @click="goToLogin">
          登录
        </el-button>
        <el-button type="success" size="large" @click="goToRegister">
          注册
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style scoped>
.home-bg {
  min-height: 100vh;
  width: 100vw;
  background: url('/crane-bg.jpg') center top/contain no-repeat, linear-gradient(135deg, #f8ecd6 0%, #e6f0fa 100%);
  display: flex;
  align-items: stretch;
  justify-content: stretch;
  position: relative;
}

.home-content.right-top {
  position: absolute;
  top: 40px;
  right: 60px;
  background: rgba(255, 255, 255, 0.85);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  padding: 48px 36px 40px 36px;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 320px;
  max-width: 90vw;
  z-index: 10;
}

.title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  background: linear-gradient(45deg, #ffd700, #ff8c00);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #666;
}

.button-group {
  display: flex;
  gap: 20px;
}

.button-group .el-button {
  min-width: 120px;
  font-size: 1.1rem;
  padding: 12px 24px;
}

@media (max-width: 768px) {
  .home-content.right-top {
    position: static;
    margin: 32px auto 0 auto;
    top: unset;
    right: unset;
    left: unset;
    transform: none;
    width: 95vw;
    min-width: 0;
    max-width: 100vw;
  }
  .title {
    font-size: 2rem;
  }
  .button-group {
    flex-direction: column;
    width: 100%;
  }
  .button-group .el-button {
    width: 100%;
  }
}
</style> 