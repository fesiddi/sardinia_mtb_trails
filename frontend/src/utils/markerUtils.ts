import { Feature } from 'ol';
import { Point } from 'ol/geom';
import { Style, Fill, Stroke, Circle, Icon } from 'ol/style';
import { fromLonLat } from 'ol/proj';
import { TrailBase } from '../types/TrailArea';

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


export const createTrailBaseMarker = (trailBase: TrailBase): Feature => {
    const feature = new Feature({
        geometry: new Point(fromLonLat(trailBase.coordinates)),
    });
    feature.set('type', 'trailBaseMarker');
    feature.set('name', trailBase.name);
    return feature;
}

export const createTrailBaseMarkerStyle = () =>
    new Style({
        image: new Icon({
            src: 'src/assets/start2.png',
            scale: 0.3,
        }),
    });

