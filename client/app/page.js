"use client"
import Image from 'next/image'
import App from './App'
import InputForm from './InputForm'
import Navbartw from './Navbartw'
import React, { useState } from 'react';

export default function Home() {

  const [graph, setGraph] = useState(null);

  return (
    <>
      <Navbartw></Navbartw>
      <main className="flex items-center text-black top-12">
        <div className="w-1/2 text-left mx-auto relative top-20">
          <h1 className="font-bold font-sans text-3xl pb-2">
            Academic Network Explorer
          </h1>
          <p className="text-justify pb-4">
            Hey there my old friend how are you doing in this fine evening testing just
            how wide my container is wow it is very wide hot damnnnnn just checking if my 
            text really is justified you know you never know bro let's just be sure dayumm
            hey
          </p>
          <InputForm
            setGraph={setGraph}>  
          </InputForm>
        </div>
      </main>
    </>
  )
}
