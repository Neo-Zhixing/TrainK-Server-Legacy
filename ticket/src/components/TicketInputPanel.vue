<template>
<b-card class="text-left" style="opacity: .95;">
  <b-nav fill tabs class="card-header-tabs" slot="header">
    <b-nav-item :active="form.tripType==1" id="1" @click="tripTypeTab">单程</b-nav-item>
    <b-nav-item disabled :active="form.tripType==2" id="2" @click="tripTypeTab">往返</b-nav-item>
  </b-nav>
  <b-form @submit="submit">
    <b-form-group label="行程" label-for="route">
      <b-input-group id="route">
        <b-form-input v-model="form.departureStation" class="text-right" placeholder="出发站"/>
          <b-input-group-button>
            <b-button @click="swapStations" variant="secondary"><font-awesome-icon icon="arrows-alt-h"/></b-button>
          </b-input-group-button>
        <b-form-input v-model="form.arrivalStation" class="text-left" placeholder="目的站"/>
      </b-input-group>
    </b-form-group>
    <b-form-group label="日期" label-for="date">
      <b-input-group id="date">
        <flat-pickr
        class="form-control"
        placeholder="选择日期"
        v-model="form.date"
        :config="datepickerConfig"/>
        <b-input-group-addon><font-awesome-icon icon="calendar-alt"/></b-input-group-addon>
      </b-input-group>
    </b-form-group>
    <b-button block variant="primary" size="lg" type="submit">搜索</b-button>
  </b-form>
</b-card>
</div>
</template>

<script>
  import flatPickr from 'vue-flatpickr-component'
  import 'flatpickr/dist/themes/airbnb.css'
  import {Mandarin} from 'flatpickr/dist/l10n/zh'

  import fontawesome from '@fortawesome/fontawesome'
  import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
  import { faArrowsAltH, faCalendarAlt } from '@fortawesome/fontawesome-free-solid'
  fontawesome.library.add(faArrowsAltH, faCalendarAlt)

  import { EventBus } from '../bus.js'
  
  export default {
    name: 'ticket',
    props: [],
    data () {
      return {
        form: {
          tripType: 1,
          departureStation: '',
          arrivalStation: '',
          date: null,
        },
      }
    },
    computed: {
      datepickerConfig () {
        return {
          locale: Mandarin,
          mode: this.form.tripType==1?'single':'range',
          minDate: new Date()
        }
      }
    },
    methods: {
      swapStations () {
        var temp = this.form.arrivalStation
        this.form.arrivalStation = this.form.departureStation
        this.form.departureStation = temp
      },
      tripTypeTab (sender) {
        this.form.tripType = Number(sender.toElement.parentElement.id)
      },
      submit (event) {
        event.preventDefault()
        this.$router.replace({
          path: 'list',
          query: {
            from: this.form.departureStation,
            to: this.form.arrivalStation,
            date: this.form.date
          }
        })
      },
    },
    components: {
      FontAwesomeIcon, flatPickr
    }
  }
</script>

<style scoped>
</style>