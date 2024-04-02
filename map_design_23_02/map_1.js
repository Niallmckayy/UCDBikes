
async function initMap() {
  
  // Request needed libraries.
  const { Map, InfoWindow } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement, PinElement } = await google.maps.importLibrary(
    "marker",
  );
  const map = new Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 53.35026632919465, lng: -6.260428242778603 },
    mapId: "992d9c838bb18c39",
  });
  // Set LatLng and title text for the markers. The first marker (Boynton Pass)
  // receives the initial focus when tab is pressed. Use arrow keys to
  // move between markers; press tab again to cycle through the map controls.
  const tourStops = [
      {position: {lat: 53.350140, lng: -6.260180}, title: "O'Connell Street"},
      {position: {lat: 53.343389, lng: -6.256586}, title: "Trinity College"},
      {position: {lat: 53.336005, lng: -6.259727}, title: "St. Stephen's Green"},
      {position: {lat: 53.345214, lng: -6.265287}, title: "Temple Bar"},
  ];
  // Create an info window to share between markers.
  const infoWindow = new InfoWindow();

  // Create the markers.
  tourStops.forEach(({ position, title }, i) => {
    const pin = new PinElement({
      glyph: `${i + 1}`,
    });
    const marker = new AdvancedMarkerElement({
      position,
      map,
      title: `${i + 1}. ${title}`,
      content: pin.element,
    });

    // Add a click listener for each marker, and set up the info window.
    marker.addListener("click", ({ domEvent, latLng }) => {
      const { target } = domEvent;

      infoWindow.close();
      infoWindow.setContent(marker.title);
      infoWindow.open(marker.map, marker);
    });
  });
}

initMap();