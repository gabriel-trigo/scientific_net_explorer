# scientific_net_explorer
A website that finds and visualize shortest coauthorship paths between authors of academic papers. This was heavily inspired by the website [Six Degrees of Wikipedia](https://www.sixdegreesofwikipedia.com/), which finds shortest paths between Wikipedia pages.

![](https://github.com/gabriel-trigo/erdos_path/blob/master/gifs/demo.gif)

# How it works
When names are inputed into the search boxes, the website (implemented with [React](https://reactjs.org/)) sends a ```POST``` request to a backend [Flask](https://flask.palletsprojects.com/en/2.2.x/) server that queries the [Semantic Scholar API](https://www.semanticscholar.org/product/api) and performs two breadth first searches, one starting from the source author and the other starting from the sink author. The two BFSs run until they:
  1. Have found at least one common node (and thus a path) and have exhausted all the other possible paths of same length.
  2. The search trees have reached the maximum number of API calls allowed by the API. 

Once the shortest paths are found, the server responds the request with the graph information, which is then displayed by the website with [D3.js](https://d3js.org/)
