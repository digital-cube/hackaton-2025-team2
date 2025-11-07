import { Component, OnInit, AfterViewInit } from '@angular/core';
import * as L from 'leaflet';
import Openrouteservice from 'openrouteservice-js';
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import { NzInputModule } from 'ng-zorro-antd/input';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-leaflet-map',
  imports: [NzInputModule, FormsModule],
  templateUrl: './leaflet-map.html',
  styleUrl: './leaflet-map.scss',
})
export class LeafletMapComponent implements OnInit, AfterViewInit {
  private map!: L.Map;
  private orsDirections: any;
  private routeLayer?: L.Polyline;

  // Define point A and point B
  private pointA: L.LatLngExpression = [51.505, -0.09]; // London
  private pointB: L.LatLngExpression = [51.515, -0.1]; // Near London

  markers: L.Marker[] = [];
  provider: any;
  results: any;
  searchValue: any;

  constructor() {
    // Initialize OpenRouteService client
    // Note: You need to get a free API key from https://openrouteservice.org/dev/#/signup
    this.orsDirections = new Openrouteservice.Directions({
      api_key: "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjM3YjVmMWNiMDZjODRlNTI5YTYxNzJlZDY0YmNlN2RjIiwiaCI6Im11cm11cjY0In0="
    });
    this.provider = new OpenStreetMapProvider();
  }

  ngOnInit() {
  }

  ngAfterViewInit() {
    this.initMap();
    this.addMarkers();
    this.createRoute();
  }

  private initMap() {
    const baseMapURl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    this.map = L.map('map').setView([51.51, -0.095], 13);
    L.tileLayer(baseMapURl).addTo(this.map);
  }

  private addMarkers() {
    // Add marker for point A (green)
    const markerA = L.marker(this.pointA, {
      icon: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      })
    }).addTo(this.map);
    markerA.bindPopup('Point A (Start)');

    // Add marker for point B (red)
    const markerB = L.marker(this.pointB, {
      icon: L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      })
    }).addTo(this.map);
    markerB.bindPopup('Point B (End)');

    this.markers = [markerA, markerB];
  }

  private createRoute() {
    // Convert LatLng to coordinates format [lng, lat] required by OpenRouteService
    const pointACoords = Array.isArray(this.pointA)
      ? [this.pointA[1], this.pointA[0]]
      : [this.pointA.lng, this.pointA.lat];
    const pointBCoords = Array.isArray(this.pointB)
      ? [this.pointB[1], this.pointB[0]]
      : [this.pointB.lng, this.pointB.lat];

    this.orsDirections.calculate({
      coordinates: [pointACoords, pointBCoords],
      profile: 'driving-car', // Can be: driving-car, cycling-regular, foot-walking, etc.
      format: 'geojson'
    })
    .then((geojson: any) => {
      // Remove previous route if exists
      if (this.routeLayer) {
        this.map.removeLayer(this.routeLayer);
      }

      // Extract coordinates from the GeoJSON response
      const coordinates = geojson.features[0].geometry.coordinates;

      // Convert coordinates from [lng, lat] to [lat, lng] for Leaflet
      const latLngs: L.LatLngExpression[] = coordinates.map((coord: number[]) => [coord[1], coord[0]]);

      // Create and add the route polyline to the map
      this.routeLayer = L.polyline(latLngs, {
        color: 'blue',
        weight: 4,
        opacity: 0.7
      }).addTo(this.map);

      // Get route summary info
      const summary = geojson.features[0].properties.summary;
      console.log(`Distance: ${(summary.distance / 1000).toFixed(2)} km`);
      console.log(`Duration: ${(summary.duration / 60).toFixed(0)} minutes`);

      // Fit map to show the entire route
      this.map.fitBounds(this.routeLayer.getBounds(), { padding: [50, 50] });
    })
    .catch((err: any) => {
      console.error('Error creating route:', err);
      alert('Failed to create route. Please check your API key and internet connection.');
    });
  }

  async onSearch() {
    console.log('working')
    this.results = await this.provider.search({ query: this.searchValue });

    if (this.results && this.results.length > 0) {
      const result = this.results[0];
      const latLng: L.LatLngExpression = [result.y, result.x]; // y is lat, x is lng

      // Create a blue marker for the search result
      const searchMarker = L.marker(latLng, {
        icon: L.icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        })
      }).addTo(this.map);

      searchMarker.bindPopup(result.label).openPopup();

      // Center map on the search result
      this.map.setView(latLng, 15);

      console.log('got the res of search', this.results);
    } else {
      console.log('No results found');
    }
  }
}
