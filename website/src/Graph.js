import React, {useState} from 'react'
import * as d3 from 'd3'

export default function Graph({graph}) {

  const svgRef = React.useRef()

  var height = 800
  var width = 1000



  const color = d3.scaleOrdinal(d3.schemeCategory10)

  React.useEffect(() => {
    
    if (graph.length === 0) return

    const zoomable = d3
      .select(svgRef.current)
      .call(
        d3.zoom()
        .on('zoom', zoomed))
    
    zoomable.selectAll("*").remove()

    const svg = zoomable.append('g')

    var simulation = d3.forceSimulation(graph[0])
      .force("link", d3.forceLink().id((d) => d.id).links(graph[1]))
      .force("center", d3.forceCenter(width / 2, height / 2))                  
      .force("charge", d3.forceManyBody().strength(-800))
      .on('tick', ticked)
    
    var link = svg
      .append('g')
      .attr('class', 'links')
      .selectAll('line')
      .data(graph[1])
      .enter()
      .append('line')
      .attr('stroke-width', 3)
      .style('stroke', 'pink')

    var node = svg
      .append('g')
      .selectAll('circle')
      .data(graph[0])
      .enter()
      .append('circle')
      .attr('r', 10)
      .attr('fill', (d) => color(d.dist))
      .call(
        d3
          .drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended)
      );

    // Node labels.
    var nodeLabels = svg
      .append('g')
      .attr('class', 'node-labels')
      .selectAll('text')
      .data(graph[0])
      .enter()
      .append('text')
      .attr('x', (d) => d.x + 10)
      .attr('y', (d) => d.y + 10)
      .text((d) => d.name);

    function ticked() {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y)

      node
        .attr('cx', (d) => d.x)
        .attr('cy', (d) => d.y)

      nodeLabels
        .attr('x', (d) => d.x + 10)
        .attr('y', (d) => d.y + 10)
    }

    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    function zoomed(event) {
      svg.attr(
        "transform",
        `translate(${event.transform.x}, ${event.transform.y}) scale(${event.transform.k})`
      );
    }

  }, [graph, width, height, color])

  const svgStyle = {
    marginLeft: "auto", 
    marginRight: "auto", 
    display: "block",
    border: '1px solid black'
  }

  if (graph.length === 0) return

  return (
    <>
      <svg style={svgStyle}
        ref={svgRef} 
        width={width} 
        height={height}>
      </svg>
    </>
  )
}
