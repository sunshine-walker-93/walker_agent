export interface User {
  id: number
  username: string
  email: string
  full_name: string
  avatar?: string
  created_at: string
  updated_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
} 