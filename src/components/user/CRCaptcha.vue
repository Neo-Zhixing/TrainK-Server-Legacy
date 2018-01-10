<template>
<div style="position: relative;" ref="captchawrapper">
  <b-img fluid-grow draggable="false" :src="captchaImageURL" ref="captcha" @click="addCursor" @click.right.prevent />
  <b-button class="captcha-component" size="sm" variant="outline-secondary" style="right: 0; top: 0;" @click="reloadCaptcha">
    <font-awesome-icon icon="sync-alt" />
    刷新
  </b-button>
  <font-awesome-icon icon="bullseye"
  class="captcha-component"
  v-for="cursor in cursors"
  :id="cursor.id"
  :key="cursor.id"
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
      cursorID: 0,
      cursors: []
    }
  },
  mounted () {
    this.reloadCaptcha()
  },
  methods: {
    addCursor (event) {
      this.cursorID ++
      let rect = event.target.getBoundingClientRect()
      let offsetX = event.clientX - rect.left
      let offsetY = event.clientY - rect.top
      this.cursors.push({
        x: offsetX / this.$refs.captchawrapper.clientWidth,
        y: offsetY / this.$refs.captchawrapper.clientHeight,
        id: this.cursorID
      })
    },
    removeCursor (event) {
      let target = event.target
      if (target.tagName !== 'svg') target = target.parentElement
      console.log(target.id)
      this.cursors = this.cursors.filter((a) => String(a.id) !== target.id)
    },
    reloadCaptcha () {
      this.captchaImageURL = `//kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&${Math.random()}`
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