<template>
  <b-container class="py-5">
    <b-row>
      <b-col md="8" class="text-center">
        <b-list-group>
          <b-list-group-item v-for="trip in trips" key="trip.id">
            <b-row class="py-2">
              <b-col sm="4">
                <h3>{{trip.record.train.stops[trip.departureIndex].station.name}}</h3>
                <h1>{{time(trip.record.train.stops[trip.departureIndex].departureTime)}}</h1>
              </b-col>
              <b-col sm="4">
                <p>{{trip.record.departureDate}}</p>
                <h3 class="separate-line">{{trip.record.train.names.join('/')}}</h3>
              </b-col>
              <b-col sm="4">
                <h3>{{trip.record.train.stops[trip.arrivalIndex].station.name}}</h3>
                <h1>{{time(trip.record.train.stops[trip.arrivalIndex].arrivalTime)}}</h1>
              </b-col>
            </b-row>
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col md="4">
        <b-card title="添加行程"
          img-src="https://lorempixel.com/600/300/food/5/"
          img-alt="Image"
          img-top>
          <b-form>
            <b-form-group label="车次">
              <b-form-input v-model='train'/>
            </b-form-group>
            <b-form-group label="日期">
              <flat-pickr
                class="form-control"
                placeholder="选择日期"
                v-model="date"
                v-validate="'required'"
              />
            </b-form-group>
            <b-button block variant="primary" @click="openAddModal">添加</b-button>
            <trip-add-view ref="tripAddView" @add="addTrip" />
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import axios from '@/utils/axios'
import TripAddView from './Add.vue'
import flatPickr from 'vue-flatpickr-component'
import moment from 'moment'
export default {
  data () {
    return {
      trips: null,
      train: '',
      date: ''
    }
  },
  mounted () {
    this.update()
  },
  methods: {
    update () {
      axios.get('/trip/')
      .then((response) => {
        this.trips = response.data.results
      })
    },
    time (ISOStr) {
      let time = moment.duration(ISOStr)
      return moment.utc(time.asMilliseconds()).format('HH:mm')
    },
    openAddModal () {
      this.$refs.tripAddView.trainName = this.train
      this.$refs.tripAddView.date = this.date
      this.$refs.tripAddView.toggle(true)
    },
    addTrip (trip) {
      this.trips.push(trip)
    }
  },
  components: {
    TripAddView, flatPickr
  }
}
</script>
<style>
.separate-line{
  padding: 0 20px 0;
  margin: 20px 0;
  line-height: 1px;
  border-left: 50px solid #ddd;
  border-right: 50px solid #ddd;
  text-align: center;
}
</style>