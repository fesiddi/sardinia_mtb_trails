import { initMap, setupPopup } from './map-utils.js';

async function fetchAndInitializeMap(segmentUrl, mapId) {

    const response = await fetch(segmentUrl);
    const data = await response.json();
    const segments = data;
    const lat = data[0]['start_lat'];
    const lng = data[0]['start_lng'];

    const map = initMap(lng, lat, mapId, segments);
    setupPopup(map, mapId);
}

async function initialize() {
    await fetchAndInitializeMap('/location/alghero', 'map1');
    await fetchAndInitializeMap('/location/baunei', 'map2');
    await fetchAndInitializeMap('/location/capoterra', 'map3');
    await fetchAndInitializeMap('/location/marci', 'map4');
    await fetchAndInitializeMap('/location/olbia', 'map5');
}

initialize();
