<template>
<div>
  <b-card class="mb-4">
    <b-form @submit.prevent="submit">
      <b-form-group class="mb-4" horizontal
      label="基本信息"
      label-size="lg">
        <b-form-group label="用户名:" label-for="username-field">
          <b-form-input id="username-field"
            type="text"
            v-model="form.username"
            required />
        </b-form-group>
        <b-form-group label="姓名:" label-for="name-field">
          <b-input-group>
            <b-form-input id="lastname-field"
              type="text"
              v-model="form.last_name"
              required
              placeholder="张" />
            </b-form-input>
            <b-form-input id="firstname-field"
              type="text"
              v-model="form.first_name"
              required
              placeholder="四铁" />
            </b-form-input>
          </b-input-group>
        </b-form-group>
        <b-button type="submit" variant="primary" class="float-right">
          <font-awesome-icon :icon="loading ? 'spinner' : 'save'" :spin="loading" />
          保存
        </b-button>
      </b-form-group>

    </b-form>
    <b-form-group horizontal label="个人资料" label-size="lg">
      <b-form-group label="地址:" label-for="address">
        <b-form-input readonly class="bg-white" :value="profile.currentLocation" />
      </b-form-group>
      <b-form-group label="关于我:" label-for="address">
        <b-form-textarea readonly class="bg-white" rows="3" :value="profile.aboutMe" />
      </b-form-group>
      <b-form-group label="头像:" horizontal label-for="address">
        <b-img :src="profile.thumbnailUrl" />
      </b-form-group>
      <a class="btn btn-primary float-right" :href="profile.profileUrl">在Gravatar编辑</a>
    </b-form-group>
  </b-card>

  <b-card class="my-4">
    <b-form novalidate>
      <b-form-group horizontal label="邮箱" label-size="lg">
        <b-form-group v-for="email in sortedEmails" :key="email.id">
          <b-input-group>
            <b-form-input :class="{'bg-white': email.verified}" type="email" readonly :value="email.email" />
            <b-input-group-addon v-b-tooltip.hover title="主邮箱" v-if="email.primary">
              <font-awesome-icon icon="envelope" />
            </b-input-group-addon>
            <b-input-group-button v-if="!email.primary || !email.verified">
              <b-button variant="warning"
                v-if="!email.verified"
                v-b-tooltip.hover title="重新发送验证邮件"
                @click="resendVerification">
                <font-awesome-icon class="text-white" :icon="email.loading ? 'spinner' : 'redo'" :spin="email.loading" />
              </b-button>
              <b-button variant="success"
                v-if="!email.primary && email.verified"
                v-b-tooltip.hover title="设为主邮箱"
                @click="makePrimary">
                <font-awesome-icon :icon="email.loading ? 'spinner' : 'arrow-up'" :spin="email.loading" />
              </b-button>
              <b-button variant="danger"
              v-if="!email.primary"
              v-b-tooltip.hover title="移除邮箱"
              @click="removeEmail">
                <font-awesome-icon :icon="email.loading ? 'spinner' : 'minus'" :spin="email.loading" />
              </b-button>
            </b-input-group-button>
          </b-input-group>
        </b-form-group>
        <b-form-group label="添加邮箱：">
          <b-input-group>
            <b-form-input type="email" name="add-email"
              :class="{'is-invalid': errors.has('add-email') }"
              v-validate="'required|email'"
              v-model="newEmail"
            />
            <b-input-group-button>
              <b-button
                :variant="errors.has('add-email') ? 'danger' : 'success'"
                :disabled="errors.has('add-email')"
                @click="addEmail"
              >
                <font-awesome-icon icon="plus" />
              </b-button>
            </b-input-group-button>
          </b-input-group>
        </b-form-group>
      </b-form-group>
    </b-form>
  </b-card>
</div>
</template>

<script>
import axios from '@/utils/axios'
import axiosJsonp from 'axios-jsonp'
import MaskedInput from 'vue-text-mask'
import fontawesome from '@fortawesome/fontawesome'
import { faPlus, faSpinner, faSave, faMinus, faRedo, faArrowUp, faEnvelope } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faPlus, faSpinner, faSave, faMinus, faRedo, faArrowUp, faEnvelope)
export default {
  data () {
    return {
      loading: false,
      emails: [],
      profile: {},
      newEmail: '',
      form: {}
    }
  },
  mounted () {
    axios.get('/user/')
    .then((response) => {
      for (let key of ['username', 'first_name', 'last_name']) this.form[key] = response.data[key]
      return axios.get(`https://en.gravatar.com/${response.data.hash}.json`, {adapter: axiosJsonp})
    })
    .then((response) => {
      console.log(response.data.entry[0])
      this.profile = response.data.entry[0]
    })

    axios.get('/user/email/')
    .then((response) => {
      this.emails = response.data
    })
  },
  methods: {
    submit () {
      this.loading = true
      axios.put('/user/', this.form)
      .then((response) => {
        this.loading = false
        this.form = response.data
        delete this.form.email
      })
    },
    getEmail (event) {
      let target = event.target
      do {
        target = target.parentElement
      } while (target !== null && target.className !== 'input-group')
      if (target === null) return null

      let email = target.firstChild.value
      for (let emailObj of this.emails) {
        if (emailObj.email === email) return emailObj
      }
      return null
    },
    makePrimary (event) {
      let email = this.getEmail(event)
      email.loading = true
      axios.patch(`/user/email/${email.id}/`, {primary: true})
      .then((response) => {
        this.emails.forEach((email) => { email.primary = false })
        email.primary = response.data.primary
        email.loading = false
      })
    },
    resendVerification (event) {
      let email = this.getEmail(event)
      email.loading = true
      axios.patch(`/user/email/${email.id}/`, {verified: true})
      .then((response) => {
        email.loading = false
      })
    },
    removeEmail (event) {
      let email = this.getEmail(event)
      email.loading = true
      axios.delete(`/user/email/${email.id}/`)
      .then((response) => this.emails.splice(this.emails.indexOf(email), 1))
    },
    addEmail () {
      axios.post('/user/email/', {email: this.newEmail})
      .then((response) => {
        this.emails.push(response.data)
        this.newEmail = null
      })
    }
  },
  computed: {
    sortedEmails () {
      return this.emails.sort((a, b) => a.primary ? false : (b.primary ? true : b.verified))
    }
  },
  components: {
    MaskedInput
  }
}
</script>