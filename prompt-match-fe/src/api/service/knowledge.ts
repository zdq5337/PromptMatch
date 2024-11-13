import request from '../config/request'
import type {
  KnowledgeBaseListItemType,
  KnowledgeFileBaseListItemBase
} from '@/views/knowledge-base/list/knowledge-types.d.ts'

// 知识库
// 新增知识库
const createKnowledgeBase = (data: KnowledgeBaseListItemType) =>
  request.post('/model-match/v1/knowledge', data)

// 获取所有知识库
const getAllKnowledgeBase = () =>
  request.get<KnowledgeBaseListItemType[]>('/model-match/v1/knowledge')

// 删除当前知识库
const deleteKnowledgeBase = (id: number) => request.delete(`/model-match/v1/knowledge/${id}`)

// 编辑知识库
const editKnowledgeBase = (data: KnowledgeBaseListItemType) =>
  request.put(`/model-match/v1/knowledge`, data)

// 获取知识库详细信息
const getKnowledgeBaseDetail = (id: number) =>
  request.get<KnowledgeBaseListItemType>(`/model-match/v1/knowledge/${id}`)

// 知识库文件
// 上传知识库文件
const createKnowledgeFile = (data: KnowledgeFileBaseListItemBase[]) =>
  request.post('/model-match/v1/knowledge_file', data)

export {
  createKnowledgeBase,
  getAllKnowledgeBase,
  deleteKnowledgeBase,
  editKnowledgeBase,
  getKnowledgeBaseDetail,
  createKnowledgeFile
}
