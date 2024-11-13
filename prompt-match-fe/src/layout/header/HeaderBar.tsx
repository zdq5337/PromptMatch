/*
 * @Description: header
 * @Author: Kyeoni hujr
 * @Date: 2024-05-16 16:22:28
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-05-17 14:22:50
 */
import { useLocation, useNavigate } from 'react-router-dom'
import './header-style.less'
import { useEffect, useState } from 'react'

export default function HeaderBar() {
  const menuList = [
    {
      name: '知识库',
      router: '/knowledge-base'
    },
    // {
    //   name: '应用中心',
    //   router: '/application-center'
    // },

    {
      name: '模型决斗场',
      router: '/model-prompt'
    }
  ]
  const [activeRouter, setActiveRouter] = useState('')
  // doc: https://reactrouter.com/en/main/hooks/use-location
  // 此方法用于获取当前路由
  const location = useLocation()
  // doc: https://reactrouter.com/en/main/hooks/use-navigate
  // 导航
  const navigate = useNavigate()
  // 【有道云笔记】2-ReactHook-useEffect.md  https://note.youdao.com/s/3pLh2Oor
  // 官方文档 https://react.docschina.org/reference/react/useEffect
  useEffect(() => {
    setActiveRouter(location.pathname)
  }, [location])

  function handleMenuClick(router: string) {
    navigate(router)
  }
  return (
    <header className='header-bar'>
      <div className='header-bar-container'>
        <div className='header-bar-logo'>TITAN</div>
        <div className='header-bar-menu'>
          {menuList.map(menu => (
            <div
              className={`menu-item ${activeRouter === menu.router && 'menu-item-active'}`}
              key={menu.router}
              onClick={() => handleMenuClick(menu.router)}
            >
              {menu.name}
            </div>
          ))}
        </div>
        <div className='header-bar-login'>
          {/*登录<span aria-hidden='true'>→</span>*/}
        </div>
      </div>
    </header>
  )
}
