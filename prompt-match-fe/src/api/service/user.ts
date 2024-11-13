/*
 * @Description: 客户相关请求
 * @Author: Kyeoni hujr
 * @Date: 2024-09-11 09:48:34
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-09-11 10:50:32
 */

import request from '../config/request'
import { UserLoginedInfo, UserLoginForm } from '@/views/user/user-types'

const userLogin = (data: UserLoginForm) => request.post<UserLoginedInfo>('/model-match/v1/users/login', data)

export {
  userLogin
}
