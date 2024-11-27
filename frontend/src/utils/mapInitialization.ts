import { Map, View } from 'ol';
import { Tile as TileLayer } from 'ol/layer';
import { fromLonLat } from 'ol/proj';
import { OSM } from 'ol/source';

/**
 * Initializes the map with a given target element.
 * @param target The target HTML element to render the map.
 * @returns The initialized map instance.
 */
export const initializeMap = (target: HTMLElement, firstSegmentLon: number, firstSegmentLat: number): Map => {
    return new Map({
        target: target,
        layers: [
            new TileLayer({
                source: new OSM(),
            }),
        ],
        view: new View({
            center: fromLonLat([firstSegmentLon, firstSegmentLat]),
            zoom: 13,
        }),
    });
};
