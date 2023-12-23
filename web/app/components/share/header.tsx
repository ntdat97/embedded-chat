import type { FC } from 'react'
import React from 'react'
import {
  Bars3Icon,
  ChevronRightIcon,
  PencilSquareIcon,
} from '@heroicons/react/24/solid'
import cn from 'classnames'
import { useTranslation } from 'react-i18next'
import Avatar from '../base/avatar'
import AppIcon from '@/app/components/base/app-icon'

export type IHeaderProps = {
  title: string
  customerIcon?: React.ReactNode
  icon: string
  icon_background: string
  isMobile?: boolean
  isEmbedScene?: boolean
  hasSetInputs?: boolean
  onShowSideBar?: () => void
  onCreateNewChat?: () => void
  isShowSidebar?: boolean
}
const Header: FC<IHeaderProps> = ({
  title,
  isMobile,
  customerIcon,
  icon,
  icon_background,
  isEmbedScene = false,
  onShowSideBar,
  onCreateNewChat,
  hasSetInputs,
  isShowSidebar,
}) => {
  console.log(hasSetInputs)
  const { t } = useTranslation()
  if (!isMobile)
    return null
  if (isEmbedScene) {
    return (
      <div className={cn((!isShowSidebar) ? 'h-[70px] items-center justify-start' : 'h-[150px] items-center justify-center', 'shrink-0 flex  transition-all px-2 bg-[#1972F5]')}>
        {(!isShowSidebar)
          && <button
            className='flex items-center justify-center transition hover:bg-[#00000033] min-h-[40px] min-w-[40px] rounded-[10px] mr-4'
            onClick={() => onShowSideBar?.()}
          >
            <ChevronRightIcon className='rotate-180 cursor-pointer' width="30" height="30" fill='white' strokeWidth="4px" />
          </button>
        }

        <div className='flex flex-col text-white items-center gap-y-2'>
          {/*         <AppIcon size="small" icon={icon} background={icon_background} /> */}
          {!(!isShowSidebar) && <div className=" text-sm  font-bold">Qustion? Chat with us</div>}
          <div className='flex flex-row items-center justify-between gap-x-4'>
            <div className={cn((!isShowSidebar) ? 'flex-row gap-x-3' : 'flex-col', 'transition-all flex items-center justify-between')}>
              <Avatar name='defaultAvatar' avatar='/logo/logo-no-background.svg' className='bg-white' size={40} />
              <div className=" text-sm   font-bold">{title}</div>
            </div>
            <div className={cn((!isShowSidebar) ? 'invisible' : 'visible', 'flex flex-col items-center justify-between')}>
              <Avatar name='defaultAvatar' avatar='/logo/logo-no-background.svg' className='bg-white' size={40} />
              <div className=" text-sm   font-bold">Supporters</div>
            </div>
          </div>

          {!(!isShowSidebar) && <div className=" text-sm  font-bold opacity-75">Typically replies under an hour</div>}
        </div>
        {/*       <div className='flex items-center justify-center min-h-[48px] min-w-[48px]' /> */}

      </div>
    )
  }

  return (
    <div className="shrink-0 flex items-center justify-between h-14 px-4 bg-gray-100">
      <div
        className='flex items-center justify-center h-8 w-8 cursor-pointer'
        onClick={() => onShowSideBar?.()}
      >
        <Bars3Icon className="h-4 w-4 text-gray-500" />
      </div>
      <div className='flex items-center space-x-2'>
        <AppIcon size="small" icon={icon} background={icon_background} />
        <div className=" text-sm text-gray-800 font-bold">{title}</div>
      </div>
      <div className='flex items-center justify-center h-8 w-8 cursor-pointer'
        onClick={() => onCreateNewChat?.()}
      >
        <PencilSquareIcon className="h-4 w-4 text-gray-500" />
      </div>
    </div>
  )
}

export default React.memo(Header)
