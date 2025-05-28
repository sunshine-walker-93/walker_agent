<template>
  <div class="nav-container">
    <el-menu
      :default-active="activeIndex"
      class="nav-menu"
      mode="horizontal"
      router
    >
      <el-menu-item index="/">
        <el-icon><HomeFilled /></el-icon>
        首页
      </el-menu-item>
      <el-menu-item index="/chat">
        <el-icon><ChatDotRound /></el-icon>
        智能助手
      </el-menu-item>
      <el-menu-item index="/profile">
        <el-icon><User /></el-icon>
        个人资料
      </el-menu-item>
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        系统设置
      </el-menu-item>
    </el-menu>

    <div class="nav-right">
      <template v-if="!isLoggedIn">
        <el-button type="text" @click="$router.push('/login')">登录</el-button>
        <el-button type="primary" @click="$router.push('/register')">注册</el-button>
      </template>
      <template v-else>
        <el-dropdown>
          <el-avatar :size="32" :src="userAvatar" />
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$router.push('/profile')">个人资料</el-dropdown-item>
              <el-dropdown-item @click="$router.push('/settings')">系统设置</el-dropdown-item>
              <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  HomeFilled,
  ChatDotRound,
  User,
  Setting
} from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()

const activeIndex = computed(() => route.path)
const isLoggedIn = computed(() => userStore.isLoggedIn)
const userAvatar = computed(() => userStore.avatar || '/default-avatar.png')

const handleLogout = async () => {
  await userStore.logout()
}
</script>

<style lang="scss" scoped>
.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
  background-color: var(--el-bg-color);
  box-shadow: var(--el-box-shadow-light);
}

.nav-menu {
  border-bottom: none;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style> 