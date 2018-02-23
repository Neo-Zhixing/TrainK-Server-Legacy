<template>
  <b-modal lazy ref="submissionQueueModal" title="订单排队中"
    ok-only :ok-disabled="!error" @ok="$router.go(-1)">
    <template v-if="error">
      <b-alert show :variant="error.level">
        {{error.message}}
      </b-alert>
    </template>
    <template v-else-if="data">
      <h5 class="my-4">剩余时间：{{getTimeStr(data.waitTime)}}</h5>
      <p v-if="data.waitTime > 3000">
        估计是进入永久排队模式了。
        洗洗睡吧。我也不知道怎么回事。
      </p>
      <small>下一次排队</small>
      <b-progress
        height="1rem"
        :value="loading ? 1 : timeElapsed"
        :max="loading ? 1 : interval"
        :animated="loading" />
    </template>
  </b-modal>
</template>

<script>
import moment from 'moment'
import axios from '@/utils/axios'
export default {
  data () {
    return {
      loading: false,
      interval: null,
      timeElapsed: null,
      timer: null,
      task: null,
      data: null,
      error: null
    }
  },
  methods: {
    trigger (state = true) {
      if (state) this.$refs.submissionQueueModal.show()
      else this.$refs.submissionQueueModal.hide()

      if (state) this.queue()
    },
    queue () {
      this.loading = true
      console.log('queue')
      return axios.put('/cr/ticket/order/')
      .then(response => {
        this.loading = false
        this.data = response.data
        let time = this.data.waitTime
        if (time === -1) return this.completeOrdering()
        if (time === -2) throw this.data
        if (time > 60) time = 60
        this.interval = time
        this.timeElapsed = 0
        if (!this.timer) {
          this.timer = setInterval(() => {
            this.timeElapsed += 1
          }, 1000)
        }
        this.task = setTimeout(this.queue, time * 1000)
      })
      .catch(error => {
        this.stop()
        if (error.msg) {
          this.error = {
            message: error.msg,
            level: 'warning'
          }
        }
      })
    },
    completeOrdering (orderID) {
      console.log(orderID)
      this.stop()
      this.$store.commit('addMessage', {
        content: '订单信息已提交，请半小时内登陆12306网站查询并支付。（App内支付正在开发中）',
        type: 'success'
      })
      this.$router.push({name: 'Trip'})
    },
    getTimeStr (time) {
      return moment.duration(time, 'seconds').humanize()
    },
    stop () {
      if (this.task) clearTimeout(this.task)
      if (this.timer) clearInterval(this.timer)
    }
  },
  destroyed () {
    this.stop()
  }
}
</script>
