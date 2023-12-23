import type { FC } from 'react'
import React from 'react'

import type { IMainProps } from '@/app/components/share/chat/embedded'
import Main from '@/app/components/share/chat/embedded'

const Chatbot: FC<IMainProps> = () => {
  return (
    <Main />
  )
}

export default React.memo(Chatbot)
