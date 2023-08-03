import Image from 'next/image'
import App from './App'
import Navbartw from './Navbartw'

export default function Home() {
  return (
    <>
      <Navbartw></Navbartw>
      <main className="flex items-center text-black top-12">
        <div className="w-1/2 text-left mx-auto relative top-20">
          <h1 className="font-semibold text-3xl">
            Academic Network Explorer
          </h1>
            Hey there my old friend how are you doing in this fine evening
          <App></App>
        </div>
      </main>
    </>
  )
}
