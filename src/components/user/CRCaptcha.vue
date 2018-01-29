<template>
<div class="position-relative" ref="captchawrapper">
  <b-img fluid-grow style="user-drag: none; user-select: none;" :src="captchaImageURL" ref="captcha" @click="addCursor" @click.right.prevent />
  <b-button class="captcha-component" size="sm" variant="outline-secondary" style="right: 0px; top: 0px;" @click="reloadCaptcha">
    <font-awesome-icon icon="sync-alt" />
    刷新
  </b-button>
  <font-awesome-icon icon="bullseye"
  class="captcha-component"
  v-for="(cursor, index) in cursors"
  :data-index="index"
  :id="'cr-captcha-cursor-' + index"
  :key="cursor.x + '-' + cursor.y"
  :style="{left: `calc(${cursor.x*100}% - 8px)`, top: `calc(${cursor.y*100}% - 8px)`}"
  @click.right.prevent="removeCursor" />
</div>
</template>

<script>
import fontawesome from '@fortawesome/fontawesome'
import { faBullseye, faSyncAlt } from '@fortawesome/fontawesome-free-solid'
fontawesome.library.add(faBullseye, faSyncAlt)

export default {
  data () {
    return {
      captchaImageURL: null,
      cursors: []
    }
  },
  mounted () {
    this.reloadCaptcha()
  },
  computed: {
    stringValue () {
      if (this.cursors.length === 0) return null
      let points = []
      for (let cursor of this.cursors) {
        points.push(Math.round(cursor.x * 293))
        points.push(Math.round(cursor.y * 190 - 35))
      }
      return points.join()
    }
  },
  methods: {
    addCursor (event) {
      if (this.cursors.length >= 8) this.cursors.shift()
      let rect = event.target.getBoundingClientRect()
      let offsetX = event.clientX - rect.left
      let offsetY = event.clientY - rect.top
      this.cursors.push({
        x: offsetX / this.$refs.captchawrapper.clientWidth,
        y: offsetY / this.$refs.captchawrapper.clientHeight,
        id: this.cursorID
      })
      this.$emit('input', this.stringValue)
    },
    removeCursor (event) {
      let target = event.target
      if (target.tagName !== 'svg') target = target.parentElement
      console.log(target.id)
      this.cursors.splice(target.id.slice(-1), 1)
      this.$emit('input', this.stringValue)
    },
    reloadCaptcha () {
      this.captchaImageURL = `/cr/user/session/captcha?${Math.random()}`
      this.cursors = []
      this.$emit('input', null)
    }
  }
}
</script>

<style>
.captcha-component {
  position: absolute;
  user-drag: none; 
  user-select: none;
}
</style>