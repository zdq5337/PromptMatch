import type { IconNames } from '@/views/knowledge-base/list/Icon'

interface KnowledgeBaseListItemBase {
  icon: IconNames
  name: string
  description: string
}

interface KnowledgeBaseListItemType extends KnowledgeBaseListItemBase {
  create_time: string
  creator: string
  creator_id: string
  file_vos: KnowledgeFileBaseListItemType[]
  id: number
  modifier: string
  modifier_id: string
  update_time?: string
}

interface KnowledgeFileBaseListItemBase {
  create_time?: string
  creator?: string
  creator_id?: string
  id?: number
  modifier?: string
  modifier_id?: string
  update_time?: string
}

interface KnowledgeFileBaseListItemType extends KnowledgeFileBaseListItemBase {
  name: string
  oss_path: string
  size: number
  knowledge_id: number
}

export type {
  KnowledgeBaseListItemBase,
  KnowledgeBaseListItemType,
  KnowledgeFileBaseListItemBase,
  KnowledgeFileBaseListItemType
}
