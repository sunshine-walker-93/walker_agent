<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container">
      <el-container>
        <el-header>
          <NavBar v-if="isAuthenticated" />
        </el-header>
        <el-main>
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
        <el-footer>
          <FooterBar v-if="isAuthenticated" />
        </el-footer>
      </el-container>
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/NavBar.vue'
import FooterBar from '@/components/FooterBar.vue'

const userStore = useUserStore()
const isAuthenticated = computed(() => userStore.isAuthenticated)
</script>

<style lang="scss">
.app-container {
  min-height: 100vh;
  background-color: var(--el-bg-color-page);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 