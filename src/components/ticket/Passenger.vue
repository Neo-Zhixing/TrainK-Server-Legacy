<template>
  <div class="d-flex flex-row">
    <b-img rounded class="mr-2" src="http://gravatar.tra.ink/avatar/32f47f0c1d23f9f584e3aa23db920a6f" />
    <div class="mx-2">
      <h4 class="text-dark">张之行</h4>
      <h6 class="text-secondary m-0">E59954315</h6>
      <small class="text-muted">17355104365</small>
    </div>
    <div class="ml-auto">
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
import { faMale, faChild, faGraduationCap } from '@fortawesome/fontawesome-free-solid'
import { faAccessibleIcon } from '@fortawesome/fontawesome-free-brands'
export default {
  data () {
    return {
      selectedTicketType: 0
    }
  },
  computed: {
    ticketTypes () {
      return [
        { name: '成人', icon: faMale, variant: 'primary' },
        { name: '儿童', icon: faChild, variant: 'success' },
        { name: '学生', icon: faGraduationCap, variant: 'info' },
        { name: '残军', icon: faAccessibleIcon, variant: 'warning' }
      ]
    }
  }
}
</script>