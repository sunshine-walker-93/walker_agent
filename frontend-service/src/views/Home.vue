<template>
  <div class="home">
    <h1>欢迎使用个人信息管理系统</h1>
    <el-row :gutter="20" class="feature-list">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>个人信息管理</span>
            </div>
          </template>
          <div class="card-content">
            管理您的个人资料、设置和偏好
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>智能助手</span>
            </div>
          </template>
          <div class="card-content">
            与AI助手对话，获取帮助和建议
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>系统设置</span>
            </div>
          </template>
          <div class="card-content">
            自定义系统设置和偏好
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
// 组件逻辑
</script>

<style lang="scss" scoped>
.home {
  padding: 20px;

  h1 {
    text-align: center;
    margin-bottom: 40px;
  }

  .feature-list {
    margin-top: 20px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .card-content {
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
}
</style> 