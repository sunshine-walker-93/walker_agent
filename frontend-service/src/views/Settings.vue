<template>
  <div class="settings-container">
    <el-card class="settings-card">
      <template #header>
        <h2>系统设置</h2>
      </template>
      
      <el-form :model="settingsForm" ref="settingsFormRef" label-width="120px">
        <el-form-item label="主题">
          <el-select v-model="settingsForm.theme" placeholder="选择主题">
            <el-option label="浅色" value="light"></el-option>
            <el-option label="深色" value="dark"></el-option>
            <el-option label="跟随系统" value="system"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="语言">
          <el-select v-model="settingsForm.language" placeholder="选择语言">
            <el-option label="简体中文" value="zh-CN"></el-option>
            <el-option label="English" value="en-US"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="通知">
          <el-switch v-model="settingsForm.notifications"></el-switch>
        </el-form-item>
        
        <el-form-item label="自动保存">
          <el-switch v-model="settingsForm.autoSave"></el-switch>
        </el-form-item>
        
        <el-form-item label="保存间隔" v-if="settingsForm.autoSave">
          <el-input-number v-model="settingsForm.saveInterval" :min="1" :max="60"></el-input-number>
          <span class="unit">分钟</span>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSave" :loading="loading">保存设置</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const settingsFormRef = ref<FormInstance>()
const loading = ref(false)

const defaultSettings = {
  theme: 'light',
  language: 'zh-CN',
  notifications: true,
  autoSave: true,
  saveInterval: 5
}

const settingsForm = reactive({ ...defaultSettings })

const handleSave = async () => {
  loading.value = true
  try {
    // TODO: 实现保存设置逻辑
    ElMessage.success('设置已保存')
  } catch (error) {
    ElMessage.error('保存设置失败')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  Object.assign(settingsForm, defaultSettings)
  ElMessage.success('设置已重置')
}
</script>

<style scoped>
.settings-container {
  padding: 20px;
}

.settings-card {
  max-width: 800px;
  margin: 0 auto;
}

.unit {
  margin-left: 8px;
  color: #666;
}
</style> 