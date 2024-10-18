function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 3,
      center: { lat: 0, lng: -180 },
      mapTypeId: "terrain",
    });
    const flightPlanCoordinates = [
      { lat: 42.727944, lng: -73.683790 },
      { lat: 42.727283, lng: -73.680463 },
  
    ];
    const flightPath = new google.maps.Polyline({
      path: flightPlanCoordinates,
      geodesic: true,
      strokeColor: "#FF0000",
      strokeOpacity: 1.0,
      strokeWeight: 6,
    });
  
    flightPath.setMap(map);
  }
  
  window.initMap = initMap;
  