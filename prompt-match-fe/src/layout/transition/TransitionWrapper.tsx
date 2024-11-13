import { motion } from 'framer-motion'
import { Outlet, useLocation } from 'react-router-dom'

const TransitionWrapper = () => {
  const location = useLocation()

  return (
    <motion.div
      key={location.pathname}
      initial={{ y: 30, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ ease: 'easeInOut', duration: 0.5 }}
      exit={{ opacity: 0 }}
    >
      <Outlet />
    </motion.div>
  )
}

export default TransitionWrapper
