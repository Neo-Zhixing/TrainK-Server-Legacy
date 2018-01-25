<template>
  <b-container>
    <route-input-panel id="ticket-input" horizontal
    :from="$route.query.from"
    :to="$route.query.to"
    :date="$route.query.date"
    @submit="submit"/>
    <b-row>
      <b-col lg="4">
        <b-nav pills fill class="text-center">
          <b-nav-item disabled :active="filters.order===0" id="0" @click="rankingTypePills">综合</b-nav-item>
          <b-nav-item :active="filters.order===1" id="1" @click="rankingTypePills">
            出发时间
            <font-awesome-icon v-if="filters.order===1" :icon="filters.reversed ? 'sort-down' : 'sort-up'"/>
          </b-nav-item>
          <b-nav-item :active="filters.order===2" id="2" @click="rankingTypePills">
            时长
            <font-awesome-icon v-if="filters.order===2" :icon="filters.reversed ? 'sort-down' : 'sort-up'"/>
          </b-nav-item>
          <b-nav-item :active="filters.order===3" id="3" @click="rankingTypePills">
            到达时间
            <font-awesome-icon v-if="filters.order===3" :icon="filters.reversed ? 'sort-down' : 'sort-up'"/>
          </b-nav-item>
        </b-nav>
      </b-col>
      <b-col lg="8">
        <multiselect multiple
          v-model="filters.options"
          :options="availableOptions"

          group-values="value"
          group-label="label"

          :loading="tickets === null"
          placeholder="过滤器..."

          track-by="value"
          label="label"
          >
          <template slot="noResult">没有相应的过滤器</template>
        </multiselect>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="9">
        <spinner
          v-if="tickets === null"
          size="huge"
          message="加载中"
          class="mt-5"
        />
        <div v-else-if="currentTickets === null ? false : currentTickets.length === 0">没有找到</div>
        <template v-else>
          <ticket
            v-for="ticket in currentTickets"
            :key="ticket.trainTelecode"
            :ticket = "ticket"
            :stationmap = "stationMap"
            :querydate = "$route.query.date"
          />
        </template>
      </b-col>
      <b-col md="3">
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import TrainTypeMap from '@/utils/TrainTypeMap'
import axios from 'axios'
import Ticket from '@/components/ticket/Ticket'
import RouteInputPanel from '@/components/ticket/RouteInputPanel'
import Spinner from 'vue-simple-spinner'
import Multiselect from 'vue-multiselect'

import fontawesome from '@fortawesome/fontawesome'
import { faSortUp, faSortDown } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faSortUp, faSortDown)

