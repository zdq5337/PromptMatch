import React, {useEffect, useState} from 'react';
import {Layout} from 'antd';
import styles from '@/views/knowledge-base/detail/detail.module.less';
import type {ApplicationListItemType} from "./application-types";
import {getApplicationDetail} from "@/api/service/application.ts";
import {useParams} from 'react-router-dom';

const {Header, Footer} = Layout;


const ApplicationCenterDetail: React.FC = () => {
  const id = Number(useParams().id);
  const [application, setApplication] = useState<ApplicationListItemType | null>(null);


  useEffect(() => {
    fetchApplication();
  }, []);


  const fetchApplication = async () => {
    const {data} = await getApplicationDetail(id);
    console.log("data", data)
    setApplication(data);
  };
  return (
    <div>
      <Layout className={styles.layout}>
        <Header className={styles.layoutHeader}>
          <div className={styles.logo}>{application?.name}</div>
        </Header>

        <Footer style={{textAlign: 'center'}}>
          应用中心详情页面
        </Footer>
      </Layout>
    </div>

  );
};

export default ApplicationCenterDetail;
