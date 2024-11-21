import { createLayer } from './marker.js';

export function addTrailBaseMarkers(map, trail_bases) {
    trail_bases.forEach((trail_base) => {
        const trailBaseMarker = createTrailBaseMarker(trail_base.coordinates);
        const trailBaseMarkerLayer = createLayer([trailBaseMarker]);

        trailBaseMarker.setStyle(createTrailBaseMarkerStyle());
        map.addLayer(trailBaseMarkerLayer);
    });
}

const createTrailBaseMarker = (trail_base_coord) =>
    new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(trail_base_coord)),
    });

const createTrailBaseMarkerStyle = () =>
    new ol.style.Style({
        image: new ol.style.Icon({
            src: 'static/start3.png',
            scale: 0.3,
        }),
    });
