import React from 'react'
import Path from "./Path"

const tableStyle = {
  border: '1px solid black',
  margin: 'auto'
}

const headerStyle = {
  borderBottom: "1px dashed grey",
  textAlign: "center", 
  padding: "10px"
}

export default function PathList({graph}) {

  if (graph.length === 0) return

  return (
    <table style={tableStyle}>
      <thead>
        <tr>
          {graph[2][0].map(function(element, index) {
            return (<td style={headerStyle}>{index}</td>)})
          }
        </tr>
      </thead>
      <tbody>
        {graph[2].map(path => {
          return (<tr>
            <Path path={path}/>
          </tr>)})}
      </tbody>
    </table>
  )
}
