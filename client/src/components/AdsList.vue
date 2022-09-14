<template>
  <div style="height: 100%">
<!--    <div style="padding: 0 30px;">-->
<!--      <md-autocomplete v-model="selectedCity" :md-options="cities">-->
<!--        <label>City</label>-->
<!--      </md-autocomplete>-->
<!--    </div>-->
    <div style="max-height: 85vh; overflow-y: scroll">
      <md-card v-for="ad in items" v-bind:key="ad.title" class="ad_card">
        <md-card-header>
          <div class="md-title">{{ad.title}}</div>
        </md-card-header>

        <md-card-content>
          {{ad.description}}<br><br>
          Location: {{ad.location}}
        </md-card-content>

        <md-card-actions>
          <span class="plan">{{ad.datetime}}</span>
          <md-button v-on:click="openMap(ad.longitude, ad.latitude)">Find on map</md-button>
        </md-card-actions>
      </md-card>
    </div>
  </div>
</template>
<script>

export default {
  name: "AdsList",
  data() {
    return {
    selectedCountry: null,
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
    openMap(longitude, latitude) {
      this.longitude = longitude;
      this.latitude = latitude;
      this.localLongitude = longitude;
      this.localLatitude = latitude;
    },
  }

}
</script>

<style>
.ad_card{
  margin-bottom: 10px;
}
.md-card-actions.md-alignment-right {
  justify-content: space-between !important;
}
span.plan{
  margin-left: 8px !important;
}
</style>