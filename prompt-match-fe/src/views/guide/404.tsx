import {Button, Result} from 'antd'
import {useNavigate} from 'react-router-dom'

export default function NotFound() {
  const navigate = useNavigate()
  const handleBackToHomeClick = () => {
    navigate('/')
  }
  return (
    <Result
      status='404'
      title='404'
      subTitle='您访问的页面不存在'
      extra={
        <Button onClick={handleBackToHomeClick} type='primary'>
          返回主页
        </Button>
      }
    />
  )
}
