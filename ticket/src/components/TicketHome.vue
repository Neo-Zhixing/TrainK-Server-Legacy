<template>
<div class="py-5">
  <b-container>
    <b-row>
      <b-col md="6">
        <ticket-input-panel/>
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
    data () {
      return {
      }
    },
    components: {
      TicketInputPanel
    }
  }
</script>

<style scoped>
</style>