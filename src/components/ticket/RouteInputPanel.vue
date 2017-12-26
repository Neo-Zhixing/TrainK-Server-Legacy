<template>

<b-row v-if="horizontal">
  <b-col lg="2" class="my-1">
    <b-nav pills fill class="text-center">
      <b-nav-item :active="form.tripType==1" id="1" @click="tripTypeTab">单程</b-nav-item>
      <b-nav-item disabled :active="form.tripType==2" id="2" @click="tripTypeTab">往返</b-nav-item>
    </b-nav>
  </b-col>
  <b-col lg="5" class="my-1">
    <route-input v-model="form" />
  </b-col>
  <b-col lg="3" class="my-1">
    <b-input-group id="date">
      <flat-pickr
      required
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
<b-card v-else class="text-center" style="opacity: .95;">
  <b-nav fill tabs class="card-header-tabs" slot="header">
    <b-nav-item :active="form.tripType==1" id="1" @click="tripTypeTab">单程</b-nav-item>
    <b-nav-item disabled :active="form.tripType==2" id="2" @click="tripTypeTab">往返</b-nav-item>
  </b-nav>
  <b-form @submit="submit">
    <b-form-group label="行程" label-for="route">
      <route-input required v-model="form" />
    </b-form-group>
    <b-form-group label="日期" label-for="date">
      <b-input-group id="date">
        <flat-pickr
        required
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
import RouteInput from '@/components/RouteInput'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/themes/airbnb.css'
import {Mandarin} from 'flatpickr/dist/l10n/zh'

import fontawesome from '@fortawesome/fontawesome'
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
    tripTypeTab (sender) {
      this.form.tripType = Number(sender.toElement.parentElement.id)
    },
    submit (event) {
      event.preventDefault()
      this.$emit('submit', this.form)
    }
  },
  components: {
    flatPickr, RouteInput
  }
}
</script>

<style>
  .flatpickr-input {
    text-align: center;
  }
</style>
