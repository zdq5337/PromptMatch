import axios, { AxiosError } from 'axios'
import { message as messageApi } from 'antd'
import { Response } from '@/types'

const axiosInstance = axios.create({
  baseURL: import.meta.env.VITE_MAIN_BASE_URL,
  timeout: 60000,
  timeoutErrorMessage: '请求超时，请稍后重试',
  withCredentials: true
})

// 请求拦截器
axiosInstance.interceptors.request.use(
  config => {
    // TODO: 引入状态管理后改写这块
    // if (token) {
    //   // 把token放到请求头里
    //   config.headers.Authorization = token
    // }
    // config.headers['X-Remote-Client'] = getRemoteClient()
    return config
  },
  (error: AxiosError) => Promise.reject(error)
)

// 响应拦截器
axiosInstance.interceptors.response.use(
  response => response?.data,
  error => {
    if (error.response) {
      // 请求发出去收到响应了，但是状态码超出了2xx范围
      const {
        status,
        data: { message }
      } = error.response
      // 后端要求只有400/401向外暴露message
      if (status === 400) {
        messageApi.error(message || '请求参数错误')
      } else if (status === 401) {
        // 后台返回401，用户无权限访问该接口
        messageApi.error('您没有权限或长时间未登录，请重新登录')
      } else if (status === 403) {
        messageApi.error('您没有权限')
      } else if (status === 404 || status >= 500) {
        // 后台404并不是找不到资源，而是报错，属于历史问题
        messageApi.error('抱歉，服务端异常，正在抢修中，请您稍后重试')
      }
    } else if (/timeout/.test(error.message)) {
      // 请求发出去没有收到响应
      messageApi.error('请求超时，请刷新重试')
    }
  }
)

export default {
  get<T>(url: string, params?: object): Response<T> {
    return axiosInstance.get(url, { params })
  },
  post<T>(url: string, params?: object): Response<T> {
    return axiosInstance.post(url, params)
  },
  delete<T>(url: string): Response<T> {
    return axiosInstance.delete(url)
  },
  put<T>(url: string, params?: object): Response<T> {
    return axiosInstance.put(url, params)
  }
}
