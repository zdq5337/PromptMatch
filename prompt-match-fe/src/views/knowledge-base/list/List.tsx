/*
 * @Description: 知识库列表
 * @Author: Kyeoni hujr
 * @Date: 2024-05-16 16:59:53
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-05-22 16:33:01
 */
import styles from './list.module.less'
import type {MenuProps} from 'antd'
import {Button, Dropdown, message, Modal} from 'antd'
import {MoreOutlined, PlusOutlined} from '@ant-design/icons'
import type {KnowledgeBaseModalHandle} from './Modal'
import KnowledgeBaseModal from './Modal'
import {useEffect, useRef, useState} from 'react'
import {deleteKnowledgeBase, getAllKnowledgeBase} from '@/api/service/knowledge.ts'
import type {KnowledgeBaseListItemType} from './knowledge-types'
import Icon from '@/views/knowledge-base/list/Icon'
// import { useHistory } from 'react-router-dom';
// import { withRouter } from 'react-router-dom';
import {useNavigate} from 'react-router-dom';


export default function KnowledgeBaseList() {
  const [knowledgeList, setList] = useState<Array<KnowledgeBaseListItemType>>([])
  const [showMoreButtonId, setShowMoreButtonId] = useState<number>(Infinity)

  const knowledgeBaseModal = useRef<KnowledgeBaseModalHandle>(null)
  const handleModalOpen = (type: 'add' | 'edit') => {
    let item
    if (type === 'edit') {
      item = knowledgeList.find(({id}) => id === showMoreButtonId)
    }
    knowledgeBaseModal.current?.open({
      type,
      initValues: type === 'edit' ? item : undefined
    })
    // fetchKnowledgeBaseList()
  }

  // 提取获取知识库列表的函数
  const fetchKnowledgeBaseList = () => {
    getAllKnowledgeBase().then(({data}) => {
      setList(data)
    })
  }


  useEffect(() => {
    fetchKnowledgeBaseList()
  }, [])

  const onClick: MenuProps['onClick'] = ({key}) => {
    if (key === 'edit') {
      handleModalOpen('edit')
    } else if (key === 'delete') {
      // 进行删除
      Modal.confirm({
        title: '你确定要删除这个知识库吗？',
        content: '删除后，你将无法恢复这个知识库（此删除操作将会删除知识库和知识库下的所有文件）。',
        okText: '确认',
        cancelText: '取消',
        onOk() {
          deleteKnowledgeBase(showMoreButtonId).then(({data}) => {
            message.success('删除成功');
            // 更新知识库列表
            console.log(data);
            setList(knowledgeList.filter(({id}) => id !== showMoreButtonId));
          });
        },
      });
    }
  }

  const items: MenuProps['items'] = [
    {
      key: 'edit',
      label: '编辑'
    },
    {
      key: 'delete',
      label: '删除',
      className: 'delete-item'
    }
  ]

  const navigate = useNavigate();

  const handleClick = (id: number) => {
    navigate(`/knowledge-base/detail/${id}`);
  };


  return (
    <>
      <div>
        <div className={styles.knowledgeLibraryTitle}>
          <div className={styles.knowledgeLibraryTitleLeft}>知识库管理</div>
          <div className={styles.knowledgeLibraryTitleRightButton}>
            <Button
              onClick={() => handleModalOpen('add')}
              type='primary'
              icon={<PlusOutlined/>}
              size='large'
            >
              新建知识库
            </Button>
          </div>
        </div>
      </div>
      <div className={styles.knowledgeLibraryList}>
        <div className={styles.knowledgeLibraryListGutter}></div>
        <div className={styles.knowledgeLibraryListWrapper}>
          {knowledgeList.map(item => {
            return (
              <div
                className={styles.knowledgeLibraryListItem}
                key={item.id}
                onMouseEnter={() => setShowMoreButtonId(item.id)}
                onMouseLeave={() => setShowMoreButtonId(Infinity)}

              >
                <div className={styles.knowledgeLibraryListItemInner}>
                  <div className={styles.knowledgeLibraryListItemIcon} onClick={() => handleClick(item.id)}>
                    <Icon type={item.icon}/>
                  </div>
                  <div className={styles.knowledgeLibraryListItemName}>{item.name}</div>
                  <div className={styles.knowledgeLibraryListIteDesc}>{item.description}</div>

                  <Dropdown menu={{items, onClick}} trigger={['hover']}>
                    <MoreOutlined
                      // onClick={() => handleModalOpen('add')}
                      className={`${styles.dropdownMoreButton} ${showMoreButtonId === item.id && styles.dropdownMoreButtonActive}`}
                    />
                  </Dropdown>
                </div>
              </div>
            )
          })}
        </div>
        <div className={styles.knowledgeLibraryListGutter}></div>
      </div>
      {/*<KnowledgeBaseModal ref={knowledgeBaseModal} />*/}
      <KnowledgeBaseModal ref={knowledgeBaseModal} fetchKnowledgeBaseList={fetchKnowledgeBaseList}/>
    </>
  )
}
