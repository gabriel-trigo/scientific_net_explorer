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
      <div style={divStyle}>
        <input type="text" ref={srcRef} name="Source"/>
        <input type="text" ref={tgtRef} name="Target"/>
        <button className="bg-purple-500 hover:bg-purple-400 border-b-4 border-purple-800 px-3 py-1 text-white font-semibold rounded" onClick={fetchPaths}>Submit</button>
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
