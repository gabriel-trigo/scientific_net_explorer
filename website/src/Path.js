import React from 'react'
import Cell from './Cell'



function cellStyle(index) {
  const colors = ["#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD"]
  return {
    margin: "50",
    padding: "2px",
    backgroundColor: colors[index]
  }
}

console.log(cellStyle(1))

export default function Path({path}) {
  return (
    path.map(function (e, index) {
        return (<td style={cellStyle(index)}>{e}</td>)})
  )
}
