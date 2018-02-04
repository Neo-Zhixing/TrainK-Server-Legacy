<template>
  <div class="d-flex flex-row">
    <b-img rounded class="mr-2" src="http://gravatar.tra.ink/avatar/32f47f0c1d23f9f584e3aa23db920a6f" />
    <div class="mx-2">
      <h4 class="text-dark">{{value.passenger_name}}</h4>
      <h6 class="text-secondary m-0">{{value.passenger_id_type_name}}: {{value.passenger_id_no}}</h6>
      <small class="text-muted">{{value.mobile_no}}</small>
    </div>
    <div class="ml-auto">
      <b-button variant="danger" class="float-right">
        <font-awesome-icon :icon="minusIcon" />
      </b-button>
      <b-button-group>
        <b-button
          v-for="(type, index) in ticketTypes"
          :variant="index === selectedTicketType ? type.variant : 'outline-secondary'"
          @click="selectedTicketType = index"
        >
          <font-awesome-icon :icon="type.icon" />
          {{type.name}}
        </b-button>
      </b-button-group>
    </div>
  </div>
</template>


<script>
import { faMale, faChild, faGraduationCap, faMinus } from '@fortawesome/fontawesome-free-solid'
import { faAccessibleIcon } from '@fortawesome/fontawesome-free-brands'
export default {
  props: ['value'],
  data () {
    return {
      selectedTicketType: 0
    }
  },
  computed: {
    minusIcon () { return faMinus },
    ticketTypes () {
      return [
        { name: '成人', icon: faMale, variant: 'primary' },
        { name: '儿童', icon: faChild, variant: 'success' },
        { name: '学生', icon: faGraduationCap, variant: 'info' },
        { name: '残军', icon: faAccessibleIcon, variant: 'warning' }
      ]
    }
  },
  methods: {
    remove () {}
  }
}
</script>