<template>
<div class="py-5" id="ticket-panel-row">
  <b-container>
    <b-row>
      <b-col md="6">
        <route-input @submit="submit"/>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script>
  import RouteInput from '@/components/ticket/RouteInputPanel'
  export default {
    name: 'ticket',
    props: [],
    methods: {
      submit (event) {
        this.$router.push({
          path: 'list',
          query: {
            from: event.departureStation,
            to: event.arrivalStation,
            date: event.date
          }
        })
      }
    },
    components: { RouteInput }
  }
</script>

<style scoped>
#ticket-panel-row {
  background-height:100%;
  background-position: center top;
}
</style>