<template>
  <div>
    <b-row>
      <b-col cols="4">
      </b-col>
      <b-col cols="8">
        User Details
        lka sdfjkq ewfi mkf
        fdaskl mf qwe klv dsafqwe fdekwrk wreq jkqwkjerqwkdf wa knw afdkfd
      </b-col>
    </b-row>
    <b-button-group class="btn-block mt-2">
      <a class="btn btn-primary col-7" href="/user">用户中心<font-awesome-icon icon="cloud" /></a>
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
import axios from 'axios'
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
  methods: {
    logout () {
      this.errorMessage = null
      this.loading = true
      axios.delete('/user/session')
      .then((response) => {
        this.loading = false
        this.$emit('loggedOut')
      })
      .catch((error) => {
        this.loading = false
        if (error.response) this.errorMessages = error.response.data
        else this.errorMessage = error.message
      })
    }
  }
}
</script>