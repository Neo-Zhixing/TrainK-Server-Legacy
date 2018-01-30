import './map.css'
import * as d3 from 'd3'
import { tubeMap } from 'd3-tube-map'

var container = d3.select('#map-container')

var width = 1200
var height = 1200

var map = tubeMap()
.width(width)
.height(height)
.margin({
  top: height / 50,
  right: width / 7,
  bottom: height / 10,
  left: width / 7
})
.on('click', name => {
  console.log(name)
})
d3.json('/static/pubs.json', (error, data) => {
  console.log(error)
  container.datum(data).call(map)
  var svg = container.select('svg')

  var zoom = d3
    .zoom()
    .scaleExtent([0.5, 6])
    .on('zoom', zoomed)

  var zoomContainer = svg.call(zoom)
  var initialScale = 1
  var initialTranslate = [100, 200]

  zoom.scaleTo(zoomContainer, initialScale)
  zoom.translateTo(zoomContainer, initialTranslate[0], initialTranslate[1])

  function zoomed () {
    svg.select('g').attr('transform', d3.event.transform.toString())
  }
})
