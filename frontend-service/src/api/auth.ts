import axios from 'axios'
import type { LoginResponse, User, ApiResponse } from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 5000
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export async function login(username: string, password: string): Promise<LoginResponse> {
  const response = await api.post<ApiResponse<LoginResponse>>('/auth/token', {
    username,
    password
  })
  return response.data
}

export async function logout(): Promise<void> {
  await api.post('/auth/logout')
  localStorage.removeItem('token')
}

export async function getUserInfo(): Promise<User> {
  const response = await api.get<ApiResponse<User>>('/user/profile')
  return response.data
}

export async function register(data: {
  username: string
  password: string
  email: string
  full_name: string
}): Promise<void> {
  await api.post('/auth/register', data)
} 