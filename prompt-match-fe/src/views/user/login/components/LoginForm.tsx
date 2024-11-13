/*
 * @Description: 登录表单
 * @Author: Kyeoni hujr
 * @Date: 2024-09-10 15:54:20
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-09-11 11:43:46
 */
import { Form, Input, ConfigProvider, Button } from 'antd'
import type { FormProps } from 'antd'
import styles from '../login.module.less'
import type { UserLoginForm } from '../../user-types'
import { userLogin } from '@/api/service/user'

export default function LoginForm() {
  const [form] = Form.useForm()
  const onFinish: FormProps<UserLoginForm>['onFinish'] = values => {
    console.log('Success:', values)
    userLogin(values).then(({ data }) => {
      //   {
      //     "code": "000000",
      //     "message": "请求成功！",
      //     "data": {
      //         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Imt5ZW9uNiIsInJvbGUiOiJ1c2VyIiwiaWQiOjYsImV4cCI6MTcyNjYyNzQ2Mn0.jLjZ180sM-Hs9-fN02niWsJVQUl1tLloPosNzFNPR1g",
      //         "token_type": "bearer",
      //         "username": "kyeon6",
      //         "role": "user",
      //         "last_login_time": "2024-09-10T09:33:52",
      //         "create_time": "2024-09-10T09:33:52",
      //         "id": 6
      //     },
      //     "timestamp": 1726022662471
      // }
      console.log('res',data);
    })
  }
  return (
    <>
      <div className={styles.loginFormOfComponent}>
        <ConfigProvider
          theme={{
            components: {
              Input: {
                activeBorderColor: 'rgba(0, 0, 0, 0.28)',
                activeShadow:
                  'rgba(0, 0, 0, 0.28) 0px 0px 0px 1px, rgba(0, 0, 0, 0.11) 0px 0px 1px 0px, rgba(0, 0, 0, 0.11) 0px 0px 0px 4px;',
                hoverBorderColor: 'rgba(0, 0, 0, 0.28)'
              }
            }
          }}
        >
          <Form
            form={form}
            layout='vertical'
            name='login'
            initialValues={{ remember: true }}
            size='large'
            onFinish={onFinish}
          >
            <Form.Item<UserLoginForm>
              name='username'
              rules={[
                { required: true, message: '请输入用户名' },
                {
                  validator: async (_, username) => {
                    if (!/^[A-Za-z\d_]{5,10}$/.test(username)) {
                      return Promise.reject(new Error('用户名由字母数字下划线组成，长度为5-10位'))
                    }
                  }
                }
              ]}
            >
              <div>
                <div className={styles.formFieldTitle}>用户名</div>
                <Input placeholder='请输入用户名' />
              </div>
            </Form.Item>
            <Form.Item<UserLoginForm>
              name='password'
              rules={[
                { required: true, message: '请输入密码' },
                {
                  validator: async (_, password) => {
                    if (
                      !/^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()_\-+\\,.?":{}|<>])[A-Za-z\d!@#$%^&*()_\-+\\,.?":{}|<>]{8,}$/.test(
                        password
                      )
                    ) {
                      return Promise.reject(
                        new Error('密码必须包含字母、数字和特殊字符，长度不能小于8位')
                      )
                    }
                  }
                }
              ]}
            >
              <div>
                <div className={styles.formFieldTitle}>密码</div>
                <Input.Password placeholder='请输入密码' />
              </div>
            </Form.Item>
            <Button
              style={{ marginTop: '1rem' }}
              type='primary'
              htmlType='submit'
              block
              size='large'
            >
              继续
            </Button>
          </Form>
        </ConfigProvider>
      </div>
    </>
  )
}
