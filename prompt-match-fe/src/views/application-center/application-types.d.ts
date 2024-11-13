import type {IconNames} from './Icon'

interface ApplicationListItemType {
  id: number
  icon: IconNames
  name: string
  description: string
  knowledge_vos: KnowledgeVoItemType[]
  model_name: string
  model_name_valid: boolean
  creator: string
  creator_id: string
  create_time: string
  modifier: string
  modifier_id: string
  update_time?: string
}

interface KnowledgeVoItemType {
  knowledge_id: number
  knowledge_name: string
}

export type {ApplicationListItemType, KnowledgeVoItemType}