export default {
  name: 'TicketList',
  data () {
    return {
      filters: {
        keys: ['departureStation', 'arrivalStation', 'trainType', 'seatType'],
        excludeMap: { // 互排表
          ANYH: TrainTypeMap.highSpeedTrainTypes.add('ANYO'),
          ANYO: TrainTypeMap.ordinaryTrainTypes.add('ANYH'),
          ANY: new Set(Object.keys(TrainTypeMap.seatTypeMap)),
          ANYS: TrainTypeMap.sleeperTypes
        },
        options: [],
        order: 2,
        reversed: false
      },
      currentTickets: null,
      tickets: null,
      stationMap: null
    }
  },
  computed: {
    filterOptions () {
      let options = {}
      for (let key of this.filters.keys) options[key] = new Set()
      for (let option of this.filters.options) options[option.key].add(option.value) // 把select控件维护的options给转化为sets
      return options
    },
    filterExcludes () {
      let excludes = new Set()
      for (let key of this.filters.keys.slice(2, 4)) for (let option of this.filterOptions[key]) if (this.filters.excludeMap[option] !== undefined) excludes = new Set([...excludes, ...this.filters.excludeMap[option]])
      return excludes
    },
    availableOptions () { // 过滤器下拉框中可用的过滤器
      // 排除tickets或者stationMap为null的情况
      if (this.tickets === null) return []
      if (this.stationMap === null) return []
      let options = {}
      for (let key of this.filters.keys) options[key] = new Set()
      let excludes = this.filterExcludes

      // 遍历所有票，在options中添加相应的过滤器
      for (let ticket of this.tickets) {
        options.departureStation.add(ticket.departureStation)
        options.arrivalStation.add(ticket.arrivalStation)
        let trainType = TrainTypeMap.typeForTrain(ticket.trainName)
        if (!excludes.has(trainType)) options.trainType.add(trainType)
        if (TrainTypeMap.highSpeedTrainTypes.has(trainType) && !excludes.has('ANYH')) options.trainType.add('ANYH')
        else if (TrainTypeMap.ordinaryTrainTypes.has(trainType) && !excludes.has('ANYO')) options.trainType.add('ANYO')
        // 遍历该票所有的座位, 添加相应过滤器
        for (let seatType in ticket.seats) {
          if (!excludes.has(seatType)) options.seatType.add(seatType)
          if (TrainTypeMap.sleeperTypes.has(seatType) && !excludes.has('ANYS')) options.seatType.add('ANYS')
        }
      }
      options.seatType.add('ANY')
      options.departureStation.add('TERMINAL')
      options.arrivalStation.add('TERMINAL')

      // 把options set转化为array
      var results = []
      for (let index in this.filters.keys) {
        let key = this.filters.keys[index]
        let result = {
          label: ['出发车站', '目的车站', '列车类型', '坐席有票'][index],
          value: []
        }
        for (var option of options[key]) {
          var value
          if (key === 'departureStation' || key === 'arrivalStation') value = option === 'TERMINAL' ? {'departureStation': '始发站', 'arrivalStation': '目的站'}[key] : this.stationMap[option] // 如果是终端站，则返回“始发站”或者“目的站”， 否则返回中文站名
          else if (key === 'trainType') value = TrainTypeMap.trainTypeMap[option]
          else if (key === 'seatType') value = TrainTypeMap.seatTypeMap[option]
          result.value.push({
            label: value,
            key: key,
            value: option
          })
        }
        results.push(result)
      }

      // 排序results array
      for (let index in results) {
        results[index].value.sort((a, b) => {
          if (a.value.slice(0, 3) === 'ANY') return false
          if (b.value.slice(0, 3) === 'ANY') return true
          return true
        })
      }

      return results
    }
  },
  watch: {
    'filters.options' (newOptions) {
      let excludes = this.filterExcludes
      for (let index in newOptions) {
        if (excludes.has(newOptions[index].value)) {
          newOptions.splice(index, 1)
        }
      }
      this.rank()
    }
  },
  methods: {
    rankingTypePills (sender) {
      var element = sender.toElement
      var newOrder = 0
      for (var i = 0; i < 5; i++) {
        if (element.id !== '') {
          newOrder = element.id
          break
        }
        element = element.parentElement
      }
      newOrder = Number(newOrder)
      if (newOrder === this.filters.order) this.filters.reversed = !this.filters.reversed
      else this.filters.order = newOrder
      this.rank()
    },
    rank () {
      if (this.tickets === null) return
      let tickets = Object.assign([], this.tickets)
      let options = this.filterOptions
      tickets = tickets.filter((x) => {
        let keyMap = {}
        keyMap[this.filters.keys[0]] = 'originStation'
        keyMap[this.filters.keys[1]] = 'destinationStation'
        for (let key of this.filters.keys.slice(0, 2)) {
          if (options[key].has('TERMINAL') && x[key] !== x[keyMap[key]]) return false // 终端站
          if (!(
            options[key].has(x[key]) || // 符合Filter条件
             options[key].size === 0 || // 没有Filters
            (options[key].size === 1 && options[key].has('TERMINAL')) // 只有一个终端站filter
            )) return false
        }

        // 检查列车种类
        let trainType = TrainTypeMap.typeForTrain(x.trainName)
        var includes = options.trainType
        if (includes.has('ANYO')) includes = new Set([...TrainTypeMap.ordinaryTrainTypes, ...includes])
        else if (includes.has('ANYH')) includes = new Set([...TrainTypeMap.highSpeedTrainTypes, ...includes])
        if (!(includes.has(trainType) || options.trainType.size === 0)) return false

        // 检查座位种类
        includes = options.seatType
        if (includes.size === 0) return true // 因为这是最后一个test了，所以可以直接返回true
        if (includes.has('ANY')) includes = new Set([...Object.keys(TrainTypeMap.seatTypeMap), ...includes])
        else if (includes.has('ANYS')) includes = new Set([...TrainTypeMap.sleeperTypes, ...includes])
        for (let type of includes) if (x.seats[type] !== undefined && x.seats[type] !== false) return true
        return false
      })
      tickets.sort((a, b) => {
        if (a.status !== 0) return true  // 停运的车永远排在最下面
        let keyMap = ['', 'departureTime', 'duration', 'arrivalTime']
        let aTime = a[keyMap[this.filters.order]]
        let bTime = b[keyMap[this.filters.order]]
        var result
        if (aTime.slice(0, 2) === bTime.slice(0, 2)) result = Number(aTime.slice(3, 5)) > Number(bTime.slice(3, 5))
        else result = Number(aTime.slice(0, 2)) > Number(bTime.slice(0, 2))
        if (this.filters.reversed) result = !result
        return result
      })
      this.currentTickets = tickets
    },
    ticketList () {
      axios.get('https://cr.api.tra.ink/otn/leftTicket/queryZ', {
        params: {
          'leftTicketDTO.train_date': this.$route.query.date,
          'leftTicketDTO.from_station': this.$route.query.from,
          'leftTicketDTO.to_station': this.$route.query.to,
          'purpose_codes': 'ADULT'
        }
      })
      .then((response) => {
        let data = response.data.data
        this.stationMap = data.map

        let tickets = []
        let ticketType = function (value) {
          if (value === '有') return true
          if (value === '无') return false
          if (value === '') return undefined
          return Number(value)
        }
        let keyMap = [
          { name: 'secret', type: String },
          { name: 'buttonText', type: String },
          { name: 'trainTelecode', type: String },
          { name: 'trainName', type: String },
          { name: 'originStation', type: String },
          { name: 'destinationStation', type: String },
          { name: 'departureStation', type: String },
          { name: 'arrivalStation', type: String },
          { name: 'departureTime', type: String },
          { name: 'arrivalTime', type: String },
          { name: 'duration', type: String },
          { name: 'purchasability', type: String },
          { name: 'yp_info', type: String },
          { name: 'departureDate', type: String },
          { name: 'train_seat_feature', type: String },
          { name: 'locationCode', type: String },
          { name: 'departureIndex', type: Number },
          { name: 'arrivalIndex', type: Number },
          { name: 'IDCardSupported', type: Boolean },
          { name: 'status', type: Number },
          { name: 'gg_num', type: ticketType, subpath: 'seats' },
          { name: 'A6', type: ticketType, subpath: 'seats' },
          { name: 'MIN', type: ticketType, subpath: 'seats' },
          { name: 'A4', type: ticketType, subpath: 'seats' },
          { name: 'A2', type: ticketType, subpath: 'seats' },
          { name: 'P', type: ticketType, subpath: 'seats' },
          { name: 'WZ', type: ticketType, subpath: 'seats' },
          { name: 'yb_num', type: ticketType, subpath: 'seats' },
          { name: 'A3', type: ticketType, subpath: 'seats' },
          { name: 'A1', type: ticketType, subpath: 'seats' },
          { name: 'O', type: ticketType, subpath: 'seats' },
          { name: 'M', type: ticketType, subpath: 'seats' },
          { name: 'A9', type: ticketType, subpath: 'seats' },
          { name: 'F', type: ticketType, subpath: 'seats' },
          { name: 'yp_ex', type: String },
          { name: 'seat_types', type: String },
          { name: 'reward', type: Boolean }
        ]

        for (let ticketStr of data.result) {
          let ticketParams = ticketStr.split('|')
          let ticket = {}
          for (let paramIndex in ticketParams) {
            let keyObj = keyMap[paramIndex]
            let value = keyObj.type(ticketParams[paramIndex])
            if (keyObj.subpath === undefined) ticket[keyObj.name] = value
            else {
              if (ticket[keyObj.subpath] === undefined) ticket[keyObj.subpath] = {}
              ticket[keyObj.subpath][keyObj.name] = value
            }
          }
          tickets.push(ticket)
        }
        console.log(tickets)
        this.tickets = tickets
        this.filters.options = [{
          label: '有票 - 任意',
          key: 'seatType',
          value: 'ANY'
        }]
        this.rank()
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submit (event) {
      this.tickets = null
      this.stationmap = null
      this.$router.replace({
        path: 'list',
        query: {
          from: event.departureStation,
          to: event.arrivalStation,
          date: event.date
        }
      })
      this.ticketList()
    }
  },
  mounted () {
    this.filters.excludeMap.ANY.delete('ANY')
    this.ticketList()
  },
  components: {
    Ticket,
    RouteInputPanel,
    Spinner,
    Multiselect
  }
}
</script>

<style scoped>
  #ticket-input {
    background-color: #f5f5f5;
    border-radius: 10px;
    padding-top: 1rem;
    padding-bottom: 1rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }
</style>
