<template>
  <div class="chat-container">
    <el-card class="chat-card">
      <template #header>
        <div class="chat-header">
          <h2>智能助手</h2>
          <el-button type="primary" @click="startNewChat">新对话</el-button>
        </div>
      </template>
      
      <div class="chat-messages" ref="messagesContainer">
        <div v-for="(message, index) in messages" :key="index" 
             :class="['message', message.role === 'user' ? 'user-message' : 'assistant-message']">
          <div class="message-content">
            <div class="message-avatar">
              <el-avatar :size="40" :icon="message.role === 'user' ? 'User' : 'Service'"></el-avatar>
            </div>
            <div class="message-text">
              <div class="message-role">{{ message.role === 'user' ? '我' : '智能助手' }}</div>
              <div class="message-body">{{ message.content }}</div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <el-input
          v-model="inputMessage"
          type="textarea"
          :rows="3"
          placeholder="输入消息..."
          @keyup.enter.ctrl="sendMessage"
        ></el-input>
        <div class="input-actions">
          <el-button type="primary" @click="sendMessage" :loading="loading">发送</el-button>
          <span class="input-tip">按 Ctrl + Enter 发送</span>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Service } from '@element-plus/icons-vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const messages = ref<Message[]>([])
const inputMessage = ref('')
const loading = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) {
    ElMessage.warning('请输入消息内容')
    return
  }

  const userMessage = inputMessage.value.trim()
  messages.value.push({
    role: 'user',
    content: userMessage
  })
  inputMessage.value = ''
  await scrollToBottom()

  loading.value = true
  try {
    // TODO: 实现与后端AI服务的通信
    // 模拟AI响应
    setTimeout(() => {
      messages.value.push({
        role: 'assistant',
        content: '这是一个模拟的AI响应。实际使用时，这里应该调用后端AI服务获取真实的响应。'
      })
      scrollToBottom()
    }, 1000)
  } catch (error) {
    ElMessage.error('发送消息失败')
  } finally {
    loading.value = false
  }
}

const startNewChat = () => {
  messages.value = []
  ElMessage.success('已开始新对话')
}

onMounted(() => {
  // 添加欢迎消息
  messages.value.push({
    role: 'assistant',
    content: '你好！我是你的智能助手，有什么我可以帮你的吗？'
  })
})
</script>

<style scoped>
.chat-container {
  padding: 20px;
  height: calc(100vh - 40px);
}

.chat-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h2 {
  margin: 0;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message {
  max-width: 80%;
}

.message-content {
  display: flex;
  gap: 12px;
}

.user-message {
  align-self: flex-end;
}

.assistant-message {
  align-self: flex-start;
}

.message-text {
  background-color: #f5f7fa;
  padding: 12px;
  border-radius: 8px;
}

.user-message .message-text {
  background-color: #ecf5ff;
}

.message-role {
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.message-body {
  white-space: pre-wrap;
  word-break: break-word;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #ebeef5;
}

.input-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 12px;
  gap: 12px;
}

.input-tip {
  font-size: 12px;
  color: #909399;
}
</style> 