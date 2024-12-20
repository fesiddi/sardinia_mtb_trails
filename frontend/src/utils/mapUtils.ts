import { Map } from 'ol';
import { Vector as VectorLayer } from 'ol/layer';
import { Vector as VectorSource } from 'ol/source';
import { Segment } from '../types/Segment';
import { createMarker, createMarkerStyle, createTrailBaseMarker, createTrailBaseMarkerStyle } from './markerUtils';
import { createTextLabelLayer } from './textOverlayUtils';
import { createPolylineFeature, createPolylineStyle } from './polylineUtils';
import { decodePolyline } from './decodePolyline';
import { TrailBase } from '../types/TrailArea';

/**
 * Draws all segments on the map.
 * @param map The map instance to draw the segments on.
 * @param segments The array of segment objects containing polyline, start coordinates, and alt_name.
 */
export const drawSegments = (map: Map, segments: Segment[]): void => {
    console.log(
        'Drawing segments:',
        segments.map((segment) => segment.alt_name)
    );
    // Create a single VectorSource to hold all features
    const vectorSource = new VectorSource();

    segments.forEach((segment) => {
        // Create a LineString feature from the decoded polyline
        const lineFeature = createPolylineFeature(segment.polyline);
        lineFeature.setStyle(createPolylineStyle(segment));

        // Create a marker at the start of the polyline
        const startMarker = createMarker([
            segment.start_lng,
            segment.start_lat,
        ]);
        startMarker.setStyle(createMarkerStyle());

        // Create a text label layer for the segment
        const decodedPolyline = decodePolyline(segment.polyline);
        const textLabelLayer = createTextLabelLayer(decodedPolyline, segment, map);

        // Add features to the vector source
        vectorSource.addFeature(lineFeature);
        vectorSource.addFeature(startMarker);
        
        const source = textLabelLayer.getSource();
        if (source) {
            source.getFeatures().forEach((feature) => vectorSource.addFeature(feature));
        }
    });

    // Create a single VectorLayer with the VectorSource
    const vectorLayer = new VectorLayer({
        source: vectorSource,
    });

    // Add the VectorLayer to the map
    map.addLayer(vectorLayer);
};

/**
 * Draws trail base markers on the map.
 * @param map The OpenLayers map instance.
 * @param trailBases The array of trail base objects.
 */
export const drawTrailBases = (map: Map, trailBases: TrailBase[]): void => {
    const vectorSource = new VectorSource();

    trailBases.forEach((trailBase) => {
        const trailBaseMarker = createTrailBaseMarker(trailBase);
        trailBaseMarker.setStyle(createTrailBaseMarkerStyle());
        vectorSource.addFeature(trailBaseMarker);
    });

    // Create a single VectorLayer with the VectorSource
    const vectorLayer = new VectorLayer({
        source: vectorSource,
    });

    // Add the VectorLayer to the map
    map.addLayer(vectorLayer);
}
