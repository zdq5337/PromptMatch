/*
 * @Description: 新增/编辑知识库
 * @Author: Kyeoni hujr
 * @Date: 2024-05-20 14:21:03
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-09-11 09:51:44
 */
import styles from './list.module.less'
import { forwardRef, useState, useImperativeHandle } from 'react'
import { Modal, Form, Input, message } from 'antd'
import {
  ToolFilled,
  BookFilled,
  CloudFilled,
  PushpinFilled,
  MessageFilled
} from '@ant-design/icons'
import { createKnowledgeBase, editKnowledgeBase } from '@/api/service/knowledge.ts'
import type { KnowledgeBaseListItemType, KnowledgeBaseListItemBase } from './knowledge-types'

interface KnowledgeBaseModalInfo {
  type: 'add' | 'edit'
  initValues?: KnowledgeBaseListItemType
}
export interface KnowledgeBaseModalHandle {
  open: (data: KnowledgeBaseModalInfo) => void
}

interface KnowledgeBaseModalProps {
  fetchKnowledgeBaseList: () => void;
}

const KnowledgeBaseModal = forwardRef<KnowledgeBaseModalHandle, KnowledgeBaseModalProps>((props, ref) => {
  const [modalOpen, setModalOpen] = useState(false)
  const [title, setTitle] = useState('')
  const [form] = Form.useForm()
  const iconName = Form.useWatch('icon', form)
  const [modalInfo, setModalInfo] = useState<KnowledgeBaseModalInfo | null>(null)


  useImperativeHandle(ref, () => ({
    open: (data: KnowledgeBaseModalInfo) => {
      setTitle(`${data.type === 'add' ? '新建' : '编辑'}知识库`)
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
      values = { ...modalInfo.initValues, ...formValues }
    }

    console.log('modalInfo', modalInfo)
    console.log('values', values)

    if (modalInfo?.type === 'add') {
      //创建知识库
      createKnowledgeBase(values).then(() => {
        message.success('创建成功')
        form?.resetFields()
        setModalOpen(false)
        //需要进行刷新列表操作
        props.fetchKnowledgeBaseList()
      })
    } else if (modalInfo?.type === 'edit') {
      // 编辑知识库
      editKnowledgeBase(values).then(() => {
        message.success('编辑成功')
        form?.resetFields()
        setModalOpen(false)
        //需要进行刷新列表操作
        props.fetchKnowledgeBaseList()
      })
    }

  }

  const handleIconClick = (iconName: string) => {
    form.setFieldsValue({ icon: iconName })
  }

  return (
    <Modal
      title={title}
      centered
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
        initialValues={{ remember: true }}
        autoComplete='off'
        size='large'
      >
        <Form.Item<KnowledgeBaseListItemBase | KnowledgeBaseListItemType>
          label='知识库名称'
          name='name'
          rules={[{ required: true, message: '请输入知识库名称' }]}
        >
          <Input placeholder='请输入知识库名称' />
        </Form.Item>

        <Form.Item<KnowledgeBaseListItemBase | KnowledgeBaseListItemType>
          label='知识库描述'
          name='description'
          rules={[{ required: true, message: '请输入知识库描述' }]}
        >
          <Input placeholder='请输入知识库描述' />
        </Form.Item>

        <Form.Item<KnowledgeBaseListItemBase | KnowledgeBaseListItemType>
          label='知识库图标'
          name='icon'
          rules={[{ required: true, message: '请选择知识库图标' }]}
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
      </Form>
    </Modal>
  )
})

export default KnowledgeBaseModal
