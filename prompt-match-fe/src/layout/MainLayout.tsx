/*
 * @Description: Layout模版
 * @Author: Kyeoni hujr
 * @Date: 2024-05-16 11:01:11
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-05-17 14:22:30
 */
import { Outlet } from 'react-router-dom'
import HeaderBar from './header/HeaderBar'
import { AnimatePresence } from 'framer-motion'

export default function Layout() {
  return (
    <>
      <HeaderBar />
      <AnimatePresence mode='wait'>
        <Outlet />
      </AnimatePresence>
    </>
  )
}
