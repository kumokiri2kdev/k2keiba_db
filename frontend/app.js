Vue.component('racelistmini', {
  template: '\
    <div>\
      <button class="btn btn-info" data-toggle="modal" v-bind:data-target=idtagx>レース一覧</button>\
      <div class="modal fade" v-bind:id=idtag tabindex="-1">\
        <div class="modal-dialog" v-on:click="test">\
          <div class="modal-content">\
            <div class="modal-header">\
              <h5 class="modal-title">{{this.place.index}}回{{this.place.day}}日目　{{this.place.place}}</h5>\
              <button class="close" data-dismiss="modal"><span>&times;</span></button>\
            </div>\
            <div class="modal-body">\
              <ul class="list-group">\
                <li v-for="race in place.race" :key="race.id" class="list-group-item d-flex justify-content-between align-items-center">\
                  <div style="width: 10%;">\
                    {{race.idx}}R\
                  </div>\
                  <div style="width: 80%;">\
                    {{race.cond}}\
                  </div>\
                  <div class="badge badge-primary badge-pill" style="width: 10%;">{{race.uma_num}}</div>\
                </li>\
                </ul>\
              </div>\
            <div class="modal-footer">\
              <button class="btn btn-secondary" data-dismiss="modal">閉じる</button>\
            </div>\
          </div>\
        </div>\
      </div>\
    </div>'
    ,
    props:['place'],
    data() {
      return {
        idtag: this.place.place + this.place.index + this.place.day,
        idtagx : '#' + this.place.place + this.place.index + this.place.day
      }
    },
    mounted :function(){
      console.log("mounted");
      console.log(this.place);
    },
    methods : {
      test: function(event){
        console.log("On Click");
      }
    }
})


Vue.component('placecard', {
  template: '\
    <div class="col-md-6 col-lg-4 mb-4" v-on:click="test">\
      <div class="card border-primary text-primary">\
        <h4 class="card-header">{{place.place}}</h4>\
        <div class="card-body" style="width:500px;">\
          <h5 class="card-title">title</h5>\
          <racelistmini v-bind:place=this.place>></racelistmini>\
        </div>\
      </div>\
    </div>\
  '
  ,
  props:['place'],
  mounted :function(){
    console.log("mounted");
    console.log(this.place);
  },
  methods : {
    test: function(event){
      console.log("On Click");
      console.log(this.place);
    }
  }
})




Vue.component('kaisaicard', {
  template: '\
    <div>\
      <div class="row">\
        <p>{{info.day}}</p>\
      </div>\
      <div class="row">\
        <placecard v-for="place in info.places" :key="place.place" v-bind:place=place>\
        </placecard>\
      </div>\
    </div>\
  '
  ,
    props:['info'],
  mounted :function(){
    console.log("mounted");
  },
  methods : {
    func_a: function() {
      console.log("func_a")
    }
  }
})

const Foo = { template: '<foo></foo>' }
const Bar = { template: '<div>bar</div>' }

const routes = [
  { path: '/foo', component: Foo },
  { path: '/bar', component: Bar }
]

const router = new VueRouter({
  routes // `routes: routes` の短縮表記
})

const app = new Vue({
  router,
  data() {
    return {
      kaisai: []
    }
  },
  methods : {
    rootDataHandler: function(data) {
      console.log(data.data);
      this.kaisai = data.data;
    }


  },
  mounted :function(){
  axios.get('http://127.0.0.1:5000/')
      .then(function(response){
        //console.log(response)
        this.rootDataHandler(response.data);
      }.bind(this))
      .catch(response => console.log(response))
  }
}).$mount('#app')
