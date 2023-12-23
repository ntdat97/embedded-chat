'use client'
import type { FC } from 'react'
import React, { useRef } from 'react'
import cn from 'classnames'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import { ChatBubbleOvalLeftEllipsisIcon as ChatBubbleOvalLeftEllipsisSolidIcon } from '@heroicons/react/24/solid'
import {
  ChatBubbleOvalLeftEllipsisIcon,
} from '@heroicons/react/24/outline'
import { useHover } from 'ahooks'
import ItemOperation from '@/app/components/explore/item-operation'
import type { ConversationItem } from '@/models/share'
import Avatar from '@/app/components/base/avatar'

dayjs.extend(relativeTime)

export type IItemProps = {
  onClick: (id: string) => void
  item: ConversationItem
  isCurrent: boolean
  isPinned: boolean
  togglePin: (id: string) => void
  onDelete: (id: string) => void
  onRenameConversation: (item: ConversationItem) => void
}

const Item: FC<IItemProps> = ({
  isCurrent,
  item,
  onClick,
  isPinned,
  togglePin,
  onDelete,
  onRenameConversation,
}) => {
  console.log(item)
  const ItemIcon = isCurrent ? ChatBubbleOvalLeftEllipsisSolidIcon : ChatBubbleOvalLeftEllipsisIcon
  const ref = useRef(null)
  const isHovering = useHover(ref)

  return (
    <div
      ref={ref}
      onClick={() => onClick(item.id)}
      key={item.id}
      className={cn(
        isCurrent
          ? 'bg-primary-50 text-primary-600'
          : 'text-gray-700 hover:bg-gray-200 hover:text-gray-700',
        'group flex justify-between items-center rounded-md px-5 py-4 text-sm font-medium cursor-pointer',
      )}
    >
      <div className='flex items-center w-0 grow'>
        <Avatar name='defaultAvatar' avatar='/logo/logo-no-background.svg' className={cn(
          isCurrent
            ? 'text-primary-600'
            : 'text-gray-400 group-hover:text-gray-500',
          'mr-3 h-5 w-5 flex-shrink-0 bg-white',
        )} size={40} />
        {/*  <ItemIcon
          className={}
          aria-hidden="true"
        /> */}
        <div className='flex flex-col gap-x-2 justify-center items-start '>
          <div >{item.name}</div>
          <div className='font-normal text-sm text-[#666666]'>{item.created_at ? dayjs(Number(item.created_at) * 1000).fromNow() : ''}</div>
        </div>
      </div>

      {item.id !== '-1' && (
        <div className='shrink-0 h-6' onClick={e => e.stopPropagation()}>
          <ItemOperation
            isPinned={isPinned}
            isItemHovering={isHovering}
            togglePin={() => togglePin(item.id)}
            isShowDelete
            isShowRenameConversation
            onRenameConversation={() => onRenameConversation(item)}
            onDelete={() => onDelete(item.id)}
          />
        </div>
      )}
    </div>
  )
}
export default React.memo(Item)
