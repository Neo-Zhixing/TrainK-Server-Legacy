<template>
  <b-row class="ticket">
    <b-col>
      <b-row :class="{ 'ticket-gist-triggered': !collapsed, 'ticket-available': ticket.status === 0 }" class="ticket-gist text-center" @click="expand">
        <b-col>
          <h1>{{ ticket.trainName }}</h1>
        </b-col>
        <b-col>
          <b-badge v-if="ticket.departureStation === ticket.originStation" variant="primary">始</b-badge>
          <b-badge v-else>过</b-badge>
          {{ stationmap[ticket.departureStation] }}
          <h2>{{ ticket.status === 0 ? ticket.departureTime : '----' }}</h2>
        </b-col>
        <b-col>
          <template v-if="ticket.status === 0">
            {{ticket.duration}}
            <font-awesome-icon v-if="ticket.IDCardSupported" v-b-tooltip.hover title="支持刷身份证进站" icon="id-card" />
            <font-awesome-icon v-if="ticket.reward" v-b-tooltip.hover title="可用积分兑换" icon="tag" />
          </template>
          <br/>
          <div class="separate-line"></div>
          <template v-if="ticket.status === 0">{{arrivalDay}}</template>
          <template v-else><div class="text-danger">列车停运</div></template>
        </b-col>
        <b-col>
          <b-badge v-if="ticket.arrivalStation === ticket.destinationStation" variant="primary">终</b-badge>
          <b-badge v-else>过</b-badge>
          {{ stationmap[ticket.arrivalStation] }}
          <h2>{{ ticket.status === 0 ? ticket.arrivalTime : '----' }}</h2>
        </b-col>
      </b-row>
      <b-collapse :id="ticket.trainTelecode + '-details'" :visible="!collapsed">
        <b-row class="py-2">
          <b-col cols="10" class="text-left">
            <ul class="ticket-info">
              <li v-for="info in ticketInfo">
                {{info.key}}<b-badge :variant="info.badge">{{info.value}}</b-badge>
                {{info.price}}
              </li>
            </ul>
          </b-col>
          <b-col cols="2">
            <b-button variant="primary" size="sm">详情</b-button>
          </b-col>
        </b-row>
      </b-collapse>
    </b-col>
  </b-row>
</template>

<script>
  import TicketUtils from '@/utils'
  import axios from 'axios'
  import fontawesome from '@fortawesome/fontawesome'
  import { faIdCard, faTag } from '@fortawesome/fontawesome-free-solid'
  import { EventBus } from '@/bus.js'
  fontawesome.library.add(faIdCard, faTag)
  export default {
    name: 'ticket',
    props: ['ticket', 'stationmap', 'querydate'],
    data () {
      return {
        collapsed: true,
        price: null
      }
    },
    computed: {
      arrivalDay () {
        var hour = Number(this.ticket.departureTime.substring(0, 2)) + Number(this.ticket.duration.substring(0, 2))
        var minute = Number(this.ticket.departureTime.substring(3, 5)) + Number(this.ticket.duration.substring(3, 5))
        if (minute >= 60) hour = hour + 1

        var matchStr
        if (hour >= 24 && hour < 48) matchStr = '次'
        else if (hour >= 48 && hour < 72) matchStr = '两'
        else if (hour >= 72) matchStr = '三'
        else matchStr = '当'
        return matchStr + '日到达'
      },
      ticketInfo () {
        var values = []
        for (let index in this.ticket.seats) {
          let value = this.ticket.seats[index]
          if (value === undefined) continue
          var info = {}
          info.key = TicketUtils.seatTypeMap[index]
          info.price = this.price === null ? null : this.price[index]

          info.value = value ? (value === true ? '有' : value) : '无'
          info.badge = value ? (value === true ? 'success' : 'primary') : 'danger'
          values.push(info)
        }
        return values
      }
    },
    methods: {
      expand () {
        if (this.ticket.status !== 0) return
        // Expand/Collapse the ticket details, and if we're expanding, send an event to all of other ticket components.
        if (this.collapsed) {
          EventBus.$emit('ticket-expand', this)
          if (this.price === null) {
            axios.get('//api.tra.ink/ticket/price', {
              params: {
                'telecode': this.ticket.trainTelecode,
                'from': this.ticket.departureIndex,
                'to': this.ticket.arrivalIndex,
                'seat_types': this.ticket.seat_types,
                'date': this.querydate
              }
            })
            .then((response) => {
              if (response.data !== {}) this.price = response.data
            })
            .catch(function (error) {
              console.log(error)
            })
          }
        }
        this.collapsed = !this.collapsed
      }
    },
    mounted () {
      // Register EventBus. Listen to the events other ticket components sent.
      EventBus.$on('ticket-expand', sender => {
        // Collapse the ticket details unless this is the sender
        if (this !== sender) this.collapsed = true
      })
    }
  }
</script>

<style scoped>
.separate-line {
  background-color: black;
  height: 1px;
  margin: 5px 0;
  width: 100%;
}

.ticket {
  background-color: #f5f5f5;
  border-radius: 10px;
  margin-top: 1rem;
  margin-bottom: 1rem;
}
.ticket-gist {
  user-select: none;
  background-color: #f5f5f5;
  border-radius: 10px;
  padding-top: 1rem;
  padding-bottom: 1rem;
  transition: background-color 0.3s;
}
.ticket-available{
  cursor:pointer;
}

.ticket-available:hover,
.ticket-gist-triggered {
  background-color: #DDDDDD;
}
.ticket-info {
  list-style-type: none;
}
.ticket-info li {
  margin-right: 2rem;
  float: left;
}
</style>