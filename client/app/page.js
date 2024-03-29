"use client"
import InputForm from './InputForm/InputForm'
import Navbartw from './Navbartw'
import React, { useState } from 'react';
import LoadingComponent from './Loading/LoadingComponent'
import Graph from './Graph/Graph'
import { SnackbarProvider } from 'notistack'

export default function Home() {

  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [numAuthors, setNumAuthors] = useState(null);
  const [numPapers, setNumPapers] = useState(null);

  return (
    <>
      <Navbartw></Navbartw>
      <main className="flex items-center text-black top-12">
        <div className="w-1/2 text-left mx-auto relative top-20">
          <h1 className="font-bold font-sans text-3xl pb-2">
            Academic Network Explorer
          </h1>
          <p className="text-justify pb-4">
            Hi, this is a website made as a fun project to explore coauthorship graphs
            between scientific authors. The information shown here is 
            provided by the <a>Semantic Scholar API</a>, and you can check 
            out the entire code here.
          </p>
          <InputForm
            setNodes={ setNodes }
            setEdges={ setEdges }
            setIsLoading={ setIsLoading }
            isLoading={ isLoading }
            setNumAuthors={ setNumAuthors }
            setNumPapers={ setNumPapers }>  
          </InputForm>
          <div>
            { 
              numAuthors == null ? <></> 
              : 
              <LoadingComponent numAuthors={ numAuthors } isLoading={ isLoading } numPapers={ numPapers }/> 
            }
            <Graph nodes={ nodes } edges={ edges }/>
          </div>
        </div>
        <SnackbarProvider/>
      </main>
    </>
  )
}
