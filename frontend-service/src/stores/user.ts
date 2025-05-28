import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { login as loginApi, logout as logoutApi, getUserInfo } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userInfo = ref<User | null>(null)

  const isLoggedIn = computed(() => !!token.value)
  const avatar = computed(() => userInfo.value?.avatar)

  async function login(username: string, password: string) {
    const { access_token } = await loginApi(username, password)
    token.value = access_token
    await fetchUserInfo()
  }

  async function logout() {
    await logoutApi()
    token.value = ''
    userInfo.value = null
  }

  async function fetchUserInfo() {
    userInfo.value = await getUserInfo()
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    avatar,
    login,
    logout,
    fetchUserInfo
  }
}) 