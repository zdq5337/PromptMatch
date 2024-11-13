import ReactDOM from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import router from './router'
// 重置浏览器默认样式
import 'normalize.css'

ReactDOM.createRoot(document.getElementById('root')!).render(<RouterProvider router={router} />)
