<template>
  <b-container>
    <b-row class="my-3">
      <b-col>
        <b-card body-class="d-flex flex-column flex-md-row">
          <b-button-group class="m-1 btn-block">
            <b-button class="col" :variant="filters.order===0 ? 'primary' : 'outline-primary'" @click="rankingTypePills(0)" disabled>综合</b-button>
            <b-button class="col" :variant="filters.order===1 ? 'primary' : 'outline-primary'" @click="rankingTypePills(1)">
              出发时间
              <font-awesome-icon v-if="filters.order===1" :icon="filters.reversed ? 'sort-down' : 'sort-up'"/>
            </b-button>
            <b-button class="col" :variant="filters.order===2 ? 'primary' : 'outline-primary'" @click="rankingTypePills(2)">
              耗时
              <font-awesome-icon v-if="filters.order===2" :icon="filters.reversed ? 'sort-down' : 'sort-up'"/>
            </b-button>
            <b-button class="col" :variant="filters.order===3 ? 'primary' : 'outline-primary'" @click="rankingTypePills(3)">
              到达时间
              <font-awesome-icon v-if="filters.order===3" :icon="filters.reversed ? 'sort-down' : 'sort-up'"/>
            </b-button>
          </b-button-group>
          <multiselect multiple
            v-model="filters.options"
            :options="availableOptions"

            group-values="value"
            group-label="label"

            :loading="tickets === null"
            placeholder="过滤器..."

            track-by="value"
            label="label"
            class="m-1"
          >
            <template slot="noResult">没有相应的过滤器</template>
          </multiselect>
        </b-card>
      </b-col>
    </b-row>
    <b-row class="my-3">
      <b-col lg="8" class="order-1 order-lg-0">
        <spinner
          v-if="tickets === null"
          size="huge"
          message="加载中"
          class="mt-5"
        />
        <div v-else-if="currentTickets === null ? false : currentTickets.length === 0">没有找到</div>
        <template  v-else>
          <b-list-group>
            <b-list-group-item button
              v-for="ticket in currentTickets"
              :key="ticket.trainTelecode"
              @click="$refs.detailModal.show(ticket)">
              <ticket show-seats
                :ticket = "ticket"
                :stationmap = "stationMap"
              />
            </b-list-group-item>
          </b-list-group>
          <detail-view ref="detailModal" :station-map="stationMap" @reload="tickets=null; ticketList();" />
        </template>
      </b-col>
      <b-col lg="4" class="order-0 order-lg-1 d-flex flex-column flex-md-row flex-lg-column">
        <route-input id="ticket-input"
          :from="$route.query.from"
          :to="$route.query.to"
          :date="$route.query.date"
          @submit="submit"
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import TrainTypeMap from '@/utils/TrainTypeMap'
import axios from 'axios'
import moment from 'moment'
import Ticket from '@/components/ticket/Ticket'
import RouteInput from '@/components/ticket/RouteInputPanel'
import DetailView from './Detail'
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
    rankingTypePills (newOrder) {
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
      let key = ['', 'departureTime', 'duration', 'arrivalTime'][this.filters.order]
      tickets.sort((a, b) => {
        if (a.status !== 0) return true  // 停运的车永远排在最下面
        let aTime = moment.duration(a[key])
        let bTime = moment.duration(b[key])
        let result = aTime.asMinutes() - bTime.asMinutes()
        if (this.filters.reversed) result = -result // 坑：WebKit浏览器无法接受返回Boolean。必须返回Interger。
        return result
      })
      console.log(tickets)
      this.currentTickets = tickets
    },
    ticketList () {
      axios.get('/cr/ticket/', {
        params: {
          'date': this.$route.query.date,
          'from': this.$route.query.from,
          'to': this.$route.query.to
        }
      })
      .then((response) => {
        let data = response.data
        this.stationMap = data.nameMap
        this.tickets = data.results
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
    DetailView,
    RouteInput,
    Spinner,
    Multiselect
  }
}
</script>
