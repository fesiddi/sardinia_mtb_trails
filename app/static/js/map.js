import { createTileLayer } from './tileLayer.js';
import { calculateBounds, calculateExtent } from './bounds.js';
import { addPolylineLayers, fitMapToSegments } from './polyline.js';

export const initMap = (firstSegmentLng, firstSegmentLat, target, segments) => {
    const bounds = calculateBounds(segments);
    const extent = calculateExtent(bounds);

    const map = new ol.Map({
        target: target,
        layers: [createTileLayer()],
        view: new ol.View({
            center: ol.proj.fromLonLat([firstSegmentLng, firstSegmentLat]),
            zoom: 13,
            extent: ol.proj.transformExtent(extent, 'EPSG:4326', 'EPSG:3857'),
        }),
    });

    map.once('postrender', () => {
        addPolylineLayers(map, segments);
        fitMapToSegments(map, segments);
    });

    return map;
};
