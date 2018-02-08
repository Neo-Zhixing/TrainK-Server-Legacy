<template>
  <b-card class="text-center w-100" style="opacity: .95;">
    <b-nav fill tabs class="card-header-tabs" slot="header">
      <b-nav-item :active="form.tripType==1" @click="form.tripType = 1">单程</b-nav-item>
      <b-nav-item disabled :active="form.tripType==2" @click="form.tripType = 2">往返</b-nav-item>
    </b-nav>
    <b-form @submit.prevent="submit">
      <b-form-group label="行程" label-for="route-form-input">
        <route-input id="route-form-input" required v-model="form" />
      </b-form-group>
      <b-form-group label="日期" label-for="date-form-input">
        <flat-pickr
        id="date-form-input"
        class="form-control"
        placeholder="选择日期"
        v-model="form.date"
        :config="datepickerConfig"/>
      </b-form-group>
      <b-button block variant="primary" size="lg" type="submit" :disabled="!form.date || !form.arrivalStation || !form.departureStation">搜索</b-button>
    </b-form>
  </b-card>
</template>

<script>
import RouteInput from '@/components/RouteInput'
import flatPickr from 'vue-flatpickr-component'
import {Mandarin} from 'flatpickr/dist/l10n/zh'

import fontawesome from '@fortawesome/fontawesome'
import { faArrowsAltH } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faArrowsAltH)

export default {
  name: 'TicketInputPanel',
  props: {
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
    submit (event) {
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
