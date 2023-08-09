"use client"
import React, { useState, useRef } from "react"
import axios from "axios"
import Graph from "./Graph"
import PathList from "./PathList"

function App() {

  const [graph, setGraph] = useState([])

  // Input references.
  const srcRef = useRef()
  const tgtRef = useRef()

  function fetchPaths() {  

    const srcName = srcRef.current.value
    const tgtName = tgtRef.current.value

    if (srcName === "" || tgtName === "") return

    srcRef.current.value = null
    tgtRef.current.value = null
    
    axios.post(
      "http://127.0.0.1:8000/query", 
      {
        src: srcName, 
        tgt: tgtName
      }
    ).then(response => {
      console.log(response.data["nodes"])
      console.log(response.data["edges"])
      console.log(response.data["paths"])
      setGraph([
        response.data["nodes"], 
        response.data["edges"], 
        response.data["paths"]
      ])
    })
  }

  const titleStyle = {
    textAlign: "center", 
    fontSize: "40px"
  }

  const divStyle = {
    textAlign: "center",
  }

  const descripStyle = {
    textAlign: "center", 
    fontSize: "18px"
  }

  return (
    <>
      <div className="flex items-center mb-6 w-2/3">
        <div className="w-1/4">
          <label className="block text-gray-500 font-bold text-left pr-2" for="inline-full-name">
            Source Author
          </label>
        </div>
        <div className="w-3/4">
          <input className="bg-gray-200 appearance-none border-2 
            border-gray-200 rounded w-full py-2 px-2 text-gray-700 
            leading-tight focus:outline-none focus:bg-white 
            focus:border-purple-500" id="inline-full-name" type="text">
          </input>
        </div>
      </div>
      <div className="flex items-center mb-6 w-2/3">
        <div className="md:w-1/4">
          <label className="block text-gray-500 font-bold text-left pr-2" for="inline-full-name">
            Target Author
          </label>
        </div>
        <div className="w-3/4">
          <input className="bg-gray-200 appearance-none border-2 
            border-gray-200 rounded w-full py-2 px-2 text-gray-700 
            leading-tight focus:outline-none focus:bg-white 
            focus:border-purple-500" id="inline-full-name" type="text">
          </input>
        </div>
      </div>
      <div style={divStyle}>
        <Graph graph={graph}/>
      </div>
      <div>
        <PathList graph={graph}></PathList>
      </div>
    </>
  )
}

export default App;
