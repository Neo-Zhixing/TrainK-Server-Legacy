<template>
<div class="py-5" id="ticket-panel-row">
  <b-container>
    <b-row>
      <b-col md="6">
        <ticket-input-panel @submit="submit"/>
      </b-col>
    </b-row>
  </b-container>
</div>
</template>

<script>
  import TicketInputPanel from './TicketInputPanel'
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
    components: {
      TicketInputPanel
    }
  }
</script>

<style scoped>
#ticket-panel-row {
  background-image: url("../static/img/features.jpg");
  background-height:100%;
  background-position: center top;
}
</style>