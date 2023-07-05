<template>
  <div style="height: 100%">
<!--    <div style="padding: 0 30px;">-->
<!--      <md-autocomplete v-model="selectedCity" :md-options="cities">-->
<!--        <label>City</label>-->
<!--      </md-autocomplete>-->
<!--    </div>-->
    <div style="max-height: 85vh; overflow-y: scroll">;
      <md-card v-for="ad in items" v-bind:key="ad.id" :class="{ 'ad_card': true,'is_active': activeAdId === ad.id }">
        <md-card-header>
          <div class="md-title">{{ad.title}}</div>
        </md-card-header>

        <md-card-content>
          {{ad.description}}<br><br>
          Location: {{ad.location}}
        </md-card-content>

        <md-card-actions>
          <span class="plan">{{ad.datetime}}</span>
          <md-button v-on:click="openMap(ad.id, ad.longitude, ad.latitude)">Find on map</md-button>
<!--          style="position:absolute; top: -65px; right: 15px"-->
          <md-button class="md-icon-button md-raised md-warning" @click="deleteAdd(ad)" >
            <md-icon>delete</md-icon>
          </md-button>
        </md-card-actions>
      </md-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AdsList",
  data() {
    return {
    selectedCountry: null,
    activeAdId: null,
    cities: [
      'Los Angeles / USA',
      'Argentina',
      'Brazil',
      'Canada',
      'Italy',
      'Japan',
      'United Kingdom',
      'United States'
    ],
    longitude: null,
    latitude: null,
    }
  },
  props: ['data', 'value', 'items', 'city'],
  computed: {

    localLongitude: {
      get() {
        return this.longitude;
      },
      set(newLongitude) {
        this.$emit('setLongitude', newLongitude);
      },
    },
    localLatitude: {
      get() {
        return this.latitude;
      },
      set(newLatitude) {
        this.$emit('setLatitude', newLatitude);
      },
    },
  },
  watch: {
    data: function() {
      // this._chart.destroy();
      // this.renderLineChart();
    }
  },
  methods: {
    openMap(id, longitude, latitude) {
      this.activeAdId = id;
      this.longitude = longitude;
      this.latitude = latitude;
      this.localLongitude = longitude;
      this.localLatitude = latitude;
    },
    deleteAdd(ad) {
      if (window.confirm('Are you sure you want to delete "'+ad.title+'"?')) {
        let that = this;
        axios.post('http://127.0.0.1:8011/data/delete', {id: ad.id}).then(
            function (response) {
              if(response.data.status){
                that.$parent.getData()
              }
            });
      }
    },
  }

}
</script>

<style>
.ad_card{
  margin-bottom: 10px;
}
.is_active{
  background: #5f6873 !important;
}
.md-card-actions.md-alignment-right {
  justify-content: space-between !important;
}
span.plan{
  margin-left: 8px !important;
}
</style>