import { min, max } from 'd3-array'
import { scaleLinear } from 'd3-scale'
function extractLines (data) {
  var lines = []

  data.forEach(function (line) {
    var lineObj = {
      name: line.name,
      title: line.label,
      stations: [],
      color: line.color,
      shiftCoords: line.shiftCoords,
      nodes: line.nodes,
      highlighted: false
    }

    lines.push(lineObj)

    for (var node = 0; node < line.nodes.length; node++) {
      var data = line.nodes[node]

      if (!data.hasOwnProperty('name')) continue

      lineObj.stations.push(data.name)
    }
  })

  return lines
}

export default class {
  constructor (data) {
    this.margin = { top: 80, right: 80, bottom: 20, left: 80 }
    this.width = 760
    this.height = 640
    this.lineWidthMultiplier = 0.8
    this.lineWidthTickRatio = 3 / 2
    this.lines = extractLines(data.lines)
    this.rivers = data.river
    this.raw = data.lines

    // Calculating minX, minY, maxX, maxY
    let fs = {'min': min, 'max': max}
    for (let key of ['min', 'max']) {
      for (let co of [0, 1]) {
        let name = key + ['X', 'Y'][co]
        let handler = fs[key]
        this[name] = handler(data.lines, line => handler(line.nodes, node => node.coords[co]))
      }
    }
    let desiredAspectRatio = (this.maxX - this.minX) / (this.maxY - this.minY)
    let actualAspectRatio =
      (this.width - this.margin.left - this.margin.right) /
      (this.height - this.margin.top - this.margin.bottom)
    let ratioRatio = actualAspectRatio / desiredAspectRatio

    // Note that we flip the sense of the y-axis here
    if (desiredAspectRatio > actualAspectRatio) {
      this.maxXRange = this.width - this.margin.left - this.margin.right
      this.maxYRange = (this.height - this.margin.top - this.margin.bottom) * ratioRatio
    } else {
      this.maxXRange = (this.width - this.margin.left - this.margin.right) / ratioRatio
      this.maxYRange = this.height - this.margin.top - this.margin.bottom
    }

    this.xScale = scaleLinear().domain([this.minX, this.maxX]).range([this.margin.left, this.margin.left + this.maxXRange])
    this.yScale = scaleLinear().domain([this.minY, this.maxY]).range([this.margin.top + this.maxYRange, this.margin.top])
    this.lineWidth = this.lineWidthMultiplier * (this.xScale(1) - this.xScale(0))
  }
}
