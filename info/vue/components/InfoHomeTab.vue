<template>
<b-card class="text-center" style="opacity: .95;">
  <b-nav fill tabs class="card-header-tabs" slot="header">
    <b-nav-item :active="selectedTab === 1" id="1" @click="tripTypeTab">行程</b-nav-item>
    <b-nav-item :active="selectedTab === 2" id="2" @click="tripTypeTab">车次</b-nav-item>
    <b-nav-item :active="selectedTab === 3" id="3" @click="tripTypeTab">站点</b-nav-item>
    <b-nav-item disabled :active="selectedTab === 4" id="4" @click="tripTypeTab">线路</b-nav-item>
  </b-nav>
  <b-form @submit="submit">

    <route-input class="text-center my-3" v-if="selectedTab === 1" v-model="stations" />
    <b-form-input v-else
      class="text-center my-3"
      v-model="value"
      :placeholder="selectedTab === 2 ? 'G1' : (selectedTab === 3 ? '北京南' : '京津城际')"
      />
    <b-button block variant="primary" size="lg" type="submit">搜索</b-button>
  </b-form>
</b-card>
</template>

<script>
  import RouteInput from '../../../vue/components/RouteInput'
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
      tripTypeTab (sender) {
        this.selectedTab = Number(sender.toElement.parentElement.id)
        this.value = null
        this.stations.departureStation = null
        this.stations.arrivalStation = null
      },
      submit (event) {
        event.preventDefault()
        let rootPath = '/info/'
        if (this.selectedTab === 1) {
          window.location = rootPath + "train?departure_name=" + this.stations.departureStation + '&arrival_name=' + this.stations.arrivalStation
          return
        }
        let url = this.selectedTab === 2 ? 'train?name=' : (this.selectedTab === 3 ? 'station?name=' : 'xxx')
        window.location = rootPath + url + this.value
      }
    },
    components: {
      RouteInput
    }
  }
</script>
