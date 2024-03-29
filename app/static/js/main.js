import { initMap } from './map.js';
import { setupPopup } from './popup.js';
import { addPolylineLayers, fitMapToSegments } from './polyline.js';
import trailAreasData from './trailAreasData.js';

async function fetchAndInitializeMap(segmentUrl, mapId) {
    const response = await fetch(segmentUrl);
    const data = await response.json();
    const segments = data;
    const lat = data[0]['start_lat'];
    const lng = data[0]['start_lng'];

    const map = initMap(lng, lat, mapId, segments);
    addPolylineLayers(map, segments);
    fitMapToSegments(map, segments);
    setupPopup(map, mapId);
}

async function initialize() {
    for (let i = 0; i < trailAreasData.length; i++) {
        const area = trailAreasData[i];
        const mapId = `map${i + 1}`;
        await fetchAndInitializeMap(`/location/${area.s_name}`, mapId);
    }
}

initialize();
