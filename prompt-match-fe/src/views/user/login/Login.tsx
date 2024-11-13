/*
 * @Description: 登录页面
 * @Author: Kyeoni hujr
 * @Date: 2024-09-10 10:51:04
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-09-10 15:55:09
 */
import styles from './login.module.less'
import signInBg from './images/signin-bg.jpg'
import LoginForm from './components/LoginForm';

export default function Login() {
  return (
    <>
      <div className={styles.loginWrapper}>
        <div className={styles.loginBackgroundWrapper}>
          <img className={styles.loginBackground} src={signInBg} />
        </div>
        <div className={styles.loginMain}>
          <div className={styles.loginContent}>
            <div className={styles.loginContentTop}>
              <div className={styles.loginContentMain}>
                <div className={styles.loginContentMainLeft}>
                {/* 左侧内容 */}
                </div>
                <div className={styles.loginContentMainRight}>
                  <div className={styles.loginFormWrapper}>
                    <div className={styles.loginFormWrapperInner}>
                      <div className={styles.loginFormWrapperInnerNext}>
                        <LoginForm />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
