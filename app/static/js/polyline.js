import { createPolylineStyle, createPolyline } from './styles.js';
import { createMarkerStyle, createMarker, createLayer } from './marker.js';
import { decode } from './decode.js';
import { createTextLabelLayer } from './textLabel.js';
import { calculateBounds } from './bounds.js'

export const addPolylineLayers = (map, segments) => {
    segments.forEach((segment) => {
        const { start_lat, start_lng, polyline } = segment;
        const start_latlng = [start_lng, start_lat];
        const marker = createMarker(start_latlng);
        const markerLayer = createLayer([marker]);

        marker.setStyle(createMarkerStyle());
        map.addLayer(markerLayer);

        const latlngs = decode(polyline);
        const decodedPolyline = createPolyline(segment, latlngs);

        decodedPolyline.setStyle(createPolylineStyle(segment));

        const polylineLayer = createLayer([decodedPolyline]);

        map.addLayer(polylineLayer);

        const textLayer = createTextLabelLayer(latlngs, segment);
        map.addLayer(textLayer);
        map.renderSync();
    });
};

export const fitMapToSegments = (map, segments) => {
    let bounds = calculateBounds(segments);
    bounds = ol.proj.transformExtent(
        bounds,
        'EPSG:4326',
        map.getView().getProjection()
    );
    map.getView().fit(bounds, { padding: [50, 50, 50, 50] });
};
