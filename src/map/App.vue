<template>
  <svg v-if="map" style="width: 100%; height: 100%;">
    <g>
      <path
        :d="drawRiver(map.rivers)"
        stroke="#CCECF4"
        fill='none'
        :stroke-width="1.8*map.lineWidth"
      />
    </g>
    <g>
      <path
      v-for="line in map.lines"
      :d="drawRiver(line)"
      :stroke="line.color"
      fill="none"
      :stroke-width="line.highlighted ? map.lineWidth * 1.3 : map.lineWidth"
      />
    </g>
  </svg>
  <div v-else>
    Loading
  </div>
</template>

<script>
import Leaflet from 'vue2-leaflet'
import 'leaflet/dist/leaflet.css'
import { line } from './curve'
import axios from '@/utils/axios'
import MapData from './data'
export default {
  data () {
    return {
      map: null
    }
  },
  mounted () {
    axios.get('/static/pubs.json')
    .then(response => {
      console.log(response.data)
      this.map = new MapData(response.data)
    })
  },
  methods: {
    drawRiver (data) {
      return line(data, this.map.xScale, this.map.yScale, this.map.lineWidth, this.map.lineWidthTickRatio)
    }
  },
  components: {
    'v-map': Leaflet.Map,
    'v-tilelayer': Leaflet.TileLayer,
    'v-marker': Leaflet.Marker
  }
}
</script>

<style>
html, body {
  height: 100%;
}
#map-container {
  width:100%;
  height:100%;
}

</style>
