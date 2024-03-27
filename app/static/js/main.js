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
    await fetchAndInitializeMap('/segments/alghero', 'map1');
    await fetchAndInitializeMap('/segments/baunei', 'map2');
    await fetchAndInitializeMap('/segments/capoterra', 'map3');
    await fetchAndInitializeMap('/segments/marci', 'map4');
    await fetchAndInitializeMap('/segments/olbia', 'map5');
}

initialize();
