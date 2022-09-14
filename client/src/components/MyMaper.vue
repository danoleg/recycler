<template>
  <div id = "map" style="width: 100%; height: 100%">
  </div>
</template>

<script>
import View from 'ol/View'
import Map from 'ol/Map'
import Feature from 'ol/Feature'
import TileLayer from 'ol/layer/Tile'
import OSM from 'ol/source/OSM'
import {Vector as VectorLayer} from 'ol/layer';
import {useGeographic} from 'ol/proj';
import {Point} from 'ol/geom';
import {Style, Icon} from 'ol/style';
import {Vector as VectorSource} from 'ol/source';
// import {transform} from 'ol/proj'


export default {
  name: 'MyMaper',
  props: ['longitude','latitude', 'items'],
  data() {
    return {
      map: null,
      pointLayer: null,
      address: null
    }
  },
  mounted() {
    useGeographic();
    let place_loc = [this.longitude, this.latitude];
    let this_longitude = this.longitude
    let layers = [
      new TileLayer({
        source: new OSM()
      }),
    ]
    this.items.forEach(function (item) {
      let place = [item.longitude, item.latitude];
      let item_longitude = item.longitude

      layers.push(new VectorLayer({
        source: new VectorSource({
          features: [new Feature({
            geometry: new Point(place)
          })],
        }),

        style: new Style({
          image: new Icon({
            anchor: [0.5, 1],
            // scale: 0.1,
            src: this_longitude === item_longitude ? 'people-red.svg' : 'people.svg' ,
          })
        })
        //     {
        //   'circle-radius': this_longitude === item_longitude ? 9 : 5 ,
        //   'circle-fill-color': 'red',
        // },
      }));
    });

    if(this.longitude !== null){
      this.map = new Map({
        target: 'map',
        layers: layers,
        view: new View({
          center: place_loc,
          zoom: 16
        })
      })
    }else{
      this.map = new Map({
        target: 'map',
        layers: layers,
        view: new View({
          center: this.items.length > 0 ? [this.items[0].longitude, this.items[0].latitude] : [0,0],
          zoom: this.items.length > 0 ? 7 : 1
        })
      })
    }

    const that = this;

    this.map.on('click', function(evt){
      let lon = evt.coordinate[0];
      let lat = evt.coordinate[1];



      let data_for_url = {lon: lon, lat: lat, format: "jsonv2", limit: 1, "accept-language": "en"};

      let encoded_data = Object.keys(data_for_url).map(function (k) {
        return encodeURIComponent(k) + '=' + encodeURIComponent(data_for_url[k])
      }).join('&');

      let url_nominatim = 'https://nominatim.openstreetmap.org/reverse?' + encoded_data;

      function httpGet(url, callback_function) {

        const getRequest = new XMLHttpRequest();
        getRequest.open("get", url, true);

        getRequest.addEventListener("readystatechange", function () {

          if (getRequest.readyState === 4 && getRequest.status === 200) {

            callback_function(getRequest.responseText);
          }
        });

        getRequest.send();
      }

      httpGet(url_nominatim, function (response_text) {
        let data_json = JSON.parse(response_text);
        // let res_address = data_json.address;
        console.log(data_json.display_name);
        // console.log(res_address);
        that.address = data_json;
        that.localAddress = data_json;

        // this.items.push({
        //   "title":"Batteries 1",
        //   "location": data_json.display_name,
        //   "description": "qwerty qwerty",
        //   "datetime": "22.09.2022 11:00 am",
        //   "longitude": -118.35768242513639,
        //   "latitude": 34.07170480174831
        // })

        // let address_display_name  = data_json.display_name;
        // let address_country       = res_address.country;
        // let address_postcode      = res_address.postcode;
        // let address_city          = res_address.city;
      });


    });
  },
  computed: {

    localAddress: {
      get() {
        return this.address;
      },
      set(newAddress) {
        this.$emit('setNewAddress', newAddress);
      },
    },
  },
  watch: {
    longitude: function() {
      // this.map.render()
      this.$forceUpdate();
    }
  }
}
</script>