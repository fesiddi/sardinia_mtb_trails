import { initMap } from './map.js';
import { setupPopup } from './popup.js';
import { addPolylineLayers, fitMapToSegments } from './polyline.js';
import { addTrailBaseMarkers } from './trailBaseMarker.js';
import trailAreasData from './trailAreasData.js';

async function fetchAndInitializeMap(areaName, mapId) {
    const segmentsResponse = await fetch(`/segments/${areaName}`);
    const areaResponse = await fetch(`/trail_areas/${areaName}`);

    if (!segmentsResponse.ok) {
        console.error(
            `Error initializing map '${mapId}': ${segmentsResponse.statusText}`
        );
        return;
    }

    const segmentsData = await segmentsResponse.json();
    const areaData = await areaResponse.json();

    if (!segmentsData || segmentsData.length === 0) {
        console.error(`No segments segmentsData found for ${areaName}`);
        return;
    }

    if (!areaData || areaData.length === 0) {
        console.error(`No trail area data found for ${areaName}`);
        return;
    }

    if (segmentsData.some((element) => element === null)) {
        console.error(
            `Error: one or more elements in the segments data are null`
        );
        return;
    }

    const lat = segmentsData[0]['start_lat'];
    const lng = segmentsData[0]['start_lng'];

    const map = initMap(lng, lat, mapId, segmentsData);
    addPolylineLayers(map, segmentsData);
    if (
        areaData.hasOwnProperty('trail_bases') &&
        areaData.trail_bases !== null
    ) {
        addTrailBaseMarkers(map, areaData.trail_bases);
    }
    fitMapToSegments(map, segmentsData);
    setupPopup(map, mapId);
}

async function initialize() {
    for (let i = 0; i < trailAreasData.length; i++) {
        const area = trailAreasData[i];
        const mapId = `map${i + 1}`;
        await fetchAndInitializeMap(area.name, mapId);
    }
}

initialize();
