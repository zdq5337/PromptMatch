import request from '../config/request'
import type {
  LargeModelItemType
} from '@/views/prompt-match/large-model-types.d.ts'

// 获取所有模型信息
const getAllLargeModelBase = () =>
  request.get<LargeModelItemType[]>('/model-match/v1/large_model')


export {
  getAllLargeModelBase
}
