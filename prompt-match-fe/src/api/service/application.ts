import request from '../config/request'
import type { ApplicationListItemType } from '@/views/application-center/application-types.d.ts'

const createApplication = (data: ApplicationListItemType) =>
  request.post('/model-match/v1/application', data)

const getApplicationList = () =>
  request.get<ApplicationListItemType[]>('/model-match/v1/application')

const deleteApplication = (id: number) => request.delete(`/model-match/v1/application/${id}`)

const editApplication = (data: ApplicationListItemType) =>
  request.put(`/model-match/v1/application`, data)

const getApplicationDetail = (id: number) =>
  request.get<ApplicationListItemType>(`/model-match/v1/application/${id}`)

export {
  createApplication,
  getApplicationList,
  deleteApplication,
  editApplication,
  getApplicationDetail
}
