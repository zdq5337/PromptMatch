export interface ResponseData<T> {
  code: string
  success: boolean
  message: string
  data: T
}

export type Response<T> = Promise<ResponseData<T>>
