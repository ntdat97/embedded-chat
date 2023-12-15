import { ProviderEnum } from '../declarations'
import type { ProviderConfig } from '../declarations'
import { Gemini } from '@/app/components/base/icons/src/public/llm'

const config: ProviderConfig = {
  selector: {
    name: {
      'en': 'Gemini',
      'zh-Hans': 'Gemini',
    },
    icon: <Gemini className='w-full h-full' />,
  },
  item: {
    key: ProviderEnum.gemini,
    titleIcon: {
      'en': <div className='flex flex-row gap-1'><Gemini className='w-[24px] h-6' /><div className='font-semibold'>Gemini</div></div>,
      'zh-Hans': <Gemini className='w-[24px] h-6' />,
    },
    subTitleIcon: <Gemini className='w-6 h-6' />,
    desc: {
      'en': 'Gemini: Google AI scalpel, dissecting data, crafting breakthroughs.',
      'zh-Hans': 'Gemini: Google AI scalpel, dissecting data, crafting breakthroughs.',
    },
    bgColor: 'bg-[#F0F0EB]',
    hit: {
      'en': 'Build with Gemini',
      'zh-Hans': 'Build with Gemini',
    },
  },
  modal: {
    key: ProviderEnum.gemini,
    title: {
      'en': 'Gemini API Key',
      'zh-Hans': 'Gemini API Key',
    },
    icon: <Gemini className='w-[58px] h-6' />,
    link: {
      href: 'https://ai.google.dev/',
      label: {
        'en': 'Get your API key from Google AI Studio',
        'zh-Hans': 'Get your API key from Google AI Studio',
      },
    },
    validateKeys: ['google_api_key'],
    fields: [
      {
        type: 'text',
        key: 'google_api_key',
        required: true,
        label: {
          'en': 'Gemini API Key',
          'zh-Hans': 'Gemini API Key',
        },
        placeholder: {
          'en': 'Enter your API key here',
          'zh-Hans': '在此输入您的 API Key',
        },
      },
    ],
  },
}

export default config
