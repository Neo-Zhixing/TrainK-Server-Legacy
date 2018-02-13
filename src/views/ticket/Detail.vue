<template>
  <b-modal lazy
    ref="modal"
    title="车票详情"
    size="lg"
    :ok-title="ticket ? ['购票', '已售空', '锁定中'][ticket.purchasability] : ''"
    :ok-disabled="ticket ? ticket.purchasability !== 0 : true"
    @ok.prevent="showOrderView"
  >
    <template v-if="state">
      <b-card class="mb-3">
        <ticket
          :ticket="ticket"
          :stationmap="stationMap"
        />
      </b-card>
    </template>
    <b-card class="my-2" body-class="row" v-else-if="!user">
      <b-col md="6">
        您还没有登录！
      </b-col>
      <b-col md="6">
        <login-panel  @login="showOrderView" />
      </b-col>
    </b-card>
    <cr-login-panel horizontal v-else-if="!crAuthenticated" @login="showOrderView"/>

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
      this.state = false
      axios.post('/cr/ticket/', this.ticket)
      .then(response => {
        this.$store.commit('auth/crLogin')
        this.$router.push({name: 'PlaceOrders'})
      })
      .catch(error => {
        if (error.response) {
          if (error.response.status === 403) this.$store.commit('auth/crLogout')
          else if (error.response.status === 410) {
            this.$store.commit('auth/crLogin')
            this.$emit('reload')
            this.$refs.modal.hide()
          }
        }
      })
    }
  },
  components: { Ticket, CrLoginPanel, LoginPanel }
}
</script>