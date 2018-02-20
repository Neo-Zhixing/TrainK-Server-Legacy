<template>
  <b-modal lazy
    ref="modal"
    title="车票详情"
    :size="state ? 'lg' : 'md'"
    :ok-title="ticket ? ['购票', '已售空', '锁定中'][ticket.purchasability] : ''"
    :ok-disabled="ticket ? ticket.purchasability !== 0 : true"
    @ok.prevent="showOrderView"
    @show="state=true"
  >
    <b-card class="my-2" body-class="row" v-if="!user">
      <b-col md="6">
        您还没有登录！
      </b-col>
      <b-col md="6">
        <login-panel  @login="showOrderView" />
      </b-col>
    </b-card>
    <template v-else-if="state">
      <b-card class="mb-3">
        <ticket
          :ticket="ticket"
          :stationmap="stationMap"
        />
      </b-card>
    </template>
    <cr-login-panel v-else-if="!crAuthenticated" @login="showOrderView"/>

  </b-modal>
</template>


<script>
import { states } from '@/store/auth'
import TrainTypeMap from '@/utils/TrainTypeMap'
import Ticket from '@/components/ticket/Ticket'
import CrLoginPanel from '@/components/user/CRLogin'
import LoginPanel from '@/components/user/Login'
import axios from '@/utils/axios'
export default {
  props: ['stationMap'],
  data () {
    return {
      ticket: null,
      state: true // False: Order Preconfirming; True: Detail Displaying
    }
  },
  computed: {
    seats () {
      if (!this.ticket) return null
      let values = []
      for (let index in this.ticket.seats) {
        values.push({
          index: index,
          key: TrainTypeMap.seatTypeMap[index],
          value: this.ticket.seats[index]
        })
      }
      return values
    },
    ...states
  },
  methods: {
    show (ticket) {
      this.ticket = ticket
      this.$refs.modal.show()
    },
    showOrderView () {
      axios.post('/cr/ticket/', this.ticket)
      .then(response => {
        this.$store.commit('auth/crLogin')
        this.$router.push({name: 'Ticket-Order'})
      })
      .catch(error => {
        if (error.response) {
          if (error.response.status === 403) {
            this.state = false
            this.$store.commit('auth/crLogout')
          } else if (error.response.status === 410) {
            this.$store.commit('auth/crLogin')
            this.$store.commit('addMessage', {
              content: '订单信息过期，请重新提交！',
              type: 'info',
              time: 10
            })
            this.$emit('reload')
            this.$refs.modal.hide()
          } else if (error.response.status === 400) {
            this.$store.commit('addMessage', {
              content: '您还有订单未完成！',
              type: 'warning',
              time: 10
            })
            this.$router.push({name: 'Trip'})
          }
        }
      })
    }
  },
  components: { Ticket, CrLoginPanel, LoginPanel }
}
</script>
