import React from 'react';
import {Input, Layout} from 'antd';
import styles from './model_prompt.module.less';

const { Sider, Content } = Layout;

const MyLayout = () => (
  <Layout className={styles.layoutStyle}>
    <Sider width="20%" className={styles.siderStyle} style={{background: '#ff7f50'}}> {/* 设置左侧背景颜色 */}
      {/* 在这里添加你的左侧内容 */}
      <div className={styles.siderItem}>
        <div className={styles.promptItemTitle}>
          提示变量
        </div>
        <div className={styles.promptItem}>
          <Input placeholder="请输入您要定义的变量"/>
        </div>
      </div>
      <div className={styles.siderItem}>22222222222222222222222222222222</div>
      <div className={styles.siderItem}>3333333333333333333333333333</div>
      <div className={styles.siderItem}>444444444444444444444444444444444</div>
      <div className={styles.siderItem}>555555555555555555555555555555555</div>
      <div className={styles.siderItem}>666666666666666666666666666666666</div>
      <div className={styles.siderItem}>777777777777777777777777777777777777</div>
      <div className={styles.siderItem}>777777777777777777777777777777777777</div>
      <div className={styles.siderItem}>777777777777777777777777777777777777</div>
    </Sider>
    <Content style={{background: '#87cefa', padding: '0 50px'}}> {/* 设置右侧背景颜色 */}
      {/* 在这里添加你的右侧内容 */}
    </Content>
  </Layout>
);

export default MyLayout;
