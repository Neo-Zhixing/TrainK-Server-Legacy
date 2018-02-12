<template>
  <b-modal lazy
    ref="modal"
    title="车票详情"
    size="lg"
    :ok-title="ticket ? ['购票', '已售空', '锁定中'][ticket.purchasability] : ''"
    :ok-disabled="ticket ? ticket.purchasability !== 0 : true"
    @ok.prevent="showOrderView"
    @show="load"
  >
    <b-card class="my-2" body-class="row" v-if="authenticated === false">
      <b-col md="6">
        您还没有登录！
      </b-col>
      <b-col md="6">
        <login-panel  @login="showOrderView" />
      </b-col>
    </b-card>
    <cr-login-panel horizontal v-else-if="crauthenticated === false" @login="showOrderView"/>
    <template v-else>
      <b-card class="mb-3">
        <ticket
          :ticket="ticket"
          :stationmap="stationMap"
        />
      </b-card>
    </template>
  </b-modal>
</template>


<script>
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
      authenticated: null,
      crauthenticated: null
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
    }
  },
  methods: {
    show (ticket) {
      this.ticket = ticket
      this.$refs.modal.show()
    },
    load () {
      this.authenticated = null
      this.crauthenticated = null
    },
    showOrderView () {
      axios.post('/cr/ticket/', this.ticket)
      .then(response => {
        console.log(response.data)
        this.data = response.data
        this.authenticated = true
        this.crauthenticated = true
        this.$router.push({name: 'PlaceOrders'})
      })
      .catch(error => {
        if (error.response) {
          if (error.response.status === 403) this.authenticated = false
          else if (error.response.status === 401) {
            this.authenticated = true
            this.crauthenticated = false
          } else if (error.response.status === 410) {
            this.authenticated = true
            this.crauthenticated = true
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