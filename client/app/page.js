import Image from 'next/image'
import App from './App'

export default function Home() {
  return (
    <main className="grid place-items-center font-mono
       text-black bg-amber-60 w-full h-full">
      <div className="w-1/2 relative top-20">
        <h1 className="font-semibold text-3xl">
          Academic Network Explorer
        </h1>
        Hey there my old friend how are you doing in this fine evening
        <App></App>
      </div>
    </main>
  )
}
