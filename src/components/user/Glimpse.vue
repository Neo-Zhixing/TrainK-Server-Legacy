<template>
  <div>
    <b-row>
      <b-col cols="4">
        <b-img rounded="circle" :src="`//gravatar.tra.ink/avatar/${user.hash}`" />
      </b-col>
      <b-col cols="8">
        {{user.username}}
        {{user.email}}
      </b-col>
    </b-row>
    <b-button-group class="btn-block mt-2">
      <router-link class="btn btn-primary col-7" :to="{name:'User-Setting'}">用户中心<font-awesome-icon icon="cloud" /></router-link>
      <b-button variant="outline-danger" class="col-5" @click="logout">
        登出
        <font-awesome-icon :icon="loading ? 'spinner' : 'sign-out-alt'" :spin="loading" /></b-button>
    </b-button-group>
    <b-alert :show='errorMessage !== null' variant="danger" class="py-3">
      {{ errorMessage }}
    </b-alert>
  </div>
</template>



<script>
import { states } from '@/store/auth'
import { faSignOutAlt, faCloud, faSpinner } from '@fortawesome/fontawesome-free-solid'
import fontawesome from '@fortawesome/fontawesome'
fontawesome.library.add(faSignOutAlt, faCloud, faSpinner)

export default {
  data () {
    return {
      loading: false,
      errorMessage: null
    }
  },
  computed: states,
  methods: {
    logout () {
      this.errorMessage = null
      this.loading = true
      this.$store.dispatch('auth/logout')
      .then(user => {
        this.loading = false
      })
      .catch(error => {
        this.loading = false
        if (error.response) this.errorMessages = error.response.data.non_field_errors
        else this.errorMessages = [error.message]
      })
    }
  }
}
</script>