/* eslint-disable @typescript-eslint/no-explicit-any */
import React from 'react'
import * as Icons from '@ant-design/icons'

interface DynamicIconProps {
  type: string

  [key: string]: any
}

const DynamicIcon: React.FC<DynamicIconProps> = ({type, ...props}) => {
  let IconComponent = (Icons as any)[type]

  if (!IconComponent) {
    IconComponent = (Icons as any)['ToolFilled']
    return <IconComponent {...props} />
  }

  return <IconComponent {...props} />
}

export default DynamicIcon
