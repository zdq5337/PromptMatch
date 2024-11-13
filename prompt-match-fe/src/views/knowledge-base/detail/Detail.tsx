import React, {useEffect, useRef, useState} from 'react';
import {Button, Layout, Typography} from 'antd';
import styles from './detail.module.less';
import type {
  KnowledgeBaseListItemType,
  KnowledgeFileBaseListItemType
} from "@/views/knowledge-base/list/knowledge-types";
import {getKnowledgeBaseDetail} from "@/api/service/knowledge.ts";
import {useParams} from 'react-router-dom';
import type {KnowledgeFileUploadModalHandle} from '../file/UploadModal'
import KnowledgeFileUploadModal from '../file/UploadModal'

const {Title} = Typography;
const {Header, Sider, Content, Footer} = Layout;


const InsurancePage: React.FC = () => {
  const {id: idString} = useParams();
  const id = Number(idString);
  const [knowledgeBase, setKnowledgeBase] = useState<KnowledgeBaseListItemType | null>(null);
  const knowledgeFileUploadModal = useRef<KnowledgeFileUploadModalHandle>(null)

  const showModal = () => {
    knowledgeFileUploadModal.current?.open();
  };

  useEffect(() => {
    fetchKnowledgeBase();
  }, []);

  // 获取知识库详情
  const fetchKnowledgeBase = async () => {
    const {data} = await getKnowledgeBaseDetail(id);
    setKnowledgeBase(data);

  };
  return (
    <div>
      <Layout className={styles.layout}>
        <Header className={styles.layoutHeader}>
          <div className={styles.logo}>{knowledgeBase?.name}</div>
        </Header>

        <Button type="primary" onClick={showModal} className={styles.knowledgeFileUpload}>
          上传文件
        </Button>
        <Layout>
          <Sider className={styles.layoutLayoutSider} width="15%" theme={"light"}>
            <Title className={styles.siderTitle} level={4}>{knowledgeBase?.name}</Title>
            <Typography.Paragraph className={styles.siderTypography}>
              {knowledgeBase?.description}
            </Typography.Paragraph>
          </Sider>
          <Content style={{padding: '0 50px', display: 'flex', flexWrap: 'wrap', height: 'auto'}}>
            {knowledgeBase?.file_vos.map((file: KnowledgeFileBaseListItemType, index: number) => (
              <div key={index} className={styles.coreContent}>
                <Title level={4}>{file.name}</Title>
                {/*<Typography.Paragraph>
                  文件路径：{file.path}
                </Typography.Paragraph>
                <Typography.Paragraph>
                  OSS路径：{file.oss_path}
                </Typography.Paragraph>*/}
                <Typography.Paragraph>
                  文件大小：{file.size} (Byte)
                </Typography.Paragraph>
                {/*<Button type="primary">前往应用中心或创建问答应用</Button>*/}
              </div>
            ))}
          </Content>
        </Layout>
        <Footer style={{textAlign: 'center'}}>
          知识库详情页面
        </Footer>
      </Layout>
      <KnowledgeFileUploadModal ref={knowledgeFileUploadModal} fetchKnowledgeFileBase={fetchKnowledgeBase}/>
    </div>

  );
};

export default InsurancePage;
