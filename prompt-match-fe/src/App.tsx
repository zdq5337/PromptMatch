import {useState} from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [userName, setUserName] = useState('Kyeon')
  const title = 'Vite + React!'
  const welcome = <h3>欢迎Welcome!</h3>
  const isAdmin = true
  // const userName = <span style={{ color: 'teal', fontSize: 22 }}>kyeon</span>
  const list = ['book1', 'book2', 'book3']
  const handleUpdateUserName = () => {
    setUserName(userName + Math.random())
  }

  return (
    <>
      <div>
        <a href='https://vitejs.dev' target='_blank'>
          <img src={viteLogo} className='logo' alt='Vite logo'/>
        </a>
        <a href='https://react.dev' target='_blank'>
          <img src={reactLogo} className='logo react' alt='React logo'/>
        </a>
      </div>
      <h1>{title}</h1>
      {welcome}
      {isAdmin ? <span>您好，管理员{userName}</span> : <span>普通访客</span>}
      <p onClick={handleUpdateUserName}>
        {/* forEach map reduce  */}
        {list.map(item => (
          <div key={item}>{item}</div>
        ))}
      </p>
      <div className='card'>
        <button onClick={() => setCount(count => count + 1)}>count is {count}</button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className='read-the-docs'>Click on the Vite and React logos to learn more</p>
    </>
  )
}

export default App
