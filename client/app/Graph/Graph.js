import * as d3 from 'd3'
import React, { useRef, useEffect } from 'react';

function Graph({
    nodes, 
    edges
}) {

    // Constants
    const height = 300;
    const width = 300;
    const svgRef = useRef();

    // Mount graph.
    useEffect(() => {

        // Constants.
        var width = 300;
        var height = 300;
        
        // Zoom
        const zoomable = d3
            .select(svgRef.current)
            .call(
                d3.zoom()
                .on('zoom', zoomed)
            )
        zoomable.selectAll("*").remove()
        const svg = zoomable.append('g')

        // Create list of edges
        const links = edges.map((e) => {
            return {
                "source": e["source"]["id"], 
                "target": e["target"]["id"]
        }})

        // Create simulation
        var simulation = d3.forceSimulation()
            .force("link", d3.forceLink().id(function(d) { return d.id; }))
            .force("charge", d3.forceManyBody().strength(-300))
            .force("center", d3.forceCenter(width / 2, height / 2));
        simulation.alpha(0.1)
        simulation.alphaDecay(0)
        simulation.nodes(nodes);
        simulation.force("link").links(links);

        // Create links
        var link = svg.append("g")
            .selectAll("line")
            .data(links)
            .enter()
            .append("line")
            .attr("stroke", "black")
            .attr("stroke-width", 3);

        // Create nodes.
        var node = svg.append("g")
            .selectAll("circle")
            .data(nodes)
            .enter()
            .append("circle")
            .attr("r", 10)
            .attr("fill", "purple");

        // Node labels.
        var nodeLabels = svg
            .append('g')
            .attr('class', 'node-labels')
            .selectAll('text')
            .data(nodes)
            .enter()
            .append('text')
            .attr('x', (d) => d.x + 10)
            .attr('y', (d) => d.y + 10)
            .attr('fill', () => "black")
            .style('font-family', 'Consolas, monospace') // Set the font-family to Consolas
            .text((d) => d.name);

        // Update simulation.
        simulation.on("tick", function() {
            link
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node
                .attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });

            nodeLabels
                .attr('x', (d) => d.x + 10)
                .attr('y', (d) => d.y + 10)
                .text((d) => d.name)

            if (node.id == "30") {
                console.log("hey")
            }
        });
        
        // Add a drag behavior.
        node.call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

        // Reheat the simulation when drag starts, and fix the subject position.
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.01).restart();
            d.fx = d.x;
            d.fy = d.y;
        }

        // Update the subject (dragged node) position during drag.
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }

        // Restore the target alpha so the simulation cools after dragging ends.
        // Unfix the subject position now that it’s no longer being dragged.
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }

        // Zoom.
        function zoomed(event) {
            svg.attr(
              "transform",
              `translate(${event.transform.x}, ${event.transform.y}) scale(${event.transform.k})`
            );
        }

        // Start simulation.
        simulation.alpha(0.1).restart();
    
      }, [nodes, edges])



    return (
        <div className="w-100 bg-slate-300 border border-slate-500 rounded mt-2 h-96">
            <svg
                ref={ svgRef }
                className="h-full w-full">
            </svg>
        </div>
    )
}

export default Graph;