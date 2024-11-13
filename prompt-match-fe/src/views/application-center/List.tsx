/*
 * @Description: 应用中心
 * @Author: Kyeoni hujr
 * @Date: 2024-05-16 17:22:13
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-05-16 17:22:15
 */
import {Button, Dropdown/*, Dropdown, Modal, message*/} from 'antd'
import {PlusOutlined, MoreOutlined} from '@ant-design/icons'
import ApplicationModal from './Modal.tsx'
import type {ApplicationModalHandle} from './Modal'
import {useEffect, useRef, useState} from 'react'
import {deleteApplication, getApplicationList} from '@/api/service/application.ts'
import type {ApplicationListItemType} from './application-types'
// import Icon from '@/views/knowledge-base/list/Icon'
import {MenuProps, message, Modal} from 'antd'
import styles from "@/views/knowledge-base/list/list.module.less";
import Icon from "@/views/knowledge-base/list/Icon.tsx";
import {useNavigate} from "react-router-dom";

export default function ApplicationCenter() {
  const [applicationList, setList] = useState<Array<ApplicationListItemType>>([])
  const [showMoreButtonId, setShowMoreButtonId] = useState<number>(Infinity)

  const ApplicationModalRef = useRef<ApplicationModalHandle>(null)
  const handleModalOpen = (type: 'add' | 'edit') => {
    let item
    if (type === 'edit') {
      item = applicationList.find(({id}) => id === showMoreButtonId)
    }
    ApplicationModalRef.current?.open({
      type,
      initValues: type === 'edit' ? item : undefined
    })
  };

  useEffect(() => {
    fetchApplicationList()
  }, [])

  // 获取应用列表的函数
  const fetchApplicationList = () => {
    console.log('fetchApplicationList')
    getApplicationList().then(({data}) => {
      console.log(data)
      setList(data)
    })
  }

  const onClick: MenuProps['onClick'] = ({key}) => {
    if (key === 'experience') {
      console.log("experience:"+showMoreButtonId)
      navigate(`/application-center/experience/${showMoreButtonId}`);
    } else if (key === 'edit') {
      handleModalOpen('edit')
    } else if (key === 'delete') {
      // 进行删除
      Modal.confirm({
        title: '你确定要删除这个应用吗？',
        content: '删除后，你将无法恢复这个应用（此删除操作将会删除应用和应用下的相关数据）。',
        okText: '确认',
        cancelText: '取消',
        onOk() {
          deleteApplication(showMoreButtonId).then(({data}) => {
            message.success('删除成功');
            // 更新应用列表
            console.log(data);
            setList(applicationList.filter(({id}) => id !== showMoreButtonId));
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
    },
    {
      key: 'experience',
      label: '体验',
    }
  ]

  const navigate = useNavigate();

  const handleClick = (id: number) => {
    navigate(`/application-center/detail/${id}`);
  };

  return (
    <div>
      <div className={styles.knowledgeLibraryTitle}>
        <div className={styles.knowledgeLibraryTitleLeft}>我的应用</div>
        <div className={styles.knowledgeLibraryTitleRightButton}>
          <Button
            onClick={() => handleModalOpen('add')}
            type='primary'
            icon={<PlusOutlined/>}
            size='large'
          >
            新建应用
          </Button>
        </div>
      </div>
      <div className={styles.knowledgeLibraryList}>
        <div className={styles.knowledgeLibraryListGutter}></div>
        <div className={styles.knowledgeLibraryListWrapper}>
          {applicationList.map(item => {
            return (
              <div
                className={styles.knowledgeLibraryListItem}
                key={item.id}
                onMouseEnter={() => setShowMoreButtonId(item.id)}
                onMouseLeave={() => setShowMoreButtonId(Infinity)}
                onClick={() => handleClick(item.id)}
              >
                <div className={styles.knowledgeLibraryListItemInner}>
                  <div className={styles.knowledgeLibraryListItemIcon}>
                    <Icon type={item.icon}/>
                  </div>
                  <div className={styles.knowledgeLibraryListItemName}>{item.name}</div>
                  <div className={styles.knowledgeLibraryListIteDesc}>{item.description}</div>

                  <Dropdown menu={{items, onClick}} trigger={['hover']}>
                    <MoreOutlined
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
      {<ApplicationModal ref={ApplicationModalRef} fetchApplicationList={fetchApplicationList}/>}
    </div>
  )
}
