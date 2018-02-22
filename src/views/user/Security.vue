<template>
  <b-form novalidate @submit.prevent="submit">
    <b-card class="mb-4">
      <b-form-group horizontal
      label="密码"
      label-size="lg">
        <b-form-group label="当前密码:" label-for="old-password-field">
          <b-form-input id="old-password-field" name="old_password" autocomplete="current-password"
            :class="{'is-invalid': errors.has('old_password') }"
            type="password"
            v-validate="'required'"
            v-model="passwordChangeForm.old_password"
          />
          <b-form-invalid-feedback v-for="details in errors.collect('old_password')" :key="details">{{ details }}</b-form-invalid-feedback>
        </b-form-group>
        <b-form-group label="新密码:" label-for="new-password1-field">
          <b-form-input id="new-password1-field" name="new_password1" autocomplete="new-password"
            :class="{'is-invalid': errors.has('new_password1') }"
            type="password"
            v-validate="'required|min:8|max:128'"
            v-model="passwordChangeForm.new_password1"
          />
          <b-form-invalid-feedback v-for="details in errors.collect('new_password1')" :key="details">{{ details }}</b-form-invalid-feedback>
        </b-form-group>
        <b-form-group label="再次输入:" label-for="new-password2-field">
          <b-form-input id="new-password2-field" name="new_password2" autocomplete="new-password"
            :class="{'is-invalid': errors.has('new_password2') }"
            type="password"
            v-validate="'confirmed:new_password1'"
            v-model="passwordChangeForm.new_password2"
          />
          <b-form-invalid-feedback v-for="details in errors.collect('new_password2')" :key="details">{{ details }}</b-form-invalid-feedback>
        </b-form-group>
        <b-button type="submit" variant="primary" class="float-right"
          :disabled="Object.keys(fields).some(key => fields[key].invalid)"
        >
          保存
          <font-awesome-icon :icon="loading ? 'spinner' : 'save'" :spin="loading" />
        </b-button>
        <b-modal ok-only lazy title="密码修改" size="sm" v-model="showSuccessModel">
          <p>您的密码已经被成功修改！</p>
          <p>请牢记修改后的密码。</p>
        </b-modal>
      </b-form-group>
    </b-card>
  </b-form>
</template>

<script>
import axios from '@/utils/axios'
export default {
  data () {
    return {
      loading: false,
      showSuccessModel: false,
      passwordChangeForm: {
        new_password1: '',
        new_password2: '',
        old_password: ''
      }
    }
  },
  computed: {
    formInvalid () {
      return Object.keys(this.fields).some(key => this.fields[key].invalid)
    }
  },
  methods: {
    submit () {
      this.$validator.validateAll()
      .then(result => {
        if (result) {
          this.loading = true
          axios.put('/user/password/', this.passwordChangeForm)
          .then((response) => {
            this.loading = false
            this.showSuccessModel = true
            this.old_password = ''
            this.new_password1 = ''
            this.new_password2 = ''
          })
          .catch((error) => {
            this.loading = false
            if (error.response) {
              for (let key in error.response.data) {
                for (let errorDetails of error.response.data[key]) this.errors.add(key, errorDetails)
              }
            }
          })
        }
      })
    }
  }
}
</script>