import { Feature } from 'ol';
import { LineString } from 'ol/geom';
import { Style, Stroke } from 'ol/style';
import { decodePolyline } from './decodePolyline';
import { Segment } from '../types/Segment';

/**
 * Decodes a polyline and creates a LineString feature.
 * @param polyline The encoded polyline string.
 * @returns The LineString feature.
 */
export const createPolylineFeature = (polyline: string): Feature => {
    const decodedPolyline = decodePolyline(polyline);
    const lineString = new LineString(decodedPolyline);
    return new Feature({
        geometry: lineString,
    });
};


export const createPolylineStyle = (segment: Segment) => {
    let color = setColor(segment);
    let purpleColor = 'rgba(128, 0, 128, 0.8)';
    color = segment.average_grade > 0 ? purpleColor : color;
    return new Style({
        stroke: new Stroke({
            color: color,
            width: 3,
        }),
    });
};

const setColor = (segment: Segment) => {
    if (segment.difficulty === 'green') {
        return 'rgba(70, 180, 20, 1)';
    } else if (segment.difficulty === 'blue') {
        return 'rgba(20, 140, 240, 1)';
    } else if (segment.difficulty === 'red') {
        return 'rgba(220, 19, 19, 1)';
    } else if (segment.difficulty === 'black') {
        return 'rgba(0, 0, 0, 1)';
    } else {
        return 'rgba(220, 19, 19, 1)'; // default to red
    }
};
