
<template>
  <div class="content">
    <b-container>
      <!-- Content here -->
      <b-row class="text-left">
          <b-col class="left">
            <h4>Completed: {{nComplete}}</h4>
            <div v-for="(o, index) in order">
              <a :class="{'name selected complete': index==startIdx && completed[index], 'name complete': index != startIdx && completed[index], 'name selected incomplete': index==startIdx && !completed[index], 'name incomplete': index != startIdx && !completed[index]}"
                 @click="setIdx(index)">
                 {{o.Name}}
              </a>
            </div>
          </b-col>
          <b-col cols="8" class="right">
            <b-row>
              <iframe class="pdfView" :src="currentPDF"></iframe>
            </b-row>
            <b-row class="mt-3 pt-3">
              <b-col>
                <h6>Computing</h6>
                <vue-slider @callback="save" v-model="currentApplicant.Computing" tooltipDir="bottom" :width="200" :min="0" :max="10" :piecewise="true"></vue-slider>
              </b-col>

              <b-col>
                Neuroscience
                <vue-slider @callback="save" v-model="currentApplicant.Neuroscience" tooltipDir="bottom" :width="200" :min="0" :max="10" :piecewise="true"></vue-slider>
              </b-col>

              <b-col>
                Statement
                <vue-slider @callback="save" v-model="currentApplicant.Statement" tooltipDir="bottom" :width="200" :min="0" :max="10" :piecewise="true"></vue-slider>
              </b-col>
            </b-row>

          </b-col>
      </b-row>

    </b-container>

  </div>
</template>

<style>

  .name {
    cursor: pointer;
    padding: 2px;
  }

  .selected {
    background-color: #007bff;
    color: white !important;
  }

  .selected.completed {
    color: white !important;
  }

  .incomplete {
    color: #dc3545 !important;
  }

  .content, html, body {
      height: 90%;
  }
  .left {
      float: left;
      width: 50%;
      padding: 5px;
      height: calc(100vh - 80px);
      max-height: calc(100vh - 80px);
      overflow: scroll;
  }
  .right {
      float: left;
      width: 50%;
      height: calc(100vh - 80px);
      max-height: calc(100vh - 80px);
      overflow: scroll;
  }
  .pdfView {
    height: 75VH;
    width: 100%;
  }
</style>

<script>
import axios from 'axios'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import vueSlider from 'vue-slider-component'

Vue.use(BootstrapVue)
Vue.use(vueSlider)

export default {
  data () {
    return {
      randomNumber: 0,
      order: [],
      startIdx: 0
    }
  },
  components: {vueSlider},
  computed: {
    currentApplicant () {
      if (this.order.length) {
        return this.order[this.startIdx]
      } else {
        return {}
      }
    },
    currentPDF () {
      if (this.currentApplicant) {
        return `http://localhost:5000/api/pdf/${this.currentApplicant.Name}`
      } else {
        return null
      }
    },
    completed () {
      const completed = []
      this.order.forEach((val) => {
        if (val.Computing !== 0 && val.Neuroscience !== 0 && val.Statement !== 0) {
          completed.push(true)
        } else {
          completed.push(false)
        }
      })
      return completed
    },
    nComplete () {
      let n = 0
      this.completed.forEach((v) => {
        if (v) {
          n += 1
        }
      })
      return n
    }
  },
  methods: {
    save () {
      axios.post('http://localhost:5000/api/save', this.order).then(() => {
        console.log('success')
      }).catch((e) => {
        console.log('error', e)
      })
    },
    setIdx (index) {
      this.startIdx = index
    },
    getRandomInt (min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    getRandom () {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.randomNumber = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      const path = `http://localhost:5000/api/random`
      axios.get(path)
      .then(response => {
        console.log(response)
        this.randomNumber = response.data.randomNumber
        this.order = response.data.order
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
  created () {
    this.getRandom()
  }
}
</script>
