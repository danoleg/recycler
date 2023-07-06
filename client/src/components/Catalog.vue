<template>
  <div class="md-layout md-gutter">
    <div class="md-layout-item container" >
<!--      <md-button class="md-fab" @click="active = true" style="position:absolute; top: 0px; left: 15px">-->
<!--        <md-icon>edit</md-icon>-->
<!--      </md-button>-->
<!--      <div>-->
<!--        <md-dialog-prompt-->
<!--            :md-active.sync="active"-->
<!--            v-model="value"-->
<!--            :md-title= this.getMessage()-->
<!--            md-input-placeholder="100"-->
<!--            type="number"-->
<!--            v-on:md-confirm="setData"-->
<!--            md-confirm-text="Done" />-->
<!--      </div>-->
      <div class="left">
        <md-button class="md-icon-button md-raised md-primary" @click="getCurrentLocation" style="position:absolute; bottom: 10px; left: 25px">
          <md-icon>my_location</md-icon>
        </md-button>
        <MyMaper :items="items" :longitude="longitude" :latitude="latitude" v-if="mapVisible" v-on:setNewAddress="setNewAddress"></MyMaper>
      </div>
      <div class="right">
        <md-button class="md-icon-button md-raised md-primary" @click="active=true" style="position:absolute; top: -65px; right: 15px">
          <md-icon>add</md-icon>
        </md-button>
        <md-card v-if="active" class="ad_card">
          <md-card-content>
            <md-field>
              <label>Title</label>
              <md-input v-model="new_title"></md-input>
            </md-field>
            <md-field>
              <label>Description</label>
              <md-textarea v-model="new_descr" md-autogrow></md-textarea>
            </md-field>
            <md-datepicker v-model="new_date">
              <label>Event date</label>
            </md-datepicker>
            <md-field>
              <span>Location: {{new_location ? new_location.display_name: "Click to map for selecting"}}</span>
            </md-field>
          </md-card-content>

          <md-card-actions>
            <md-button v-on:click="active=false">Close</md-button>
            <md-button v-on:click="addNewItem()">Create</md-button>
          </md-card-actions>


        </md-card>
        <div v-if="items.length === 0" style="text-align: center">
          Create your first item with "plus" button or
          <md-button v-on:click="uploadData()">Upload demo data</md-button>
        </div>
        <AdsList :items="items" v-on:setLongitude="setLongitude" v-on:setLatitude="setLatitude"></AdsList>
      </div>

    </div>

  </div>

</template>

<script>
import axios from "axios";
import AdsList from './AdsList';
import MyMaper from './MyMaper';


export default {
  name: "Catalog",
  components: {
    AdsList,
    MyMaper
  },
  data() {
    return {
      new_title: null,
      new_descr: null,
      new_date: null,
      new_location: null,
      longitude: null,
      latitude: null,
      checked: false,
      global_is_exist: false,
      active: false,
      processing: false,
      formdata: {},
      mapVisible: true,
      items: [],
      userLocation: null
    };
  },
  mounted() {
    let that = this;
    this.formdata = {
      name: 'Items'
    };
    axios.post('http://185.69.153.16:8011/check-global-from-iris', this.formdata).then(
        function (response) {
          if (response.data.data > 0){
            that.getData();
          }else{
            that.checked = true;
          }
        });
  },
  methods: {
    getCurrentLocation(){
      if (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1" && window.location.protocol !== "https:") {
        alert("HTTPS required");
      }
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            this.onLocationSuccess.bind(this),
            this.onLocationError.bind(this)
        );
      } else {
        console.error("Geolocation is not supported by this browser.");
      }
    },
    onLocationSuccess(position) {
      const { latitude, longitude } = position.coords;
      // Store the user's location coordinates in the data property
      this.setLatitude(latitude)
      this.setLongitude(longitude)
    },
    onLocationError(error) {
      console.error("Error getting user location:", error);
    },
    setLongitude(longitude){
      this.longitude = longitude;
      this.mapVisible = false;

      this.$nextTick(() => {
        // Adding the component back in
        this.mapVisible = true;
      });
    },
    setLatitude(latitude){
      this.latitude = latitude;
    },
    setNewAddress(address){
      this.new_location = address;
    },
    addNewItem(){
      if(this.new_location !== null){
        let i = {
          "title": this.new_title,
          "description": this.new_descr,
          "location": this.new_location.display_name,
          "country": this.new_location.address.country,
          "city": this.new_location.address.city,
          "datetime": this.new_date.getDate()+'.'+this.new_date.getMonth()+'.'+this.new_date.getFullYear() ,
          "longitude": this.new_location.lon,
          "latitude": this.new_location.lat,
          "number": this.items.length
        }
        this.setData(i)
        this.items.unshift(i)
        this.active = false;
        this.new_descr = null;
        this.new_title = null;
        this.new_location = null;
        this.new_date = null;
        this.mapVisible = false;

        this.$nextTick(() => {
          // Adding the component back in
          this.mapVisible = true;
        });
      }
    },
    uploadData() {
      this.processing = true;
      this.formdata = {};
      let that = this;
      axios.post('http://185.69.153.16:8011/import-dataset', this.formdata).then(
          function (response) {
            if(response.data.status){
              that.getData();
              // that.global_is_exist = true;
              // that.checked = true;
              //
              // let that_i = that;
              // axios.post('http://185.69.153.16:8011/data/getting/month', that.formdata).then(
              //     function (response) {
              //       that_i.values = response.data.data;
              //       that_i.value = response.data.value;
              //     });
            }
          });
    },
    getData() {
      this.formdata = {
        year: this.year
      };
      let that = this;
      axios.post('http://185.69.153.16:8011/data/getting', this.formdata).then(
          function (response) {
            that.items = response.data.data;
            that.mapVisible = false;

            that.$nextTick(() => {
              // Adding the component back in
              that.mapVisible = true;
            });
          });
    },
    setData(item) {
      this.formdata = item;
      let that = this;
      axios.post('http://185.69.153.16:8011/data/set', this.formdata).then(
          function (response) {
            if(response.data.status){
              that.getData()
            }
          });
    },
    deleteItem(item) {
      this.formdata = item;
      let that = this;
      axios.post('http://185.69.153.16:8011/data/delete', this.formdata.id).then(
          function (response) {
            if(response.data.status){
              that.getData()
            }
          });
    }
  }
}
</script>

<style scoped>
/*@import url('./node_modules/ol/src/ol.css');*/
.md-radio {
  display: flex;
}
.md-theme-purple-card{
  left: 15px;
  width: 280px;
  position: absolute;
  top: 63vh;
}
.container{
  display: flex;
  height: calc(100vh - 104px);
  position: relative;
}
.left {
  width: 75%;
  height:100%;
  display: flex;
  flex-direction: column;
  align-content: space-between;
  justify-content: space-around;
}
.map{
  display: flex;
  position: relative;
  align-items: center;
  justify-content: center;
  width: 100%;
}
.right {
  width: 25%;
}
.chart-container{
  width: 100%;
}
.chart-container>div{
  height:100px;
  width: 100%;
}
#line-chart{
  width: 100%;
}
.upload{
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 64px);
}
</style>