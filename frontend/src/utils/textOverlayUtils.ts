import { Feature } from 'ol';
import { LineString } from 'ol/geom';
import { Style, Text, Fill, Stroke } from 'ol/style';
import { Vector as VectorLayer } from 'ol/layer';
import { Vector as VectorSource } from 'ol/source';

/**
 * Creates a text style for the segment name.
 * @param segmentName The name of the segment to display as text.
 * @returns The text style.
 */
export const createTextStyle = (segmentName: string): Style => {
    return new Style({
        text: new Text({
            text: segmentName,
            font: '11px sans-serif',
            placement: 'line',
            rotateWithView: false,
            overflow: true,
            fill: new Fill({ color: 'lightgreen' }),
            stroke: new Stroke({ color: 'black', width: 4 }),
        }),
    });
};

/**
 * Creates a text label layer for the segment.
 * @param coordinates The coordinates for the text label.
 * @param segment The segment object containing the alt_name.
 * @returns The text label layer.
 */
export const createTextLabelLayer = (
    coordinates: [number, number][],
    segment: { alt_name: string }
): VectorLayer => {
    const geometry = new LineString(coordinates);
    const feature = new Feature({ geometry, ...segment });
    feature.setStyle(createTextStyle(segment.alt_name));

    const source = new VectorSource({
        features: [feature],
    });

    const layer = new VectorLayer({
        source: source,
        visible: true,
        zIndex: 1000,
        declutter: true,
    });

    return layer;
};
