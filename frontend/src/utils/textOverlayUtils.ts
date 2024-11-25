import { Feature } from 'ol';
import { LineString } from 'ol/geom';
import { Style, Text, Fill, Stroke } from 'ol/style';
import { Vector as VectorLayer } from 'ol/layer';
import { Vector as VectorSource } from 'ol/source';
import { Map } from 'ol';
import { createPolylineStyle } from './polylineUtils';
import { Segment } from '../types/Segment';


const ZOOM_LEVEL_THRESHOLD = 14;

/**
 * Creates a text style for the segment name.
 * @param segmentName The name of the segment to display as text.
 * @returns The text style.
 */
export const createTextStyle = (segmentName: string): Text => {
    return new Text({
        text: segmentName,
        font: '11px sans-serif',
        placement: 'line',
        rotateWithView: false,
        overflow: true,
        fill: new Fill({ color: 'lightgreen' }),
        stroke: new Stroke({ color: 'black', width: 4 }),
    });
};

/**
 * Creates a combined style for the polyline and text label.
 * @param segment The segment object containing style information.
 * @param showText Whether to show the text label.
 * @returns The combined style for the polyline and text label.
 */
export const createCombinedStyle = (
    segment: Segment,
    showText: boolean
): Style => {
    return new Style({
        stroke: createPolylineStyle(segment).getStroke() || undefined,
        text: showText ? createTextStyle(segment.alt_name) : undefined,
    });
};

/**
 * Creates a text label layer for the segment.
 * @param coordinates The coordinates for the text label.
 * @param segment The segment object containing the alt_name.
 * @param map The map instance to get the current zoom level.
 * @returns The text label layer.
 */
export const createTextLabelLayer = (
    coordinates: [number, number][],
    segment: Segment,
    map: Map
): VectorLayer => {
    const geometry = new LineString(coordinates);
    const feature = new Feature({ geometry, ...segment });

    const source = new VectorSource({
        features: [feature],
    });

    const layer = new VectorLayer({
        source: source,
        visible: true,
        zIndex: 1000,
        declutter: true,
    });

    // Set the initial style based on the current zoom level
    const initialZoom = map.getView().getZoom();
    feature.setStyle(
        createCombinedStyle(
            segment,
            initialZoom !== undefined && initialZoom >= ZOOM_LEVEL_THRESHOLD
        )
    );

    // Listen to the change:resolution event to update the visibility of the text labels
    map.getView().on('change:resolution', () => {
        const zoom = map.getView().getZoom();
        feature.setStyle(
            createCombinedStyle(
                segment,
                zoom !== undefined && zoom >= ZOOM_LEVEL_THRESHOLD
            )
        );
    });

    return layer;
};
