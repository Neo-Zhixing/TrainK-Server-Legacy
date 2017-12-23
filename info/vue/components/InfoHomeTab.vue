<template>
<b-card no-body class="text-center" style="opacity: .95;">
  <b-tabs card v-model="selectedTab">
    <b-tab title="行程" active>
      <route-input v-model="stations" />
    </b-tab>
    <b-tab title="车次">
      <b-form-input class="text-center"
      v-model="value"
      placeholder="G1"
      />
    </b-tab>
    <b-tab title="车站">
      <station-input all v-model="value" placeholder="北京南"/>
    </b-tab>
    <b-tab disabled title="线路">
    </b-tab>
  </b-tabs>
  <b-button @click="submit" class="my-3 mx-3" variant="primary" size="lg" type="submit">搜索</b-button>
</b-card>
</template>

<script>
  import RouteInput from '../../../vue/components/RouteInput'
  import StationInput from '../../../vue/components/StationInput'
  export default {
    name: 'TicketInputPanel',
    data () {
      return {
        selectedTab: 0,
        value: null,
        stations: {
          departureStation: null,
          arrivalStation: null
        }
      }
    },
    methods: {
      tripTypeTab (sender) {
        this.selectedTab = Number(sender.toElement.parentElement.id)
        this.value = null
        this.stations.departureStation = null
        this.stations.arrivalStation = null
      },
      submit (event) {
        event.preventDefault()
        let rootPath = '/info/'
        if (this.selectedTab === 0) {
          window.location = `${rootPath}train?departure_telecode=${this.stations.departureStation}&arrival_telecode=${this.stations.arrivalStation}`
          return
        }
        let url = this.selectedTab === 1 ? 'train?name=' : (this.selectedTab === 2 ? 'station?telecode=' : 'xxx')
        window.location = rootPath + url + this.value
      }
    },
    components: {
      RouteInput, StationInput
    }
  }
</script>
