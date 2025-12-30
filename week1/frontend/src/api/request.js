import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 5000
})

service.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    console.error('API Error:', error)
    // Only show message if it's not a cancellation
    if (error.code !== 'ERR_CANCELED') {
        const message = error.response?.data?.detail || error.message || 'An error occurred';
        ElMessage.error(message)
    }
    return Promise.reject(error)
  }
)

export default service
