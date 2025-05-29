<template>
  <div class="profile-container">
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <h2>个人资料</h2>
          <el-button type="primary" @click="handleEdit" v-if="!isEditing">编辑</el-button>
          <div v-else>
            <el-button type="success" @click="handleSave" :loading="loading">保存</el-button>
            <el-button @click="handleCancel">取消</el-button>
          </div>
        </div>
      </template>
      
      <el-form :model="profileForm" :rules="rules" ref="profileFormRef" :disabled="!isEditing">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="profileForm.username"></el-input>
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="profileForm.email"></el-input>
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="profileForm.phone"></el-input>
        </el-form-item>
        
        <el-form-item label="个人简介" prop="bio">
          <el-input type="textarea" v-model="profileForm.bio" rows="4"></el-input>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'

const profileFormRef = ref<FormInstance>()
const loading = ref(false)
const isEditing = ref(false)

const profileForm = reactive({
  username: '',
  email: '',
  phone: '',
  bio: ''
})

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const handleEdit = () => {
  isEditing.value = true
}

const handleCancel = () => {
  isEditing.value = false
  // 重置表单
  if (profileFormRef.value) {
    profileFormRef.value.resetFields()
  }
}

const handleSave = async () => {
  if (!profileFormRef.value) return
  
  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        // TODO: 实现保存逻辑
        ElMessage.success('保存成功')
        isEditing.value = false
      } catch (error) {
        ElMessage.error('保存失败')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card {
  max-width: 800px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
}
</style> 