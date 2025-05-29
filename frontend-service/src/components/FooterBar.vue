<template>
  <div class="footer-bar">
    <el-menu
      mode="horizontal"
      :router="true"
      :default-active="activeIndex"
      class="footer-menu"
    >
      <el-menu-item index="/chat">
        <el-icon><ChatDotRound /></el-icon>
        <span>对话</span>
      </el-menu-item>
      
      <el-menu-item index="/profile">
        <el-icon><User /></el-icon>
        <span>我的</span>
      </el-menu-item>
      
      <el-menu-item index="/settings">
        <el-icon><Setting /></el-icon>
        <span>设置</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ChatDotRound, User, Setting } from '@element-plus/icons-vue'

const route = useRoute()
const activeIndex = ref(route.path)

onMounted(() => {
  // 根据当前路由设置激活的菜单项
  activeIndex.value = route.path
})
</script>

<style scoped>
.footer-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
  z-index: 1000;
}

.footer-menu {
  display: flex;
  justify-content: space-around;
  border: none;
}

.footer-menu :deep(.el-menu-item) {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60px;
  padding: 0;
}

.footer-menu :deep(.el-menu-item .el-icon) {
  margin-right: 0;
  margin-bottom: 4px;
  font-size: 20px;
}

.footer-menu :deep(.el-menu-item span) {
  font-size: 12px;
  line-height: 1;
}
</style> 