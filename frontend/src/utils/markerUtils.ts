import { Feature } from 'ol';
import { Point } from 'ol/geom';
import { Style, Fill, Stroke, Circle } from 'ol/style';
import { fromLonLat } from 'ol/proj';

/**
 * Creates a marker style.
 * @returns The marker style.
 */
export const createMarkerStyle = (): Style => {
    return new Style({
        image: new Circle({
            radius: 4,
            fill: new Fill({ color: 'yellow' }),
            stroke: new Stroke({
                color: 'black',
                width: 1,
            }),
        }),
    });
};

/**
 * Creates a marker feature.
 * @param start_latlng The latitude and longitude of the marker.
 * @returns The marker feature.
 */
export const createMarker = (start_latlng: [number, number]): Feature => {
    return new Feature({
        geometry: new Point(fromLonLat(start_latlng)),
    });
};
