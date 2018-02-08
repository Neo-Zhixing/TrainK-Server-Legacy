<template>
<b-card class="text-center" style="opacity: .95;">
  <b-nav fill tabs class="card-header-tabs" slot="header">
    <b-nav-item :active="selectedTab === 1" @click="tripTypeTab(1)">行程</b-nav-item>
    <b-nav-item :active="selectedTab === 2" @click="tripTypeTab(2)">车次</b-nav-item>
    <b-nav-item :active="selectedTab === 3" @click="tripTypeTab(3)">站点</b-nav-item>
    <b-nav-item disabled :active="selectedTab === 4" @click="tripTypeTab(4)">线路</b-nav-item>
  </b-nav>
  <b-form id="info-form" @submit.prevent="submit">
    <route-input required v-if="selectedTab === 1" v-model="stations" />
    <station-input required v-else-if="selectedTab === 3" v-model="value" placeholder="选择车站" />
    <b-form-input required v-else
      class="text-center"
      v-model="value"
      :placeholder="selectedTab === 2 ? 'G1' : '京津城际'"
      />
    <b-button block variant="primary" size="lg" type="submit">搜索</b-button>
  </b-form>
</b-card>
</template>

<script>
  import RouteInput from '@/components/RouteInput'
  import StationInput from '@/components/StationInput'
  export default {
    name: 'TicketInputPanel',
    data () {
      return {
        selectedTab: 1,
        value: null,
        stations: {
          departureStation: null,
          arrivalStation: null
        }
      }
    },
    methods: {
      tripTypeTab (id) {
        this.selectedTab = id
        this.value = null
        this.stations.departureStation = null
        this.stations.arrivalStation = null
      },
      submit (event) {
        let rootPath = '/info/'
        if (this.selectedTab === 1) {
          window.location = `${rootPath}train?from=${this.stations.departureStation}&to=${this.stations.arrivalStation}`
          return
        }
        let url = this.selectedTab === 2 ? 'train/' : (this.selectedTab === 3 ? 'station/' : 'xxx')
        window.location = rootPath + url + this.value
      }
    },
    components: {
      RouteInput, StationInput
    }
  }
</script>

<style>
  #info-form > .input-group,
  #info-form > .form-control,
  #info-form > .multiselect
   {
    margin-bottom: 3rem;
    margin-top: 1rem;
  }
</style>
