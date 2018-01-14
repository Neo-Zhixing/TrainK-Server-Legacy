<template>
  <b-container class="py-5">
    <b-row>
      <b-col md="8" class="text-center">
        <b-list-group>
          <b-list-group-item>
            <b-row class="py-2">
              <b-col sm="4">
                <h3>南京</h3>
                <h1>10:11</h1>
              </b-col>
              <b-col sm="4">
                <p>0:53</p>
                <h3 class="separate-line">G333</h3>
                
              </b-col>
              <b-col sm="4">
                <h3>合肥</h3>
                <h1>10:11</h1>
              </b-col>
            </b-row>
          </b-list-group-item>
          <b-list-group-item>
            <b-row class="py-2">
              <b-col sm="4">
                <h3>南京</h3>
                <h1>10:11</h1>
              </b-col>
              <b-col sm="4">
                <p>0:53</p>
                <h3 class="separate-line">G333</h3>
                
              </b-col>
              <b-col lsm="4">
                <h3>合肥</h3>
                <h1>10:11</h1>
              </b-col>
            </b-row>
          </b-list-group-item>
        </b-list-group>
        </b-list-group>
      </b-col>
      <b-col md="4">
        <b-card title="添加行程"
          img-src="https://lorempixel.com/600/300/food/5/"
          img-alt="Image"
          img-top>
          <b-form>
            <b-form-group label="车次">
              <b-form-input v-model='addForm.train'/>
            </b-form-group>
            <b-form-group label="日期">
              <b-form-input v-model='addForm.date' />
            </b-form-group>
            <b-button block v-b-modal.addTrip variant="primary">添加</b-button>
            <b-modal lazy id="addTrip" size="lg" title="添加行程">
              <trip-add-view v-model='addForm' />
            </b-modal>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import TripAddView from './Add.vue'
export default {
  data () {
    return {
      addForm: {
        train: '',
        date: ''
      },
      addModalShow: false
    }
  },
  components: {
    TripAddView
  }
}
</script>
<style>
.separate-line{
  padding: 0 20px 0;
  margin: 20px 0;
  line-height: 1px;
  border-left: 50px solid #ddd;
  border-right: 50px solid #ddd;
  text-align: center;
}
</style>