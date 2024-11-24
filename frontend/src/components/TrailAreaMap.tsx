import React, { useEffect, useRef } from 'react';
import 'ol/ol.css';
import { Map as OLMap, View } from 'ol';
import { Tile as TileLayer } from 'ol/layer';
import { OSM } from 'ol/source';
import styles from './TrailAreaMap.module.css';

interface TrailAreaMapProps {
    areaShortName: string;
}

const TrailAreaMap: React.FC<TrailAreaMapProps> = ({ areaShortName }) => {
    const mapRef = useRef<HTMLDivElement | null>(null);
    const mapInstanceRef = useRef<OLMap | null>(null);

    useEffect(() => {
        if (!mapRef.current) return;

        console.log('Initializing map');
        const mapInstance = new OLMap({
            target: mapRef.current!,
            layers: [
                new TileLayer({
                    source: new OSM(),
                }),
            ],
            view: new View({
                center: [0, 0],
                zoom: 2,
            }),
        });

        mapInstanceRef.current = mapInstance;

        return () => {
            console.log('Cleaning up map');
            mapInstance.setTarget(undefined);
        };
    }, []);

    return (
        <div className={styles.mapContainer}>
            <div
                id={`map-${areaShortName}`}
                ref={mapRef}
                className={styles.mapContainer}
            ></div>
        </div>
    );
};

export default TrailAreaMap;
