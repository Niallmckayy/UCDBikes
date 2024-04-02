
let map, infoWindow;
import { MarkerClusterer } from "https://cdn.skypack.dev/@googlemaps/markerclusterer@2.3.1";


async function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 53.35026632919465, lng: -6.260428242778603 },
    mapId: "992d9c838bb18c39"
  });

  infoWindow = new google.maps.InfoWindow();


  // Current Location Finder
  const locationButton = document.createElement("button");

  locationButton.textContent = "Pan to Current Location";
  locationButton.classList.add("custom-map-control-button");
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(locationButton);
  locationButton.addEventListener("click", () => {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

          infoWindow.setPosition(pos);
          infoWindow.setContent("Location found.");
          infoWindow.open(map);
          map.setCenter(pos);
        },
        () => {
          handleLocationError(true, infoWindow, map.getCenter());
        },
      );
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
  });

  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );

  // Add some markers to the map.

  const markerInfoWindow = new google.maps.InfoWindow({
    content: "",
    disableAutoPan: true,
  });

  const markers = tourStops.map(({ position, title }, i) => {
    const pin = new PinElement({
      glyph: `${i + 1}`,
    });
    const marker = new AdvancedMarkerElement({
      position,
      map,
      title: `${i + 1}. ${title}`,
      content: pin.element,
    });
    
    marker.addListener("click", ({ domEvent, latLng }) => {
      const { target } = domEvent;

      markerInfoWindow.close();
      markerInfoWindow.setContent(marker.title);
      markerInfoWindow.open(marker.map, marker);
    });

    return marker;
  });

  // Add a marker clusterer to manage the markers.
  new MarkerClusterer({ markers, map });

}



function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation.",
  );
  infoWindow.open(map);

  
}

const tourStops = [
  {position: {lat: 53.350140, lng: -6.260180}, title: "O'Connell Street"},
  {position: {lat: 53.343389, lng: -6.256586}, title: "Trinity College"},
  {position: {lat: 53.336005, lng: -6.259727}, title: "St. Stephen's Green"},
  {position: {lat: 53.345214, lng: -6.265287}, title: "Temple Bar"},
    { position: { lat: 53.342, lng: -6.269 }, title: 'Merrion Square' },
    { position: { lat: 53.346, lng: -6.268 }, title: 'National Gallery of Ireland' },
    { position: { lat: 53.344, lng: -6.266 }, title: 'Grafton Street' },
    { position: { lat: 53.341, lng: -6.272 }, title: 'St. Stephen\'s Green Park' },
    { position: { lat: 53.343, lng: -6.265 }, title: 'Trinity College Library' },
    { position: { lat: 53.348, lng: -6.251 }, title: 'Leinster House' },
    { position: { lat: 53.348, lng: -6.258 }, title: 'Kildare Street' },
    { position: { lat: 53.340, lng: -6.262 }, title: 'Dublin City Hall' },
    { position: { lat: 53.344, lng: -6.263 }, title: 'Temple Bar Square' },
    { position: { lat: 53.345, lng: -6.256 }, title: 'Dublin Castle Gardens' },
    { position: { lat: 53.342, lng: -6.254 }, title: 'Four Courts' },
    { position: { lat: 53.346, lng: -6.260 }, title: 'Ha\'penny Bridge' },
    { position: { lat: 53.338, lng: -6.254 }, title: 'St. Patrick\'s Cathedral' },
    { position: { lat: 53.342, lng: -6.257 }, title: 'Christ Church Cathedral' },
    { position: { lat: 53.342, lng: -6.254 }, title: 'Dublinia' },
    { position: { lat: 53.344, lng: -6.256 }, title: 'Chester Beatty Library' },
    { position: { lat: 53.342, lng: -6.259 }, title: 'Fishamble Street' },
    { position: { lat: 53.343, lng: -6.261 }, title: 'Meeting House Square' },
    { position: { lat: 53.339, lng: -6.259 }, title: 'Marsh\'s Library' },
    { position: { lat: 53.346, lng: -6.252 }, title: 'Government Buildings' },
    { position: { lat: 53.344, lng: -6.249 }, title: 'National Museum of Ireland - Archaeology' },
    { position: { lat: 53.345, lng: -6.257 }, title: 'Dublin City Gallery The Hugh Lane' },
    { position: { lat: 53.344, lng: -6.255 }, title: 'The Spire of Dublin' },
    { position: { lat: 53.345, lng: -6.261 }, title: 'Dublin Writers Museum' },
    { position: { lat: 53.343, lng: -6.247 }, title: 'Grand Canal Square' },
    { position: { lat: 53.349, lng: -6.273 }, title: 'Phoenix Park' },
    { position: { lat: 53.334, lng: -6.265 }, title: 'Guinness Storehouse' },
    { position: { lat: 53.344, lng: -6.268 }, title: 'National Museum of Ireland - Natural History' },
    { position: { lat: 53.340, lng: -6.258 }, title: 'Dublin Unitarian Church' },
    { position: { lat: 53.340, lng: -6.268 }, title: 'St. Audoen\'s Church' },
    { position: { lat: 53.344, lng: -6.269 }, title: 'Leopardstown Racecourse' },
    { position: { lat: 53.341, lng: -6.263 }, title: 'St. Michan\'s Church' },
    { position: { lat: 53.346, lng: -6.267 }, title: 'Royal Hibernian Academy' },
    { position: { lat: 53.347, lng: -6.247 }, title: 'Bord Gáis Energy Theatre' },
    { position: { lat: 53.349, lng: -6.260 }, title: 'Dublinia' },
    { position: { lat: 53.340, lng: -6.262 }, title: 'Christ Church Place' },
    { position: { lat: 53.340, lng: -6.253 }, title: 'Dublin City Wall at Wood Quay' },
    { position: { lat: 53.340, lng: -6.254 }, title: 'The Brazen Head' },
    { position: { lat: 53.343, lng: -6.271 }, title: 'Merrion Square Park' },
    { position: { lat: 53.346, lng: -6.262 }, title: 'Jameson Distillery Bow St.' },
    { position: { lat: 53.343, lng: -6.258 }, title: 'Button Factory' },
    { position: { lat: 53.343, lng: -6.266 }, title: 'Molly Malone Statue' },
    { position: { lat: 53.344, lng: -6.269 }, title: 'National Concert Hall' },
    { position: { lat: 53.342, lng: -6.264 }, title: 'Dublin City Gallery The Hugh Lane' },
    { position: { lat: 53.346, lng: -6.268 }, title: 'The Little Museum of Dublin' },
    { position: { lat: 53.344, lng: -6.267 }, title: 'The Shelbourne, Autograph Collection' },
    { position: { lat: 53.343, lng: -6.255 }, title: 'Bank of Ireland' },
    { position: { lat: 53.339, lng: -6.249 }, title: 'Royal Hospital Kilmainham' },
    { position: { lat: 53.340, lng: -6.251 }, title: 'Irish Museum of Modern Art' },
  
  
];

window.initMap = initMap;

