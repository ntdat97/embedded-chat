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
      'en': <Gemini className='w-[24px] h-6' />,
      'zh-Hans': <Gemini className='w-[24px] h-6' />,
    },
    hit: {
      'en': 'Build with Gemini',
      'zh-Hans': 'Build with Gemini',
    },
  },
  modal: {
    key: ProviderEnum.gemini,
    title: {
      'en': 'Gemini API Key',
      'zh-Hans': 'Embedding 模型',
    },
    icon: <Gemini className='w-[58px] h-6' />,
    link: {
      href: 'https://ai.google.dev/',
      label: {
        'en': 'Get your API key from Google AI Studio',
        'zh-Hans': 'Get your API key from Google AI Studio',
      },
    },
    validateKeys: ['gemini_api_key'],
    fields: [
      {
        type: 'text',
        key: 'gemini_api_key',
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
