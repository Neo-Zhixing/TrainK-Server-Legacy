import { Line } from 'vue-chartjs'
export default {
  extends: Line,
  props: ['data'],
  watch: {
    data () {
      var dates = []
      var delays = []
      for (let key in this.data) {
        dates.push(key)
        delays.push(this.data[key])
      }
      console.log('change')
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