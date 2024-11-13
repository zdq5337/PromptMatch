/*
 * @Description: 新增/编辑应用
 * @Author: Kyeoni hujr
 * @Date: 2024-05-20 14:21:03
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-05-22 17:35:21
 */
import styles from '@/views/knowledge-base/list/list.module.less'
import React, {forwardRef, useImperativeHandle, useState} from 'react'
import {Form, Input, message, Modal, Select} from 'antd'
import {BookFilled, CloudFilled, MessageFilled, PushpinFilled, ToolFilled} from '@ant-design/icons'
import {createApplication, editApplication} from '@/api/service/application.ts'
import type {ApplicationListItemType} from './application-types'

interface ApplicationModalInfo {
  type: 'add' | 'edit'
  initValues?: ApplicationListItemType
}

export interface ApplicationModalHandle {
  open: (data: ApplicationModalInfo) => void
}

interface ApplicationModalProps {
  fetchApplicationList: () => void;
}

const ApplicationModal = forwardRef<ApplicationModalHandle, ApplicationModalProps>((props, ref) => {
  const [modalOpen, setModalOpen] = useState(false)
  const [title, setTitle] = useState('')
  const [form] = Form.useForm()
  const iconName = Form.useWatch('icon', form)
  const [modalInfo, setModalInfo] = useState<ApplicationModalInfo | null>(null)


  useImperativeHandle(ref, () => ({
    open: (data: ApplicationModalInfo) => {
      setTitle(`${data.type === 'add' ? '新建' : '编辑'}应用`)
      form.setFieldsValue(data.initValues)
      setModalOpen(true)
      setModalInfo(data)
    },
    close: () => {
      setModalOpen(false)
    }
  }))


  const handleOkClick = async () => {
    // const values = await form?.validateFields()
    // const values = modalInfo?.type === 'edit' ? modalInfo.initValues : await form?.validateFields()

    const formValues = await form?.validateFields()
    let values = formValues

    if (modalInfo?.type === 'edit' && modalInfo.initValues) {
      // 使用 formValues 的值覆盖 modalInfo.initValues 的值
      values = {...modalInfo.initValues, ...formValues}
    }

    console.log('modalInfo', modalInfo)
    console.log('values', values)

    if (modalInfo?.type === 'add') {
      createApplication(values).then(() => {
        message.success('创建成功')
        form?.resetFields()
        setModalOpen(false)
        //刷新列表
        props.fetchApplicationList()
      })
    } else if (modalInfo?.type === 'edit') {
      editApplication(values).then(() => {
        message.success('编辑成功')
        form?.resetFields()
        setModalOpen(false)
        //刷新列表
        props.fetchApplicationList()
      })
    }

  }

  const handleIconClick = (iconName: string) => {
    form.setFieldsValue({icon: iconName})
  }

  return (
    <Modal
      title={title}
      open={modalOpen}
      onOk={() => handleOkClick()}
      onCancel={() => setModalOpen(false)}
      okText='保存'
      cancelText='取消'
    >
      <Form
        form={form}
        layout='vertical'
        name='basic'
        initialValues={{remember: true}}
        autoComplete='off'
        size='large'
      >
        <Form.Item<ApplicationListItemType>
          label='应用名称'
          name='name'
          rules={[{required: true, message: '请输入应用名称'}]}
        >
          <Input placeholder='请输入应用名称'/>
        </Form.Item>

        <Form.Item<ApplicationListItemType>
          label='应用描述'
          name='description'
          rules={[{required: true, message: '请输入应用描述'}]}
        >
          <Input placeholder='请输入应用描述'/>
        </Form.Item>

        <Form.Item<ApplicationListItemType>
          label='应用图标'
          name='icon'
          rules={[{required: true, message: '请选择应用图标'}]}
        >
          <div>
            <div>
              <ToolFilled
                onClick={() => handleIconClick('ToolFilled')}
                className={`${styles.knowledgeModelIcon} ${iconName === 'ToolFilled' ? styles.knowledgeModelIconActive : ''}`}
              />
              <BookFilled
                onClick={() => handleIconClick('BookFilled')}
                className={`${styles.knowledgeModelIcon} ${iconName === 'BookFilled' ? styles.knowledgeModelIconActive : ''}`}
              />
              <CloudFilled
                onClick={() => handleIconClick('CloudFilled')}
                className={`${styles.knowledgeModelIcon} ${iconName === 'CloudFilled' ? styles.knowledgeModelIconActive : ''}`}
              />
              <PushpinFilled
                onClick={() => handleIconClick('PushpinFilled')}
                className={`${styles.knowledgeModelIcon} ${iconName === 'PushpinFilled' ? styles.knowledgeModelIconActive : ''}`}
              />
              <MessageFilled
                onClick={() => handleIconClick('MessageFilled')}
                className={`${styles.knowledgeModelIcon} ${iconName === 'MessageFilled' ? styles.knowledgeModelIconActive : ''}`}
              />
            </div>
          </div>
        </Form.Item>

        <Form.Item<ApplicationListItemType>
          label='引用知识库'
          name='knowledge_vos'
        >
          <Select placeholder='关联知识库'/>
        </Form.Item>

        <Form.Item<ApplicationListItemType>
          label='调用模型'
          name='model_name'
          rules={[{required: true, message: '请选择模型'}]}
        >
          <Select placeholder='选择模型'/>
        </Form.Item>
      </Form>
    </Modal>
  )
})

export default ApplicationModal
