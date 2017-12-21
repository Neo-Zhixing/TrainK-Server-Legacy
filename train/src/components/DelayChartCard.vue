<template>
  <b-card header="正晚点" :title="title" :sub-title="subtitle" >
    <delay-chart :data="delays"></delay-chart>
    <b-button variant="primary" :href="'/query/record?telecode=' + telecode">查看历史记录</b-button>
  </b-card>
</template>
<script>
import axios from 'axios'
import DelayChart from './DelayChart'
export default {
  props: ['telecode'],
  data (){
    return {
      delays: {}
    }
  },
  computed: {
    avgDelay () {
      var avgDelay = 0
      for(let key of Object.values(this.delays)){
        avgDelay += this.delays[key] 
      }
      return avgDelay / this.delays.length
    },
    titleIndex () {
      if(this.avgDelay > 90) return 0
      else if(this.avgDelay > 30) return 1
      else if(this.avgDelay > 5) return 2
      else return 3
    },
    title () {
      return ['不在一个时区', '生活习惯问题', '一般不会迟到', '小嘛小火车'][this.titleIndex]
    },
    subtitle () {
      return ['搭车前请自行调整时钟', '适度迟到是礼貌的一种表现形式', '除非家里有事', '不怕太阳晒，不怕风雪狂'][this.titleIndex]
    }
  },
  mounted() {
    axios.get('/query/record', {
        params: {
          'telecode': this.telecode,
          'recent': '30',
          'actions': 'analysis'
        }
      })
      .then((response) => {
        var delays = {}
        for (let result of response.data.results) delays[result.departureDate] = result.delayAvg
        this.delays = delays
      })
      .catch(function (error) {
        console.log(error)
      })
  },
  components: {
  	DelayChart
  }
}
</script>