/*
 * @Description: 路由注册文件
 * @Author: Kyeoni hujr
 * @Date: 2024-02-06 14:43:25
 * @LastEditors: Kyeoni hujr
 * @LastEditTime: 2024-09-10 10:53:00
 */
import { Navigate } from 'react-router-dom'
import NotFound from '@/views/guide/404'
import MainLayout from '@/layout/MainLayout.tsx'
import KnowledgeBaseList from '@/views/knowledge-base/list/List'
import ApplicationCenter from '@/views/application-center/List.tsx'
import ApplicationCenterDetail from '@/views/application-center/Detail.tsx'
import TransitionWrapper from '@/layout/transition/TransitionWrapper'
import KnowledgeBaseDetail from "@/views/knowledge-base/detail/Detail";
import ModelPrompt from "@/views/prompt-match/ModelPrompt.tsx";
import ResizableGrid from "@/views/prompt-match/Table.tsx";
import Login from "@/views/user/login/Login";

export default [
  {
    path: '*',
    element: <Navigate to='/404' />
  },
  {
    path: '/404',
    element: <NotFound />
  },
  {
    path: '/',
    element: <Navigate to='/knowledge-base' />
  },
  {
    path: '/login',
    element: <Login />
  },
  {
    element: <MainLayout />,
    children: [
      {
        element: <TransitionWrapper />,
        children: [
          {
            path: '/knowledge-base',
            element: <KnowledgeBaseList />
          },
          {
            path: '/application-center',
            element: <ApplicationCenter />
          },
          {
            path: '/knowledge-base/detail/:id',
            element: <KnowledgeBaseDetail />
          },
          {
            path: '/model-prompt',
            element: <ModelPrompt />
          },
          {
            path: '/model-prompt-table',
            element: <ResizableGrid />
          },
          {
            path: '/application-center/detail/:id',
            element: <ApplicationCenterDetail />
          }
        ]
      }
    ]
  }
]
