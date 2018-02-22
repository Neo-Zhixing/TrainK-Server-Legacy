<template>
  <div v-if="context === null">
    加载中
  </div>
  <div v-else-if="seatSelectable">
    <div class="d-flex flex-row flex-nowrap justify-content-between"
      v-for="row in passengers.length > 1 ? [1, 2] : [1]">
      <template v-for="seat in seats">
        <p v-if="seat === null">走廊</p>
        <b-button v-else
          @click="btnClicked(row, seat)"
          :variant="seatSelected(row, seat) ? 'primary' : 'secondary'">
          <font-awesome-icon :icon="iconSecondClass" />
        </b-button>
      </template>
    </div>
  </div>
  <div v-else-if="seatSelectable === null">
    选择乘客，试试看你能不能选座吧！
  </div>
  <div v-else>
    对不起，您当前的购票配置不支持选择座位。
  </div>
</template>

<script>
import SeatIcons from '@/assets/Logo'
export default {
  props: ['value', 'passengers', 'context'],
  data () {
    return {
      selectedSeats: []
    }
  },
  watch: {
    context () { this.selectedSeats = [] },
    passengers () { this.selectedSeats = [] }
  },
  computed: {
    iconSecondClass () { return SeatIcons.SecondClass },
    iconFirstClass () { return SeatIcons.FirstClass },
    seatSelectable () {
      // Return null when no passengers were selected
      if (!this.context || !this.passengers || this.passengers.length === 0) return null
      if (this.context.data.canChooseSeats !== 'Y') return false
      if (!this.context.data.choose_Seats) return false
      let presumedSeat = this.passengers[0].selectedSeat
      if (!this.context.data.choose_Seats.includes(presumedSeat)) return false
      // Check if all selected passengers have the same type of seat
      for (let passenger of this.passengers) {
        if (passenger.selectedSeat !== presumedSeat) return false
      }
      return true
    },
    seats () {
      let seat = this.passengers[0].selectedSeat
      let seats = null
      if (seat === 'O') seats = ['A', 'B', 'C', null, 'D', 'F']
      else if (seat === 'M') seats = ['A', 'C', null, 'D', 'F']
      else if (seat === '9' || seat === 'P') seats = ['A', 'C', null, 'F']
      console.log(seats)
      return seats
    }
  },
  methods: {
    seatSelected (row, seat) {
      let a = this.selectedSeats.includes(row.toString() + seat)
      return a
    },
    btnClicked (row, seat) {
      let seatID = row.toString() + seat
      console.log(seatID)
      if (this.seatSelected(row, seat)) {
        this.selectedSeats.splice(this.selectedSeats.indexOf(seatID), 1)
      } else {
        if (this.passengers.length <= this.selectedSeats.length) {
          this.selectedSeats.pop()
        }
        this.selectedSeats.push(seatID)
      }
    }
  }
}
</script>
