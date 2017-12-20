<template>

<b-row v-if="horizontal" id="ticket-input-body">
  <b-col lg="2" class="my-1">
    <b-nav pills fill class="text-center">
      <b-nav-item :active="form.tripType==1" id="1" @click="tripTypeTab">单程</b-nav-item>
      <b-nav-item disabled :active="form.tripType==2" id="2" @click="tripTypeTab">往返</b-nav-item>
    </b-nav>
  </b-col>
  <b-col lg="5" class="my-1">
    <b-input-group id="route">
        <b-form-input v-model="form.departureStation" class="text-right" placeholder="出发站"/>
          <b-input-group-button>
            <b-button @click="swapStations" variant="secondary"><font-awesome-icon icon="arrows-alt-h"/></b-button>
          </b-input-group-button>
        <b-form-input v-model="form.arrivalStation" class="text-left" placeholder="目的站"/>
      </b-input-group>
  </b-col>
  <b-col lg="3" class="my-1">
    <b-input-group id="date">
        <flat-pickr
        class="form-control"
        placeholder="选择日期"
        v-model="form.date"
        :config="datepickerConfig"/>
        <b-input-group-addon><font-awesome-icon icon="calendar-alt"/></b-input-group-addon>
      </b-input-group>
  </b-col>
  <b-col lg="2" class="my-1">
    <b-button block variant="primary" @click="submit">搜索</b-button>
  </b-col>
</b-row>
<b-card v-else class="text-left" style="opacity: .95;">
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
</template>

<script>
  import flatPickr from 'vue-flatpickr-component'
  import 'flatpickr/dist/themes/airbnb.css'
  import {Mandarin} from 'flatpickr/dist/l10n/zh'

  import fontawesome from '@fortawesome/fontawesome'
  import FontAwesomeIcon from '@fortawesome/vue-fontawesome'
  import { faArrowsAltH, faCalendarAlt } from '@fortawesome/fontawesome-free-solid'
  fontawesome.library.add(faArrowsAltH, faCalendarAlt)
  
  export default {
    name: 'TicketInputPanel',
    props: {
      'horizontal': Boolean,
      'from': String,
      'to': String,
      'date': String
    },
    data () {
      return {
        form: {
          tripType: 1,
          departureStation: this.from,
          arrivalStation: this.to,
          date: this.date
        }
      }
    },
    computed: {
      datepickerConfig () {
        return {
          locale: Mandarin,
          mode: this.form.tripType === 1 ? 'single' : 'range',
          minDate: 'today'
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
        this.$emit('submit', this.form)
      }
    },
    components: {
      FontAwesomeIcon, flatPickr
    }
  }
</script>

<style scoped>
#ticket-input-body {
  background-color: #f5f5f5;
  border-radius: 10px;
  padding-top: 1rem;
  padding-bottom: 1rem;
  margin-top: 1rem;
  margin-bottom: 1rem;
}

.ticket-input-component {
  margin-top: 1rem;
  margin-bottom: 1rem;
}
</style>