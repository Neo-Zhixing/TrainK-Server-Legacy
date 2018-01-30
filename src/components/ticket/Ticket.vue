<template>
  <div class="d-flex flex-row text-center justify-content-around align-items-center">
    <div>
      <b-badge v-if="ticket.departureStation === ticket.originStation" variant="primary">始</b-badge>
      <b-badge v-else>过</b-badge>
      {{ stationmap[ticket.departureStation] }}
      <h2>{{ ticket.status === 0 ? ticket.departureTime : '----' }}</h2>
    </div>
    <div style="width: 10rem;">
      <template v-if="ticket.status === 0">
        {{ticket.duration}}
      </template>
      <div v-else class="text-danger">列车停运</div>
      <div class="separate-line"><span class="separate-line-word">{{ ticket.trainName }}</span></div>

      <font-awesome-icon v-if="arrivalDay !== 0" icon="bed" v-b-tooltip.hover :title="['当', '次', '两', '三'][arrivalDay] + '日到达'" />
      <font-awesome-icon v-if="ticket.IDCardSupported" v-b-tooltip.hover title="支持刷身份证进站" icon="id-card" />
      <font-awesome-icon v-if="ticket.reward" v-b-tooltip.hover title="可用积分兑换" icon="tag" />
      <br />
    </div>
    <div>
      <b-badge v-if="ticket.arrivalStation === ticket.destinationStation" variant="primary">终</b-badge>
      <b-badge v-else>过</b-badge>
      {{ stationmap[ticket.arrivalStation] }}
      <h2>{{ ticket.status === 0 ? ticket.arrivalTime : '----' }}</h2>
    </div>
    <div v-if="showSeats">
      <ul class="list-unstyled">
        <li v-for="info in ticketInfo">
          {{info.key}}<b-badge :variant="info.badge">{{info.value}}</b-badge>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import TrainTypeMap from '@/utils/TrainTypeMap'
import fontawesome from '@fortawesome/fontawesome'
import { faIdCard, faTag, faBed } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faIdCard, faTag, faBed)
export default {
  name: 'ticket',
  props: {
    ticket: Object,
    stationmap: Object,
    showSeats: Boolean
  },
  computed: {
    arrivalDay () {
      var hour = Number(this.ticket.departureTime.substring(0, 2)) + Number(this.ticket.duration.substring(0, 2))
      var minute = Number(this.ticket.departureTime.substring(3, 5)) + Number(this.ticket.duration.substring(3, 5))
      if (minute >= 60) hour += 1

      var matchStr
      if (hour >= 24 && hour < 48) matchStr = 1
      else if (hour >= 48 && hour < 72) matchStr = 2
      else if (hour >= 72) matchStr = 3
      else matchStr = 0
      return matchStr
    },
    ticketInfo () {
      var values = []
      for (let index in this.ticket.seats) {
        let value = this.ticket.seats[index]
        if (value === undefined) continue
        var info = {}
        info.key = TrainTypeMap.seatTypeMap[index]

        info.value = value ? (value === true ? '有' : value) : '无'
        info.badge = value ? (value === true ? 'success' : 'primary') : 'danger'
        values.push(info)
      }
      return values
    }
  }
}
</script>

<style scoped>
.separate-line {
  width: 100%; 
  text-align: center; 
  border-bottom: 1px solid #000; 
  line-height: 0.1em;
  margin: 1rem 0 1rem; 
}
.separate-line-word {
  background:#fff; 
  padding:0 10px;
  font-size: 1.5em;
}
</style>