import Apps from './Apps'

const AppList = async () => {
  return (
    <div className='flex flex-col overflow-auto bg-gray-100 shrink-0 grow'>
      <Apps />
    </div >
  )
}

export default AppList
