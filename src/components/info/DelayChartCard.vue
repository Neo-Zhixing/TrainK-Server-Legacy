<template>
  <b-card header="正晚点" :title="title" :sub-title="subtitle" >
    <delay-chart :data="delays"></delay-chart>
    <slot name="footer" />
  </b-card>
</template>
<script>
import axios from 'axios'
import { Line } from 'vue-chartjs'
export default {
  props: ['telecode'],
  data () {
    return {
      delays: null
    }
  },
  computed: {
    avgDelay () {
      if (this.delays === null) return 0
      var avgDelay = 0
      for (let value of this.delays.values()) avgDelay += value
      return avgDelay / this.delays.size
    },
    titleIndex () {
      if (this.avgDelay > 90) return 0
      else if (this.avgDelay > 30) return 1
      else if (this.avgDelay > 5) return 2
      else return 3
    },
    title () {
      console.log(this.avgDelay)
      return ['不在一个时区', '生活习惯问题', '一般不会迟到', '小嘛小火车'][this.titleIndex]
    },
    subtitle () {
      return ['搭车前请自行调整时钟', '适度迟到是礼貌的一种表现形式', '除非家里有事', '不怕太阳晒，不怕风雪狂'][this.titleIndex]
    }
  },
  mounted () {
    axios.get(`/info/train/${this.telecode}/record/`)
    .then((response) => {
      var delays = new Map()
      for (let result of response.data.results) delays.set(result.departureDate, result.delay)
      this.delays = delays
    })
    .catch(function (error) {
      console.log(error)
    })
  },
  components: {
    DelayChart: {
      extends: Line,
      props: ['data'],
      watch: {
        data () {
          if (this.data === null) return
          var dates = []
          var delays = []
          console.log(this.data)
          for (let [key, value] of this.data) {
            dates.push(key)
            delays.push(value)
          }
          this.renderChart({
            labels: dates,
            datasets: [
              {
                label: '平均晚点',
                backgroundColor: '#f87979',
                data: delays
              }
            ]
          }, {
            responsive: true,
            maintainAspectRatio: false
          })
        }
      }
    }
  }
}
</script>